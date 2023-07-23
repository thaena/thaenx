import time, os
from random import randint

directory_path = os.path.dirname(os.path.abspath(__file__)) # directory

while True:

    try:

        with open(os.path.join(directory_path, 'notification.py')) as file: # opens
            exec(file.read()) # runs
            file.close() # Closes file

    except Exception as e: # prints on exception
        print(f"Error: {e}")

    time.sleep(randint(797, 897))