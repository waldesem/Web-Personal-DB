import os
import requests

import dramatiq
from flask_melodramatiq import RabbitmqBroker

broker = RabbitmqBroker()
dramatiq.set_broker(broker)

basedir = os.path.abspath(os.path.dirname(__file__))

@dramatiq.actor
def task_queue(anketa):
    """
    A function that represents a task queue.
    Parameters:
    - anketa: The input data for the task queue.
    Returns:
    - 'OK' if the result of the task queue is True, otherwise 'None'.
    """
    try:
        # Send a request to check if the resume can be sent
        response = requests.post(url='https://httpbin.org/post', json=anketa, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:
            # If the resume can be sent, update its status and commit the changes to the database
            return {'message': "Success"}
        else:
            # If the resume cannot be sent, return an error message
            return {'message': "Fail"}
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        return {'message': f"Отправка не удалась ({e})"}
    
