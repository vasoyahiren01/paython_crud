__author__ = "Hiren Vasoya"
__date__ = "2023-06-06"
__version__ = '1.0.0'
import jwt
import os  # Import the os module to access environment variables
from flask import Flask, request, jsonify
from models import users  # call model file
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other
from router.user_route import extendApplication
import constant as cs
import threading
from task_queue.job_manager import QueueManager

app = Flask(__name__)
CORS(app)

users = users.Users()
extendApplication(app)


def start_workers():
    """
    Start threads for all queues.
    """
    queue_manager = QueueManager(cs.QUEUE_NAMES)
    threads = []

    for queue_name in cs.QUEUE_NAMES:
        thread = threading.Thread(target=queue_manager.process_queue, args=(queue_name,))
        thread.daemon = True  # Ensure threads close when the Flask app stops
        threads.append(thread)
        thread.start()

    print("All workers are running.")
    return threads

@app.before_request
def before_request():
    # print('url: %s ,data: %s' % (request.path, request.values.to_dict()), extra={"type": request.method})
    if request.path not in cs.NOT_AUTH_API:
        token = request.headers.get('Authorization')
        if token:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            if payload['_id']:
                user_obj = users.find_by_id(payload['_id'])
                if user_obj['_id'] == False:
                    return jsonify({'message': 'user Not found'}), 404
            else:
                return jsonify({'message': 'invalid token or token has been expired'}), 404
        else:
            return jsonify({'message': 'Unauthorized'}), 404


if __name__ == '__main__':
    start_workers()
    port = os.environ.get('PORT', 5000)  # Get the port number from the environment variable 'PORT' or use 5000 as default
    print(f"Starting Flask app on port {port}...")
    app.run(debug=True, port=port)  # Pass the port argument to the run method
    