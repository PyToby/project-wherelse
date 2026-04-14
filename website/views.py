from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from .ai_process import ProcessData
from .models import Comparison, UserHistory
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
        return render_template('compare.html', error="Please fill in both inputs")
    
    a, b = normalize_pair(raw_a, raw_b)
    if a == b:
        render_template('compare.html', error="Please input two different services")
        return redirect('/')

    existing = Comparison.query.filter_by(service_a=a, service_b=b).first()
    if existing:
        searched_comparison = existing
        result = json.loads(existing.result_json)
        
    else:
        result = exec(a, b)
        searched_comparison = Comparison(
            service_a=a,
            service_b=b,
            result_json=json.dumps(result)
        )
        db.session.add(searched_comparison)
        db.session.flush()

    if current_user.is_authenticated:
        existing_history = UserHistory.query.filter_by(
            user_id=current_user.user_id,
            comparison_id=searched_comparison.comparison_id
        ).first()

        if not existing_history:
            user_history = UserHistory(
                user_id = current_user.user_id,
                comparison_id = searched_comparison.comparison_id
            )
            db.session.add(user_history)
    
    db.session.commit()
    
    return render_template(
        'compare.html', 
        service_a=raw_a.capitalize(), 
        service_b=raw_b.capitalize(), 
        result=result, 
        error=None
    )

@view.route('/user')
@login_required
def user():
    return render_template('user.html')

@view.route('/pricing')
def pricing():
    return render_template('pricing.html')

@view.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@view.route('/loading')
def loading():
    return render_template('loading.html')

def normalize_pair(a: str, b: str):
    list = [a.strip().lower(), b.strip().lower()]
    pair = sorted(list)
    return pair[0], pair[1]

def exec(a: str, b: str) -> str:
    obj = ProcessData(a, b)
    internet, reddit = obj.scrape()
    response = obj.generate_response(reddit, internet)
    formatted = obj.parse_response(response)
    return formatted