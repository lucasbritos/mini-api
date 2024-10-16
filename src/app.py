import json
import logging
from logging_config import setup_logging

from bottle import Bottle, request, response
from plugins import stopwatch, error_handler_plugin, authorize

# Setup logging, only here and once # TODO: OS env in import??
setup_logging()

logger = logging.getLogger(__name__)

app = Bottle()

app.install(stopwatch)
app.install(error_handler_plugin)
app.install(authorize)


@app.route('/tasks', method=['GET'])
def get_tasks():
    tasks = [{"name": "task1"},{"name":"task2"}]
    response.status = 200
    response.content_type = 'application/json'
    return json.dumps(tasks)

@app.hook('after_request')
def log_request():
    # Log method, path, status code, and any other relevant information
    logging.info(f"{request.method} {request.path} - Status: {response.status} exec_time: {float(response.headers['X-Exec-Time'])}")

# This should be last
@app.route("/<url:path>")
def index(url):
  logger.info(f"Route not found:{url}")
  response.status = 404
  return "Not found"