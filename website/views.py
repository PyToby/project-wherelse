from flask import Blueprint, render_template, request
#from flask_login import current_user, login_required

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