from flask import render_template,  Blueprint, flash,   redirect, url_for, request
from models.models import Encaminhamentos, EncaminhamentosIncorretos, DataConsultaSgd, User, IgnorarMes
from datetime import datetime, timedelta
from libs.importa_arquivo_sql import import_sql_file
from libs.connecta_sgd import connecta_sgd
from models.models import database
from flask_login import login_required, logout_user, current_user

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@routes_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    encaminhamentos_incorretos = EncaminhamentosIncorretos.query.all()
    return render_template('listar_encaminhamentos_incorretos_validados.html', encaminhamentos_incorretos=encaminhamentos_incorretos, user=current_user)

@routes_bp.route("/encaminhamentos_para_validacao", methods=["GET", "POST"])
@login_required
def encaminhamentos_para_validacao():
    encaminhamentos_para_validacao = EncaminhamentosIncorretos.query.filter(
        EncaminhamentosIncorretos.analise_analista != "Não avaliado",
        EncaminhamentosIncorretos.concordancia == False,
        EncaminhamentosIncorretos.status == False,
    ).all()
    return render_template('listar_encaminhamentos_para_validacao.html', encaminhamentos_para_validacao=encaminhamentos_para_validacao, user=current_user)
    
@routes_bp.route("/listar_meus_encaminhamentos_para_analise", methods=["GET", "POST"])
@login_required
def listar_meus_encaminhamentos_para_analise():
    dados_usuario = User.query.filter_by(username=current_user.username).first()
    if dados_usuario.isAdmin:
        encaminhamentos_incorretos = EncaminhamentosIncorretos.query.filter_by(analise_analista="Não avaliado").all()
        return render_template('listar_meus_encaminhamentos_para_analise.html', encaminhamentos_incorretos=encaminhamentos_incorretos, user=current_user)
    else:
        encaminhamentos_incorretos = EncaminhamentosIncorretos.query.filter_by(analista=current_user.nome_sgd).filter_by(analise_analista="Não avaliado").all()
        return render_template('listar_meus_encaminhamentos_para_analise.html', encaminhamentos_incorretos=encaminhamentos_incorretos, user=current_user)

@login_required
def retorna_quantidade_encaminhamento_mes(query_encaminhamentos):
    encaminhamentos_por_analista = []
    for encaminhamento in query_encaminhamentos:
        analista = encaminhamento.analista
        mes_encaminhamento = encaminhamento.data.month
        try:
            encaminhamento_existente = next(
                (
                    encaminhamento for encaminhamento in encaminhamentos_por_analista if
                    encaminhamento['analista'] == analista and any(mes['mes'] == mes_encaminhamento for mes in encaminhamento['meses'])
                )
            )
            for mes in encaminhamento_existente['meses']:
                if mes['mes'] == mes_encaminhamento:
                    mes['quantidade'] += 1
        except StopIteration:
            for encaminhamento_por_analista in encaminhamentos_por_analista:
                if encaminhamento_por_analista['analista'] == analista:    
                    if not any(mes for mes in encaminhamento_por_analista['meses'] if mes['mes'] == mes_encaminhamento):
                        novo_mes = {
                            'mes' : mes_encaminhamento,
                            'quantidade' : 0,
                        }
                        encaminhamento_por_analista['meses'].append(novo_mes)
                        break
            else:
                novo_encaminhamento = {
                    'analista' : analista,
                    'meses' : [
                        {
                            'mes' : mes_encaminhamento,  
                            'quantidade' : 1,
                        }
                    ]
                }
                encaminhamentos_por_analista.append(novo_encaminhamento)
    for mes_range in range(1, 13):
        for encaminhamento in encaminhamentos_por_analista:
             if not any(mes for mes in encaminhamento['meses'] if mes['mes'] == mes_range ):
                        novo_mes_zerado = {
                            'mes' : mes_range,
                            'quantidade' : 0,
                        }
                        encaminhamento['meses'].append(novo_mes_zerado)
    return encaminhamentos_por_analista

@routes_bp.route("/meta_quantidade_encaminhamentos_incorretos", methods=['GET'])
@login_required
def meta_quantidade_encaminhamentos_incorretos():
    encaminhamentos_incorretos = EncaminhamentosIncorretos.query.all()
    dict_encaminhamentos_incorreto_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos_incorretos)
    return render_template('meta_quantidade_encaminhamentos_incorretos.html', dict_encaminhamentos_incorreto_mes = dict_encaminhamentos_incorreto_mes, user=current_user)

