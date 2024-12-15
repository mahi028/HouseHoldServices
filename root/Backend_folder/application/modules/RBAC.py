from functools import wraps
from flask_jwt_extended import jwt_required, current_user
from flask import request, abort
from application import csrf

def admin_required(fn):
    """Decorater for Admin Authentication"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(404)
        
        if current_user.role != 1:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

def pro_required(fn):
    """Decorater for Service Pro Authentication"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(404)
        
        if current_user.role != 2:
            abort(403)
        
        return fn(*args, **kwargs)
    return wrapper

def cust_required(fn):
    """Decorater for Customer Authentication"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(404)
        
        if current_user.role != 3:
            abort(403)
        
        return fn(*args, **kwargs)
    return wrapper

def csrf_protected(fn):
    """Enables Flask WTF CSRF Protection for FlaskForms"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method != 'GET':
            csrf_token = request.headers.get('X-CSRF-TOKEN')
            if not csrf_token:
                print('h')
                abort(400, description="CSRF token missing")
            try:
                csrf.protect()
            except Exception:
                print('l')
                abort(400, description="CSRF token invalid")
        return fn(*args, **kwargs)
    return wrapper