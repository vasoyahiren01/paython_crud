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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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

    logging.info("All workers are running.")
    return threads

@app.before_request
def before_request():
    if request.path not in cs.NOT_AUTH_API:
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token, os.environ.get('JWT_SECRET', 'secret'), algorithms=["HS256"])
                user_obj = users.find_by_id(payload['_id'])
                if not user_obj:
                    return jsonify({'message': 'User not found'}), 404
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
        else:
            return jsonify({'message': 'Unauthorized'}), 401


if __name__ == '__main__':
    start_workers()
    port = os.environ.get('PORT', 5000)  # Get the port number from the environment variable 'PORT' or use 5000 as default
    logging.info(f"Starting Flask app on port {port}...")
    app.run(debug=True, port=port)  # Pass the port argument to the run method
    