@routes_bp.route("/meta_quantidade_encaminhamentos", methods=['GET'])
@login_required
def meta_quantidade_encaminhamentos():
    encaminhamentos = Encaminhamentos.query.all()
    dict_encaminhamentos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos)
    return render_template('meta_quantidade_encaminhamentos.html', dict_encaminhamentos_mes = dict_encaminhamentos_mes, user=current_user)

@routes_bp.route('/ignorar_mes', methods=['POST', 'GET'])
@login_required
def ignorar_mes():
    analistas = User.query.all()
    return render_template('ignorar_mes.html', analistas=analistas, user=current_user)

@routes_bp.route('/adicionar_mes_a_ignorar/<int:id>/', methods=['POST', 'GET'])
@login_required
def adicionar_mes_a_ignorar(id):
    analistas = User.query.all()
    analista = User.query.filter_by(id=id).first()
    mes = request.form.get('mes_a_ignorar')
    novo_ignorar_mes = IgnorarMes(id_analista=analista.id, mes=mes)
    database.session.add(novo_ignorar_mes)
    database.session.commit()
    
    return render_template('ignorar_mes.html', analistas=analistas, user=current_user)

@login_required
def verifica_mes_ignorado(mes, id_analista):
    meses_ignorados = IgnorarMes.query.filter_by(id_analista=id_analista, mes=mes).all()
    if meses_ignorados:
        return True
    else:
        return False
    
@login_required
def calcular_media(quantidade, total):
    if quantidade == 0:
        return 100.00
    else:
        return round(100 - (quantidade / total * 100),2 )

@login_required
def ordenar_meses(lista_encaminhamentos):
    encaminhamentos_meses_odenados = []
    for encaminhamento in lista_encaminhamentos:
        meses_ordenados = sorted(encaminhamento['meses'], key=lambda x: x['mes'])
        dict_encaminhamentos_ordenados = {
            'analista': encaminhamento['analista'],
            'meses': meses_ordenados
        }
        encaminhamentos_meses_odenados.append(dict_encaminhamentos_ordenados)
    return encaminhamentos_meses_odenados

@login_required
def adiciona_meses_sem_encaminhamentos(lista_encaminhamentos):
    for mes_range in range(1, 13):
            for encaminhamento in lista_encaminhamentos:
                if not any(mes for mes in encaminhamento['meses'] if mes['mes'] == mes_range):
                            novo_mes_zerado = {
                                'mes' : mes_range,
                                'media' : 0,
                            }
                            encaminhamento['meses'].append(novo_mes_zerado)
    return lista_encaminhamentos

