import uuid
from django.db import models


# Define STATUS_CHOICES
STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('RUNNING', 'Running'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
    ('KILLED', 'Killed'),
    ("STOP_REQUESTED", "STOP_REQUESTED")
]

class ScriptTask(models.Model):
    id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=255)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique code per execution
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='PENDING')
    output = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.script_name} - {self.status}"

    class Meta:
        app_label = 'mysite'




from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
import os




class ScheduledScriptTask(models.Model):
    script_path = models.CharField(
        max_length=2550,
        help_text="Enter the full path to the script."
    )
    run_time = models.TimeField(
        help_text="Time of day to run the script (24-hour format)."
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="Timezone for the scheduled task."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Toggle to activate/deactivate the task."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.script_path} - {self.run_time} ({self.timezone})"




from django.core.exceptions import ValidationError
import os

def validate_script_path(value):
    """
    Validates that the given script path exists and is executable.
    """
    if not os.path.isfile(value):
        raise ValidationError(f"The path '{value}' does not exist or is not a file.")
    if not os.access(value, os.X_OK):
        raise ValidationError(f"The file at '{value}' is not executable.")