import sqlite3
import os
from flask import Flask, request, render_template, redirect
from flask_httpauth import HTTPBasicAuth
from mbiiez import settings

# Web Tools
from mbiiez_web.tools import tools

# Controllers
from mbiiez_web.controllers.dashboard import controller as dashboard_c
from mbiiez_web.controllers.logs import controller as logs_c
from mbiiez_web.controllers.stats import controller as stats_c
from mbiiez_web.controllers.players import controller as players_c
from mbiiez_web.controllers.instance import controller as instance_c

# Views
from mbiiez_web.views.dashboard import view as dashboard_v
from mbiiez_web.views.logs import view as logs_v
from mbiiez_web.views.stats import view as stats_v
from mbiiez_web.views.players import view as players_v
from mbiiez_web.views.instance import view as instance_v

app = Flask(__name__, static_url_path="/assets", static_folder="mbiiez_web/static", template_folder="mbiiez_web/templates")

# Authentication
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    if(username == settings.web_service.username and password == settings.web_service.password):
        return username
                
@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def home():
    return redirect("/dashboard", code=302)

@app.route('/dashboard', methods=['GET', 'POST'])
@auth.login_required
def dashboard():
    c = dashboard_c()  
    return dashboard_v(c).render()


@app.route('/logs', methods=['GET', 'POST'])
@auth.login_required
def log():
    c = logs_c(request.args.get('instance'), request.args.get('page'), request.args.get('per_page'))
    return logs_v(c).render()
    
@app.route('/players', methods=['GET', 'POST'])
@auth.login_required
def players():
    c = players_c(request.args.get('filter'), request.args.get('page'), request.args.get('per_page'))
    return players_v(c).render()    
    
@app.route('/stats', methods=['GET', 'POST'])
@auth.login_required
def stats():
    c = stats_c(request.args.get('instance'))
    return stats_v(c).render()    

@app.route('/instance', methods=['GET', 'POST'])
@auth.login_required
def instance():
    c = instance_c(request.args.get('instance'))
    return instance_v(c).render()     


@app.context_processor
def include_instances():
    return dict(instances=tools().list_of_instances())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=settings.web_service.port)