@routes_bp.route("/meta_percent_encaminhamentos", methods=['GET'])
@login_required
def meta_percent_encaminhamentos():
    encaminhamentos = Encaminhamentos.query.all()
    list_encaminhamentos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos)
    encaminhamentos_incorretos = EncaminhamentosIncorretos.query.all()
    list_encaminhamentos_incorretos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos_incorretos)
    list_encaminhamentos_mes = adiciona_meses_sem_encaminhamentos(list_encaminhamentos_mes)
    list_encaminhamentos_mes = ordenar_meses(list_encaminhamentos_mes)
    list_encaminhamentos_incorretos_mes = adiciona_meses_sem_encaminhamentos(list_encaminhamentos_incorretos_mes)
    list_encaminhamentos_incorretos_mes = ordenar_meses(list_encaminhamentos_incorretos_mes)
    encaminhamentos_por_analista_mes = []
    for encaminhamento_mes in list_encaminhamentos_mes:
        analista = encaminhamento_mes['analista']
        id_analista = User.query.filter_by(nome_sgd = analista).first()
        encaminhamentos_incorretos_analista = next(
                    (
                        encaminhamento_incorreto for encaminhamento_incorreto in list_encaminhamentos_incorretos_mes if encaminhamento_incorreto['analista'] == analista 
                    ), None
                )
        for mes in encaminhamento_mes['meses']:
            try: 
                encaminhamento_encontrado = next(
                    encaminhamento_existe for encaminhamento_existe in encaminhamentos_por_analista_mes if
                    encaminhamento_existe['analista'] == analista 
                )
                if encaminhamento_encontrado is not None:
                    for mes_encaminhamentos_incorretos in encaminhamentos_incorretos_analista['meses']:
                        if mes_encaminhamentos_incorretos['mes'] == mes['mes']:
                            valida_mes_ignorado = verifica_mes_ignorado(mes['mes'], id_analista.id)
                            if valida_mes_ignorado is True:
                                media = 0
                            else:
                                if mes_encaminhamentos_incorretos['mes'] > datetime.today().month:
                                    media = 0
                                elif mes_encaminhamentos_incorretos['quantidade'] != 0:
                                    media = round(100 - (mes_encaminhamentos_incorretos['quantidade'] / mes['quantidade'] * 100), 2)
                                else:
                                    media = 100.00 
                            novo_mes = {
                                'mes' : mes['mes'],
                                'media' : media
                            }
                            encaminhamento_encontrado['meses'].append(novo_mes)
            except StopIteration:
                for mes_encaminhamentos_incorretos in encaminhamentos_incorretos_analista['meses']:
                    if mes_encaminhamentos_incorretos['mes'] == mes['mes']:
                        valida_mes_ignorado = verifica_mes_ignorado(mes['mes'], id_analista.id)
                        if valida_mes_ignorado is True:
                            media = 0
                        else:
                            if mes_encaminhamentos_incorretos['mes'] >= datetime.today().month:
                                media = 0
                            elif mes_encaminhamentos_incorretos['quantidade'] != 0:
                                media = round(100 - (mes_encaminhamentos_incorretos['quantidade'] / mes['quantidade'] * 100), 2)
                            else:
                                media = 100.00 
                        novo_encaminhamento = {
                            'analista' : analista,
                            'meses' : [
                                {
                                    'mes' : mes['mes'],
                                    'media' : media,
                                }
                            ]
                        }
                        encaminhamentos_por_analista_mes.append(novo_encaminhamento)
                        break  
    result = render_template('meta_percent_encaminhamentos.html', encaminhamentos_por_analista_mes = encaminhamentos_por_analista_mes, user=current_user)
    return result, encaminhamentos_por_analista_mes

@routes_bp.route("/meta_percent_encaminhamentos_acumulado", methods=["GET"])
@login_required
def meta_percent_encaminhamentos_acumulado():
    _, encaminhamentos_por_analista_mes = meta_percent_encaminhamentos()
    encaminhamentos_por_analista_mes_acumulado = []
    for encaminhamento_mes_percent in encaminhamentos_por_analista_mes:
        id_analista = User.query.filter_by(nome_sgd = encaminhamento_mes_percent['analista']).first()
        armazena_media = 0
        contador_meses = 1
        for mes in encaminhamento_mes_percent['meses']:
            try:
                encaminhamento_encontrado = next(
                    encaminhamento_existe for encaminhamento_existe in encaminhamentos_por_analista_mes_acumulado if
                    encaminhamento_existe['analista'] == encaminhamento_mes_percent['analista']
                )
                valida_mes_ignorado = verifica_mes_ignorado(mes['mes'], id_analista.id)
                if valida_mes_ignorado == True:
                    novo_mes = {
                            'mes' : mes['mes'],
                            'media_acumulada' : 0
                        }
                    encaminhamento_encontrado['meses'].append(novo_mes)
                else:
                    contador_meses += 1
                    armazena_media += mes['media']
                    media_acumulada = round((armazena_media / contador_meses), 2)
                    if mes['mes'] > datetime.today().month:
                        novo_mes = {
                            'mes' : mes['mes'],
                            'media_acumulada' : 0
                        }
                    else:
                        novo_mes = {
                            'mes' : mes['mes'],
                            'media_acumulada' : media_acumulada
                        }
                    encaminhamento_encontrado['meses'].append(novo_mes)
            except StopIteration:
                for mes in encaminhamento_mes_percent['meses']:
                    armazena_media += mes['media']
                    media_acumulada = round((armazena_media / mes['mes']),2)
                    novo_encaminhamento = {
                        'analista' : encaminhamento_mes_percent['analista'],
                        'meses': [
                            {
                                'mes': mes['mes'],
                                'media_acumulada' : media_acumulada
                            }
                        ]
                    }
                    encaminhamentos_por_analista_mes_acumulado.append(novo_encaminhamento)
                    break
    return render_template('meta_percent_encaminhamentos_acumulado.html', encaminhamentos_por_analista_mes_acumulado = encaminhamentos_por_analista_mes_acumulado, user=current_user)

