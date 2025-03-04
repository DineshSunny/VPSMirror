import os
import datetime
import time
import random
from multiprocessing import Pool, Manager


def perform_task(task_id):
    # Seed the random number generator based on the task ID
    random.seed(task_id)
    # Generate a random delay time between 0 and 5 seconds
    delay = random.randrange(0, 5)
    # Sleep for the generated delay time
    time.sleep(delay)
    # Get the process and thread details
    current_process = os.getpid()
    current_thread = os.getpid()
    # Return a dictionary with task details
    return {
        "Task_ID": task_id,
        "Process_ID": current_process,
        "Thread_ID": current_thread,
        "Timestamp": datetime.datetime.now(),
    }


def save_results(task_data, mutex):
    # Acquire the lock to ensure only one thread writes at a time
    mutex.acquire()
    try:
        # Open the file in append mode
        with open("output/log.txt", "a") as log_file:
            for entry in task_data:
                # Write the task data to the file
                log_file.write(
                    f'Task ID: {entry["Task_ID"]}, Process ID: {entry["Process_ID"]}, Thread ID: {entry["Thread_ID"]}, Time: {entry["Timestamp"]}\n'
                )
    except Exception as error:
        print(f"Error occurred: {error}")
    finally:
        # Release the lock
        mutex.release()


def execute_tasks():
    # Create a Manager instance to handle shared resources
    with Manager() as manager:
        # Create a mutex lock for synchronization
        lock = manager.Lock()
        # Create a pool of 4 worker processes
        with Pool(processes=4) as task_pool:
            # Map the tasks to the worker processes
            results = task_pool.map(perform_task, [i for i in range(4)])
            # Save the results to a log file
            save_results(results, lock)


if __name__ == "__main__":
    # Run the task execution 10 times
    for _ in range(10):
        execute_tasks()
