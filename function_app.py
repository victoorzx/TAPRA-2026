import logging
import azure.functions as func
import os

#importar a biblioteca de banco de dados
import pyodbc

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_chamado(myTimer: func.TimerRequest) -> None:
    
    #capturar variaveis de ambiente
    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

    #como montar uma string de conexao com PYODB AZURE DATABASE SQL
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER=tcp:{host_sql},1433;"
        f"DATABASE={database_sql};"
        f"UID={user_sql};"
        f"PWD={pass_sql};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )   

    #Abrir a conexão
    #fazer um select em qualquer tabela ex: itsm.chamado
    # imprimir usando logging

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            
            cursor.execute("SELECT TOP 10 * FROM itsm.chamado")
            rows = cursor.fetchall()

            
            logging.info(f"Linhas capturadas da tabela chamado: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar o banco: {e}")