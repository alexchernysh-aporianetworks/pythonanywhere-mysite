import subprocess
import os
from .models import ScriptTask
import uuid
import signal
from django.utils import timezone
import time
from django_q.tasks import async_task  # אם כבר קיים אצלך למעלה – אל תכפיל


import subprocess
import os
import time
from .models import ScriptTask


def run_script_task(script_path, unique_code):
    """
    Launch the robust wrapper and let IT manage:
    - stdout / stderr
    - status transitions
    - STOP_REQ handling
    - kill safety
    """

    task = None
    try:
        task = ScriptTask.objects.get(unique_code=unique_code)

        # Wrapper itself will manage RUNNING → DONE / FAILED / KILLED
        task.status = "RUNNING"
        task.save(update_fields=["status"])

        subprocess.Popen(
            [
                "python3",
                "/home/Karmel/Amit/wrapper_print_code.py",
                str(task.id),
                script_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )

        # ❗ חשוב:
        # לא מחכים
        # לא עושים communicate
        # לא בודקים return code
        # Django-Q מסיים פה — ה-wrapper רץ עצמאית

    except ScriptTask.DoesNotExist:
        print(f"Task with unique_code {unique_code} does not exist")

    except Exception as e:
        if task:
            task.status = "FAILED"
            task.error = str(e)
            task.save(update_fields=["status", "error"])




# tasks.py

def run_scheduled_script_task(script_path):
    """
    Wraps run_script_task to execute scheduled tasks as manual tasks.
    """
    try:
        # Create a new task entry in the database
        task = ScriptTask.objects.create(
            script_name=script_path,
            status='PENDING',
            unique_code=uuid.uuid4(),
            created_at=timezone.now()
        )

        # Call run_script_task via Django-Q
        async_task(
            'mysite.tasks.run_script_task',
            script_path,
            str(task.unique_code),  # Ensure unique_code is passed correctly
            hook='mysite.tasks.task_completion_hook'  # Optional hook
        )
    except Exception as e:
        print(f"Failed to schedule task: {e}")