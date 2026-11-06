import csv
import io
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
import pyodbc
from azure.storage.filedatalake import DataLakeServiceClient

app = func.FunctionApp()


def build_conn_str(server, database, user, password):
    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )


def get_conn_str():
    return build_conn_str(
        os.getenv("HOST"),
        os.getenv("DATABASE"),
        os.getenv("USER"),
        os.getenv("PASSWORD"),
    )


def get_dest_conn_str():
    return build_conn_str(
        os.getenv("DEST_HOST"),
        os.getenv("DEST_DATABASE"),
        os.getenv("DEST_USER"),
        os.getenv("DEST_PASSWORD"),
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


LOAD_ORDER = [
    "fila",
    "categoria",
    "sla",
    "cliente_organizacao",
    "analista",
    "solicitante",
    "chamado",
    "chamado_sla",
    "chamado_status_historico",
    "csat_avaliacao",
]


def read_latest_csv(file_system, table):
    paths = [
        p.name
        for p in file_system.get_paths(path=table)
        if not p.is_directory and p.name.endswith(".csv")
    ]
    if not paths:
        raise FileNotFoundError(f"Nenhum arquivo em bronze/{table}")
    latest = max(paths)
    content = file_system.get_file_client(latest).download_file().readall()
    reader = csv.reader(io.StringIO(content.decode("utf-8"), newline=""))
    header = next(reader)
    rows = list(reader)
    logging.info(f"{len(rows)} linhas lidas de bronze/{latest}")
    return header, rows


def get_column_types(cursor, table):
    cursor.execute(
        "select column_name, data_type from information_schema.columns "
        "where table_schema = 'itsm' and table_name = ?",
        table,
    )
    return {row[0]: row[1] for row in cursor.fetchall()}


def convert_value(value, data_type):
    if value == "":
        return None
    if data_type in ("int", "bigint", "smallint", "tinyint"):
        return int(value)
    if data_type == "bit":
        return value.strip().lower() in ("true", "1")
    if data_type in ("datetime2", "datetime", "smalldatetime", "date"):
        return datetime.fromisoformat(value)
    return value


def load_to_destination():
    file_system = DataLakeServiceClient.from_connection_string(
        os.getenv("DATALAKE_CONNECTION_STRING")
    ).get_file_system_client("bronze")

    data = {}
    for table in LOAD_ORDER:
        data[table] = read_latest_csv(file_system, table)

    conn = pyodbc.connect(get_dest_conn_str())
    try:
        cursor = conn.cursor()
        for table in reversed(LOAD_ORDER):
            cursor.execute(f"delete from itsm.{table}")
        for table in LOAD_ORDER:
            header, rows = data[table]
            types = get_column_types(cursor, table)
            converted = [
                [convert_value(v, types[c]) for v, c in zip(row, header)]
                for row in rows
            ]
            if converted:
                placeholders = ", ".join("?" for _ in header)
                cursor.executemany(
                    f"insert into itsm.{table} ({', '.join(header)}) "
                    f"values ({placeholders})",
                    converted,
                )
            logging.info(f"{len(converted)} linhas gravadas em itsm.{table}")
        conn.commit()
        logging.info("Carga no banco de destino concluída")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro na carga do destino: {str(e)}")
        raise
    finally:
        conn.close()


@app.timer_trigger(
    schedule="0 0 3 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def load_destino(myTimer: func.TimerRequest) -> None:
    load_to_destination()