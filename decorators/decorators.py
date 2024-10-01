from functools import wraps
from flask import request, jsonify 
import os  



def access_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.args.get('key')
        vm_name = request.args.get('vm_name')

        if key != os.getenv('KEY'):
            return jsonify({"completed": False, "message": "Authentication failed"}), 401
        
        elif vm_name is None:
            return jsonify({"completed": False, "message": "Name virtual machine is missing"}), 400

        return func(*args, **kwargs)
    
    return wrapper
