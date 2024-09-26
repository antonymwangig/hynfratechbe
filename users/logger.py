from .models import UserLog

def log_user_action(user, action, details=None):
    """Log user actions to the database"""
    UserLog.objects.create(user=user, action=action, details=details)
