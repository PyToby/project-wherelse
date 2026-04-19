from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from .ai_process import ProcessData
from .models import Comparison, UserHistory
import json, threading, logging
from . import db

view = Blueprint('view', __name__)
logger = logging.getLogger(__name__)

# Naming blueprint => service_a + "||" + service_b  (f.ex. )
jobs = {} # This serves as a cache for pending comparison threads

@view.route('/')
def home():
    return render_template('base.html')

@view.route('/compare', methods=['GET'])
def compare():
    raw_a: str = request.args.get('a', '').strip()
    raw_b: str = request.args.get('b', '').strip()

    if not raw_a and not raw_b: # MAKES COMPARE BUTTONS WHO DON'T HANDLE INPUT WORK -- just a redirect to /compare
        return render_template('compare.html', result=None, service_a=None, service_b=None, error=None, loading=False)
    elif not raw_a or not raw_b: # Error handling if user fills in one input only
        return render_template('compare.html', error="Please fill in both inputs", loading=False)
    
    a, b = normalize_pair(raw_a, raw_b)
    if a == b:
        render_template('compare.html', error="Please input two different services", loading=False)
        return redirect('/')
    
    user_id: int = current_user.user_id if current_user.is_authenticated else None

    existing = Comparison.query.filter_by(service_a=a, service_b=b).first()
    if existing:
        searched_comparison = existing
        result = json.loads(existing.result_json)
        write_history(searched_comparison, user_id)
        return render_template(
            'compare.html', 
            service_a=a.capitalize(), 
            service_b=b.capitalize(), 
            result=result, 
            error=None,
            loading=False
        ) 
    elif (a+"||"+b) in jobs:
        return render_template("compare.html", result=None, loading=True, service_a=a.capitalize(), service_b=b.capitalize(),)
    else:
        ### THREADING ###
        jobs[a+"||"+b] = "pending"
        thread = threading.Thread(target=run, args=(a, b, user_id))
        thread.start()

    
    return render_template(
        'compare.html', 
        service_a=a.capitalize(), 
        service_b=b.capitalize(), 
        result=None, 
        error=None,
        loading=True
    )

def write_history(searched_comparison, user_id):
    if user_id != None:
        existing_history = UserHistory.query.filter_by(
            user_id=user_id,
            comparison_id=searched_comparison.comparison_id
        ).first()

        if not existing_history:
            user_history = UserHistory(
                user_id = user_id,
                comparison_id = searched_comparison.comparison_id
            )
            db.session.add(user_history)
            db.session.commit()

@view.route('/api/status/')
def status():
    raw_a = request.args.get('a', '').strip()
    raw_b = request.args.get('b', '').strip()

    if not raw_a or not raw_b:
        return {"ready": False, "error": "Missing parameters"}, 400
    
    a, b = normalize_pair(raw_a, raw_b)

    if jobs.get(a+"||"+b) == "failed":
        jobs.pop(a+"||"+b, None)
        return {"ready": False, "error": "Generation failed"}, 400

    existing = Comparison.query.filter_by(service_a=a, service_b=b).first()
    if existing:
        result = json.loads(existing.result_json)
        return {"ready": True, "result": result}
    else:
        return {"ready": False}

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

@view.route('/privacy')
def privacy():
    return render_template('privacy.html')

def normalize_pair(a: str, b: str):
    list = [a.strip().lower(), b.strip().lower()]
    pair = sorted(list)
    return pair[0], pair[1]

def run(a: str, b: str, user_id: int):
    '''
    A function running as a thread processing AI information and handling actions after generating

    :param a: Service A
    :param b: Service B
    '''
    from main import app
    with app.app_context():
        try:
            obj = ProcessData(a, b)
            internet, reddit = obj.scrape()
            response = obj.generate_response(reddit, internet)
            formatted = obj.parse_response(response)

            searched_comparison = Comparison(
                service_a=a,
                service_b=b,
                result_json=json.dumps(formatted)
            )
            db.session.add(searched_comparison)
            db.session.commit()
            write_history(searched_comparison, user_id)
        except Exception as e:
            logger.error(f"Generation failed for {a} and {b}: {e}")
            jobs[a+"||"+b] = "failed"