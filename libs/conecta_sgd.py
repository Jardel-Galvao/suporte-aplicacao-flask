import pyodbc

def connecta_sgd():
    conn = pyodbc.connect(
            """driver=SQL Anywhere 16; 
                DatabaseName=sgd; 
                AutoStop=NO; 
                Integrated=NO; 
                AutoStart=NO; 
                Host=gw01-aws-int.dominiosistemas.com.br:50015; 
                UID=jardel.sgdrel; 
                PWD=jr#%&sgdrel"""
        )
    return conn
