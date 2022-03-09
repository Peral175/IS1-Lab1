print("Hello World!")
from datetime import datetime


def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

psychobable = [
    [r'What time(.*)\?',
    ["The current time is: {0} in {1}",
    ]]
]