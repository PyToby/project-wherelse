from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from .ai_process import ProcessData
from .models import Comparison
import json
from . import db

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
    raw_a = request.args.get('a', '').strip()
    raw_b = request.args.get('b', '').strip()

    if not raw_a and not raw_b: # MAKES COMPARE BUTTONS WHO DON'T HANDLE INPUT WORK -- just a redirect to /compare
        return render_template('compare.html', result=None, service_a=None, service_b=None, error=None)
    elif not raw_a or not raw_b: # Error handling if user fills in one input only
        render_template('base.html', error="Please fill in both inputs")
        return redirect('/')
    
    a, b = normalize_pair(raw_a, raw_b)
    if a == b:
        render_template('base.html', error="Please input two different services")
        return redirect('/')

    existing = Comparison.query.filter_by(service_a=a, service_b=b).first()
    if existing:
        result = json.loads(existing.result_json)
        return render_template(
            'compare.html', 
            service_a=raw_a.capitalize(), 
            service_b=raw_b.capitalize(), 
            result=result, 
            error=None
        )
    
    process = ProcessData(a, b)
    ai_call_result = process.generate_response()
    
    new_comparison = Comparison(
        service_a=a,
        service_b=b,
        result_json=json.dumps(ai_call_result)
    )
    db.session.add(new_comparison)
    db.session.commit()
    return render_template(
        'compare.html', 
        service_a=raw_a.capitalize(), 
        service_b=raw_b.capitalize(), 
        result=ai_call_result, 
        error=None
    )

@view.route('/user')
@login_required
def user():
    return render_template('user.html')

@view.route('/pricing')
def pricing():
    return render_template('pricing.html')

def normalize_pair(a: str, b: str):
    list = [a.strip().lower(), b.strip().lower()]
    pair = sorted(list)
    return pair[0], pair[1]
