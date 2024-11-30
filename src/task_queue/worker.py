from src.task_queue.job_worker import JobWorker
import constant as cs
import threading


def start_worker(queue_name):
    """Start a worker for a specific queue."""
    worker = JobWorker(queue_name)
    worker.listen_to_queue()


if __name__ == "__main__":
    threads = []
    for queue_name in cs.QUEUE_NAMES:
        thread = threading.Thread(target=start_worker, args=(queue_name,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
