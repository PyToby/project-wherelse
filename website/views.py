from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from . import ai_process as ai



view = Blueprint('view', __name__)

'''
DYNAMIC URLs

@view.route('/greet/<name>') --> <name> is a variable
def greet(name): --> function takes the name var
    return f"Hello {name}" 

@view.route('/add/<int:num1>/<int:num2>') --> <int: forces string to be int
def greet(num1, num2): --> function takes the name var
    return f"equals {num1 + num2}" 

HANDLING PARAMETERS

@view.route('/handle')
def handle():
    if 'greeting' in request.ars.keys() && 'name' in request.args.keys(): --> if a parameter is missing it will skip this instead of giving an error
        greeting = request.args.get('greeting')
        name = request.args.get('name')
        return f'{greeting}, {name}'
    else:
        return "some params are missing"
'''

@view.route('/')
def home():
    return render_template('base.html')

@view.route('/compare', methods=['GET'])
def compare():
    query = request.args.get('query')

    if query:
        parts = query.lower().split(' vs ')
        if len(parts) == 2:
            service_a = parts[0].strip().title()
            service_b = parts[1].strip().title()
            result = ai.generate_response(service_a, service_b)
            return render_template('compare.html', result=result, service_a=service_a, service_b=service_b, error=None)
        else:
            return render_template('compare.html', result=None, service_a=query, service_b=None, error="Please enter a valid comparison, e.g. Notion vs Obsidian")
    else:
        return render_template('compare.html', result=None, service_a=None, service_b=None, error=None)

@view.route('/dashboard')
@login_required
def dashboard():
    return f"Hello {current_user.name}"

