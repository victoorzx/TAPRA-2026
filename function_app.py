import logging
import azure.functions as func
import requests

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_log_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

@app.route(route="http_get_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_get_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="http_relay_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_relay_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('http_relay_trigger recebeu uma chamada.')

    info = req.params.get('info')
    if not info:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = None
        if req_body:
            info = req_body.get('info')

    if info:
        resultado = f"{info} - processado pela http_relay_trigger"
        return func.HttpResponse(resultado, status_code=200)
    else:
        return func.HttpResponse(
            "Nenhuma informação recebida no parâmetro 'info'.",
            status_code=400
        )

@app.timer_trigger(schedule="0 */2 * * * *", arg_name="timerCaller", run_on_startup=False, use_monitor=False)
def timer_caller_trigger(timerCaller: func.TimerRequest) -> None:
    logging.info('timer_caller_trigger disparado, chamando http_relay_trigger...')

    url = "http://localhost:7071/api/http_relay_trigger"
    params = {"info": "mensagem enviada pela timer_caller_trigger"}

    try:
        response = requests.get(url, params=params, timeout=10)
        logging.info(f'Resposta da http_relay_trigger: {response.text}')
    except Exception as e:
        logging.error(f'Erro ao chamar http_relay_trigger: {e}')