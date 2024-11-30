import redis
import json
from task_queue.job_worker import JobWorker

class QueueManager:
    def __init__(self, queue_names):
        self.queue_names = queue_names
        self.redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
        self.job_worker = JobWorker()

    def process_queue(self, queue_name):
        """
        Listen to a specific queue and process jobs.
        """
        print(f"Listening to queue: {queue_name}")
        while True:
            # Fetch the next job ID from the wait list
            job_id = self.redis_client.lpop(queue_name)
            if job_id:
                try:
                    # Construct the Redis key to retrieve job data
                    job_data_key = f"bull:{queue_name.split(':')[1]}:{job_id}"
                    print(f"Fetching data for job key: {job_data_key}")

                    # Fetch the job data from Redis
                    job_data = self.redis_client.hgetall(job_data_key)
                    if job_data and 'data' in job_data:
                        # Parse the job payload (stored as JSON)
                        payload = json.loads(job_data['data'])
                        print(f"Processing job from {queue_name}: {payload}")

                        # Delegate processing to JobWorker
                        self.job_worker.process_job(queue_name, payload)
                    else:
                        print(f"No valid data found for job ID: {job_id}")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse job data for ID {job_id}: {e}")
                except Exception as e:
                    print(f"Error processing job from {queue_name}: {e}")
