import csv
import io
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
import pyodbc
from azure.storage.filedatalake import DataLakeServiceClient

app = func.FunctionApp()


def get_conn_str():
    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")
    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )


def extract_to_bronze(table):
    logging.info(f"tabela {table}")
    try:
        with pyodbc.connect(get_conn_str()) as conn:
            cursor = conn.cursor()
            cursor.execute(f"select * from itsm.{table}")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            logging.info(f"{len(rows)} linhas lidas de itsm.{table}")

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(columns)
        writer.writerows(rows)

        now = datetime.now(timezone.utc)
        file_path = f"{table}/{now:%Y/%m/%d}/{table}_{now:%Y%m%d_%H%M%S}.csv"

        datalake = DataLakeServiceClient.from_connection_string(
            os.getenv("DATALAKE_CONNECTION_STRING")
        )
        file_client = datalake.get_file_system_client("bronze").get_file_client(
            file_path
        )
        file_client.upload_data(buffer.getvalue().encode("utf-8"), overwrite=True)

        logging.info(f"Arquivo gravado em bronze/{file_path}")
    except Exception as e:
        logging.error(f"Erro ao ler itsm.{table}: {str(e)}")
        raise


@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_chamado(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("chamado")


@app.timer_trigger(
    schedule="5 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_analista(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("analista")


@app.timer_trigger(
    schedule="10 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_categoria(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("categoria")


@app.timer_trigger(
    schedule="15 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_chamado_sla(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("chamado_sla")


@app.timer_trigger(
    schedule="20 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_chamado_status_historico(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("chamado_status_historico")


@app.timer_trigger(
    schedule="25 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_cliente_organizacao(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("cliente_organizacao")


@app.timer_trigger(
    schedule="30 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_csat_avaliacao(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("csat_avaliacao")


@app.timer_trigger(
    schedule="35 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_fila(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("fila")


@app.timer_trigger(
    schedule="40 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_sla(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("sla")


@app.timer_trigger(
    schedule="45 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def extract_solicitante(myTimer: func.TimerRequest) -> None:
    extract_to_bronze("solicitante")
