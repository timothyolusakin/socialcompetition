from . import creatives
from ..model import Skill,Creatives,db
from flask import request,render_template,redirect,url_for


@creatives.route('/index')
def creative():
    return  render_template('about.html')

@creatives.route('/accepttask')
def accept_task():
    return  render_template('accept_task.html')

@creatives.route('/submit-task')
def submit_task():
    return  render_template('submit_task.html')

@creatives.route('/view_profile')
def view_profile():
    return  render_template('view_profile.html')