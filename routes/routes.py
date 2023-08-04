from flask import render_template,  Blueprint, flash,   redirect, url_for, request
from models.models import Encaminhamentos, EncaminhamentosIncorretos, DataConsultaSgd, User
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
    for i in encaminhamentos_para_validacao:
        print(i.concordancia)
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
                (encaminhamento for encaminhamento in encaminhamentos_por_analista if
                 encaminhamento["analista"] == analista and encaminhamento['meses']['mes'] == mes_encaminhamento)
            )
            encaminhamento_existente['meses']['quantidade'] += 1
        except StopIteration:
            encaminhamento_novo = {
                'analista': analista,
                'meses' : {
                    'mes': mes_encaminhamento,
                    'quantidade': 1
                }
            }
            encaminhamentos_por_analista.append(encaminhamento_novo)
    lista_acumulado_meses = []
    for encaminhamento in encaminhamentos_por_analista:
        analista_meses = encaminhamento['analista']
        mes_meses = encaminhamento['meses']['mes']
        quantidade = encaminhamento['meses']['quantidade']
        for key, mes in encaminhamento['meses'].items():
            print("TAFARELLLLLLLLLLLLLLL")
            print(mes)
            try:
                encaminhamento_existente_meses = next(
                    encaminhamento for encaminhamento in lista_acumulado_meses if
                    encaminhamento["analista"] == analista_meses and mes['mes'] == mes_meses
                )
                lista_acumulado_meses.append(encaminhamento_existente_meses)
            except StopIteration:
                encaminhamento_novo_meses = {
                    'analista': analista_meses,
                    'meses' : {
                        'mes': mes_meses,
                        'quantidade': quantidade
                    }
                }
                lista_acumulado_meses.append(encaminhamento_novo_meses)
    print("ONVIOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(lista_acumulado_meses)
    return encaminhamentos_por_analista

@routes_bp.route("/meta_quantidade_encaminhamentos_incorretos", methods=["GET"])
@login_required
def meta_quantidade_encaminhamentos_incorretos():
    encaminhamentos_incorretos = EncaminhamentosIncorretos.query.all()
    dict_encaminhamentos_incorreto_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos_incorretos)
    dict_encaminhamentos_incorretos_agrupados = {}

    for encaminhamento_mes in dict_encaminhamentos_incorreto_mes:
        if encaminhamento_mes['analista'] not in dict_encaminhamentos_incorretos_agrupados:
            dict_encaminhamentos_incorretos_agrupados[encaminhamento_mes['analista']] = []
        dados = {
                'mes' : encaminhamento_mes['mes'],
                'quantidade' : encaminhamento_mes['quantidade'],
        }
        dict_encaminhamentos_incorretos_agrupados[encaminhamento_mes['analista']].append(dados)

    print(dict_encaminhamentos_incorreto_mes)
    return render_template('meta_quantidade_encaminhamentos_incorretos.html', dict_encaminhamentos_incorretos_agrupados = dict_encaminhamentos_incorretos_agrupados, user=current_user)

@routes_bp.route("/meta_quantidade_encaminhamentos", methods=["GET"])
@login_required
def meta_quantidade_encaminhamentos():
    encaminhamentos = Encaminhamentos.query.all()
    dict_encaminhamentos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos)
    dict_encaminhamentos_agrupados = {}

    for encaminhamento_mes in dict_encaminhamentos_mes:
        if encaminhamento_mes['analista'] not in dict_encaminhamentos_agrupados:
            dict_encaminhamentos_agrupados[encaminhamento_mes['analista']] = []
        dados = {
                'mes' : encaminhamento_mes['mes'],
                'quantidade' : encaminhamento_mes['quantidade'],
        }
        dict_encaminhamentos_agrupados[encaminhamento_mes['analista']].append(dados)

    return render_template('meta_quantidade_encaminhamentos.html', dict_encaminhamentos_agrupados = dict_encaminhamentos_agrupados, user=current_user)

@routes_bp.route("/meta_percent_encaminhamentos", methods=["GET"])
@login_required
def meta_percent_encaminhamentos():
    encaminhamentos = Encaminhamentos.query.all()
    dict_encaminhamentos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos)
    encaminhamentos_incorretos = EncaminhamentosIncorretos.query.all()
    dict_encaminhamentos_incorretos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos_incorretos)
    encaminhamentos_por_analista_mes = []
    for encaminhamento_incorreto in dict_encaminhamentos_incorretos_mes:
        for encaminhamento in dict_encaminhamentos_mes:
            if encaminhamento_incorreto['analista'] == encaminhamento['analista'] and encaminhamento_incorreto['mes'] == encaminhamento['mes']:
                media = round(100 - ((encaminhamento_incorreto['quantidade'] / encaminhamento['quantidade']) * 100), 2)
                encaminhamentos_por_analista_mes.append(
                    {
                        "analista" : encaminhamento['analista'],
                        "mes" : encaminhamento['mes'],
                        "media" : media,
                    }
                )
    return render_template('meta_percent_encaminhamentos.html', encaminhamentos_por_analista_mes = encaminhamentos_por_analista_mes, user=current_user)

@routes_bp.route("/meta_percent_encaminhamentos_acumulado", methods=["GET"])
@login_required
def meta_percent_encaminhamentos_acumulado():
    encaminhamentos = Encaminhamentos.query.all()
    dict_encaminhamentos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos)
    encaminhamentos_incorretos = EncaminhamentosIncorretos.query.all()
    dict_encaminhamentos_incorretos_mes = retorna_quantidade_encaminhamento_mes(encaminhamentos_incorretos)
    soma_media_acumulada = 0
    dict_encaminhamentos_agrupados = {}
    for encaminhamento_mes in dict_encaminhamentos_mes:
        if encaminhamento_mes['analista'] not in dict_encaminhamentos_agrupados:
            dict_encaminhamentos_agrupados[encaminhamento_mes['analista']] = []

        for encaminhamento_incorreto_mes in dict_encaminhamentos_incorretos_mes:
            if encaminhamento_mes['analista'] == encaminhamento_incorreto_mes['analista'] and encaminhamento_mes['mes'] == encaminhamento_incorreto_mes['mes']:
                media_do_mes = round(100 - ((encaminhamento_incorreto_mes['quantidade'] / encaminhamento_mes['quantidade']) * 100), 2) 
                if encaminhamento_mes['mes'] > 1:
                    soma_media_acumulada += media_do_mes
                else:
                    soma_media_acumulada = media_do_mes
                dados = {
                        'mes' : encaminhamento_mes['mes'],
                        'media_acumulada' : soma_media_acumulada,
                }

                dict_encaminhamentos_agrupados[encaminhamento_mes['analista']].append(dados)
        soma_media_acumulada = 0
    return render_template('meta_percent_encaminhamentos_acumulado.html', dict_encaminhamentos_agrupados = dict_encaminhamentos_agrupados, user=current_user)

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
    
@routes_bp.route("/atualiza_status_encaminhamento/<int:id>/", methods=["POST"])
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