@routes_bp.route("/listar_todos_encaminhamentos", methods=["GET"])
@login_required
def listar_todos_encaminhamentos():
    dados_usuario = User.query.filter_by(username=current_user.username).first()
    if dados_usuario.isAdmin:
        encaminhamentos = Encaminhamentos.query.all()
        return render_template('listar_todos_encaminhamentos.html', encaminhamentos=encaminhamentos, user=current_user)
    else:
        encaminhamentos = Encaminhamentos.query.filter_by(analista=current_user.nome_sgd)
        return render_template('listar_todos_encaminhamentos.html', encaminhamentos=encaminhamentos, user=current_user)

@routes_bp.route("/listar_encaminhamentos_incorretos_validados", methods=["GET"])
@login_required
def listar_encaminhamentos_incorretos_validados():
    dados_usuario = User.query.filter_by(username=current_user.username).first()
    if dados_usuario.isAdmin:
        encaminhamentos = EncaminhamentosIncorretos.query.filter(
            EncaminhamentosIncorretos.validacao == True,
            EncaminhamentosIncorretos.status == True,
            ).all()
        return render_template('listar_encaminhamentos_incorretos_validados.html', encaminhamentos=encaminhamentos, user=current_user)
    else:
        encaminhamentos = EncaminhamentosIncorretos.query.filter(
            EncaminhamentosIncorretos.validacao == True,
            EncaminhamentosIncorretos.status == True,
            EncaminhamentosIncorretos.analista == current_user.nome_sgd,
            ).all()
        return render_template('listar_encaminhamentos_incorretos_validados.html', encaminhamentos=encaminhamentos, user=current_user)

@routes_bp.route("/listar_encaminhamentos_incorretos_invalidados", methods=["GET"])
@login_required
def listar_encaminhamentos_incorretos_invalidados():
    dados_usuario = User.query.filter_by(username=current_user.username).first()
    if dados_usuario.isAdmin:
        encaminhamentos = EncaminhamentosIncorretos.query.filter(
            EncaminhamentosIncorretos.validacao == False,
            EncaminhamentosIncorretos.status == True,
            ).all()
        return render_template('listar_encaminhamentos_incorretos_invalidados.html', encaminhamentos=encaminhamentos, user=current_user)
    else:
        encaminhamentos = EncaminhamentosIncorretos.query.filter(
            EncaminhamentosIncorretos.validacao == False,
            EncaminhamentosIncorretos.status == True,
            EncaminhamentosIncorretos.analista == current_user.nome_sgd,
            ).all()
        return render_template('listar_encaminhamentos_incorretos_invalidados.html', encaminhamentos=encaminhamentos, user=current_user)
    
@routes_bp.route('/atualiza_status_encaminhamento/<int:id>/', methods=["POST"])
@login_required
def atualiza_status_encaminhamento(id):
    concordancia_value = request.form.get('opcao_selecionada')
    concordancia_convertida_bool = concordancia_value.lower() == "true" 
    analise_analista = request.form.get('analise_analista')
    encaminhamento_incorreto = EncaminhamentosIncorretos.query.get(id)
    encaminhamento_incorreto.analise_analista = analise_analista
    encaminhamento_incorreto.concordancia = concordancia_convertida_bool
    if concordancia_convertida_bool == True:
        encaminhamento_incorreto.status = True
    database.session.commit()
    return redirect(url_for('routes.listar_meus_encaminhamentos_para_analise')) 

@routes_bp.route("/valida_inavalida_encaminhamento/<int:id>/", methods=["POST"])
@login_required
def valida_invalida_encaminhamento(id):
    validacao_value = request.form.get('opcao_selecionada')
    descricao_validacao = request.form.get('descricao_validacao')
    validacao_convertida_bool = validacao_value.lower() == "true" 
    encaminhamento_incorreto = EncaminhamentosIncorretos.query.get(id)
    encaminhamento_incorreto.validacao = validacao_convertida_bool
    encaminhamento_incorreto.status = True
    encaminhamento_incorreto.descricao_validacao = descricao_validacao

    database.session.commit()
    return redirect(url_for('routes.encaminhamentos_para_validacao')) 

