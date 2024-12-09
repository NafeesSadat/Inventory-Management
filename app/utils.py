from flask_login import current_user
from functools import wraps
from flask import redirect, url_for

def role_required(role_name):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role.name != role_name:
                return redirect(url_for('routes.login'))
            return func(*args, **kwargs)
        return decorated_view
    return wrapper