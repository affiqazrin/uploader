from datetime import datetime, timedelta
import threading
import logging

class Scheduler:
    def __init__(self):
        self.tasks = []
        self.logger = logging.getLogger("Scheduler")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def add_task(self, task_func, start_date, end_date=None, frequency=None, duration=None):
        task = {
            "func": task_func,
            "start_date": start_date,
            "end_date": end_date,
            "frequency": frequency,
            "duration": duration
        }
        self.tasks.append(task)

    def run_task(self, task):
        try:
            task_func = task["func"]
            task_func()
            self.logger.info(f"Task '{task_func.__name__}' executed successfully at {datetime.now()}")
            if task["frequency"]:
                threading.Timer(task["frequency"], self.run_task, [task]).start()
        except Exception as e:
            self.logger.error(f"Task '{task_func.__name__}' failed: {e} at {datetime.now()}")

    def start(self):
        for task in self.tasks:
            try:
                start_date = task["start_date"]
                end_date = task["end_date"]
                if not end_date or end_date > datetime.now():
                    delay = (start_date - datetime.now()).total_seconds()
                    if delay > 0:
                        threading.Timer(delay, self.run_task, [task]).start()
                if end_date:
                    delay = (end_date - datetime.now()).total_seconds()
                    if delay > 0:
                        threading.Timer(delay, self.stop_task, [task]).start()
            except Exception as e:
                self.logger.error(f"Error starting task: {e}")

    def stop_task(self, task):
        try:
            if task["duration"]:
                duration = task["duration"]
                end_date = datetime.now() + timedelta(seconds=duration)
                task["end_date"] = end_date
            else:
                self.tasks.remove(task)
        except Exception as e:
            self.logger.error(f"Error stopping task: {e}")

# Example usage:
from datetime import datetime, timedelta

# Assuming kpi_summary is an object with a run method
class kpi_summary:
    @staticmethod
    def run():
        print("Running kpi_summary")

# Example usage:
scheduler = Scheduler()

# Start date and time for the task
start_date = datetime(2024, 4, 4, 9, 30)

# End date and time for the task
end_date = datetime(2024, 4, 22, 8, 0)

# Frequency for the task (every 15 minutes)
frequency = 15 * 60  # 15 minutes in seconds

# Add the task to the scheduler
scheduler.add_task(kpi_summary.run, start_date, end_date, frequency=frequency)

# Start the scheduler
scheduler.start()