@login_required
def exclui_encaminhamentos_duplicados(encaminhamentos, encaminhamentos_incorretos):
    lista_dict_exclusao = []
    for encaminhamento_incorreto in encaminhamentos_incorretos:
        for encaminhamento in encaminhamentos:
            if encaminhamento_incorreto.ss == encaminhamento.ss and encaminhamento_incorreto.tramite == encaminhamento.tramite:
                lista_dict_exclusao.append(
                    {
                        "ss" : encaminhamento_incorreto.ss,
                        "tramite" : encaminhamento_incorreto.tramite
                    }
                )
    trupla_itens_exclusao = [(encaminhamento["ss"], encaminhamento["tramite"]) for encaminhamento in lista_dict_exclusao]
    encaminhamentos_sgd_fitlrados = [encaminhamento for encaminhamento in encaminhamentos if (encaminhamento.ss, encaminhamento.tramite) not in trupla_itens_exclusao]

    return encaminhamentos_sgd_fitlrados

@login_required
def adiciona_encaminhamentos(encaminhamentos, encaminhamentos_incorretos):
    for encaminhamento in encaminhamentos:
        data_sgd = encaminhamento[1]
        if data_sgd.microsecond != 0:
            # Remove milliseconds
            data_sem_milisegundos = data_sgd - timedelta(microseconds=data_sgd.microsecond)
        else:
            data_sem_milisegundos = data_sgd
        data_formatada = datetime.strptime(str(data_sem_milisegundos),  "%Y-%m-%d %H:%M:%S").date()
        novo_encaminhamento = Encaminhamentos(
            ss=encaminhamento[0], 
            data=data_formatada, 
            tramite=encaminhamento[2], 
            analista=encaminhamento[3], 
            classificacao=encaminhamento[4], 
            modulo=encaminhamento[5], 
            topico=encaminhamento[6]
        )
        database.session.add(novo_encaminhamento) #adding the note to the database 
        database.session.commit()

    for encaminhamento in encaminhamentos_incorretos:
        data_sgd = encaminhamento[1]
        if data_sgd.microsecond != 0:
            # Remove milliseconds
            data_sem_milisegundos = data_sgd - timedelta(microseconds=data_sgd.microsecond)
        else:
            data_sem_milisegundos = data_sgd
        data_formatada = datetime.strptime(str(data_sem_milisegundos),  "%Y-%m-%d %H:%M:%S").date()
        novo_encaminhamento_incorreto = EncaminhamentosIncorretos(
            ss=encaminhamento[0], 
            data=data_formatada, 
            tramite=encaminhamento[2], 
            analista=encaminhamento[3], 
            descricao_encaminahmento =encaminhamento[4],  
            classificacao=encaminhamento[5], 
            modulo=encaminhamento[6], 
            topico=encaminhamento[7]
        )
        database.session.add(novo_encaminhamento_incorreto) #adding the note to the database 
        database.session.commit()
    return redirect(url_for('routes.listar_meus_encaminhamentos_para_analise'))

@login_required
def consulta_encaminhamentos():
    conn = connecta_sgd()
    sql_statements = import_sql_file("sql/consulta_encaminhamentos.sql")
    cursor = conn.cursor()
    cursor.execute(sql_statements, "2023-01-01", "2023-06-30")
    encaminhamentos__sgd = cursor.fetchall()
    return encaminhamentos__sgd

@login_required
def consulta_encaminhamentos_incorretos():
    conn = connecta_sgd()
    sql_statements = import_sql_file("sql/consulta_encaminhamentos_incorretos.sql")
    cursor = conn.cursor()
    cursor.execute(sql_statements, "2023-01-01", "2023-06-30")
    encaminhamentos_incorretos = cursor.fetchall()
    return encaminhamentos_incorretos 

@routes_bp.route("/atualiza_todos_encaminhamento/", methods=["POST"])
@login_required
def atualiza_todos_encaminhamento():
    try:
        encaminhamentos = consulta_encaminhamentos()
        encaminhamentos_incorretos = consulta_encaminhamentos_incorretos()
        encaminhamentos_para_incluir = exclui_encaminhamentos_duplicados(encaminhamentos, encaminhamentos_incorretos)
        adiciona_encaminhamentos(encaminhamentos_para_incluir, encaminhamentos_incorretos)
        return redirect(url_for('routes.listar_meus_encaminhamentos_para_analise'))
    except Exception as e:
        flash(e)
        return render_template('erro.html', user=current_user)
