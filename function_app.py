import logging
import azure.functions as func
import os

#importar a biblioteca de banco de dados
import pyodbc

app = func.FunctionApp()


@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_chamado(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.chamado")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela chamado: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela chamado: {e}")


@app.timer_trigger(schedule="5 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def analistatabela(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.analista")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela analista: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela analista: {e}")


@app.timer_trigger(schedule="10 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def categoriatabela(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.categoria")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela categoria: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela categoria: {e}")


@app.timer_trigger(schedule="15 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def chamado_slatabela(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.chamado_sla")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela chamado_sla: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela chamado_sla: {e}")


@app.timer_trigger(schedule="20 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def chamado_status_historico(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.chamado_status_historico")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela chamado_status_historico: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela chamado_status_historico: {e}")


@app.timer_trigger(schedule="25 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def clienteorganizacaotabela(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.cliente_organizacao")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela cliente_organizacao: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela cliente_organizacao: {e}")


@app.timer_trigger(schedule="30 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def csat_avaliacao(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.csat_avaliacao")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela csat_avaliacao: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela csat_avaliacao: {e}")


@app.timer_trigger(schedule="35 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def fila(myTimer: func.TimerRequest) -> None:

    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")

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

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT TOP 10 * FROM itsm.fila")
            rows = cursor.fetchall()

            logging.info(f"Linhas capturadas da tabela fila: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela fila: {e}")

@app.timer_trigger(schedule="40 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def sla(myTimer: func.TimerRequest) -> None:


    host_sql = os.getenv("HOST")
    database_sql = os.getenv("DATABASE")
    user_sql = os.getenv("USER")
    pass_sql = os.getenv("PASSWORD")


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


    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()


            cursor.execute("SELECT TOP 10 * FROM itsm.sla")
            rows = cursor.fetchall()


            logging.info(f"Linhas capturadas da tabela sla: {len(rows)}")
            for row in rows:
                logging.info(row)
    except Exception as e:
        logging.error(f"Erro ao consultar a tabela sla: {e}")

    