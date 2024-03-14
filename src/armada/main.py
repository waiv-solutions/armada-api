from flask import Flask, request, jsonify
from .concierge.concierge import initialize_concierge, execute_concierge
from dotenv import load_dotenv
from .celery_config import make_celery
from celery import Celery

load_dotenv()

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'

celery = make_celery(app)

# Define a Celery task
@celery.task
def execute_concierge_async(request_data):
    # This function now runs as a Celery task
    crew = initialize_concierge(request_data)
    results = execute_concierge(crew)
    return results

@app.route('/concierge', methods=['POST'])
def launch_concierge_endpoint():
    request_data = request.get_json()
    # Launch the task asynchronously
    task = execute_concierge_async.delay(request_data)
    # Return a response immediately, perhaps including the task ID
    return jsonify({'taskId': task.id}), 202

# New route to check the status of a Celery task
@app.route('/task-status/<taskId>', methods=['GET'])
def task_status(taskId):
    task = celery.AsyncResult(taskId)
    return jsonify({'status': task.status, 'result': task.result}), 200

if __name__ == "__main__":
    app.run(debug=True, port=11000)
