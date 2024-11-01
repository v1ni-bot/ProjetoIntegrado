
# Essa query serve para conectar com o banco
#pip install mysql-connector-python
#pip install streamlit

import mysql.connector
import pandas as pd

def conexao(query): # vai buscar no arquivo do dash
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="senai@134",
        db="bd_medidor"
    )

    dataframe= pd.read_sql(query, conn) # vai retornar a query

    conn.close() #vai fechar a conexão

    return dataframe