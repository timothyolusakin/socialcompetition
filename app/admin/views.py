from . import admin
from ..model import Skills,Creatives,db
from flask import request,render_template,redirect,url_for
from .mail import send_activation
from .. import current_app
import jwt


#Creating registering route for new users
@admin.route('/register',methods=['GET','POST'])
def registeration():
    #getting every skill from database to display in the registeration tab
    skills = Skills.query.all()
    if request.method == "POST":
        email = request.form["email"]
        instagram_name = request.form["instagram_username"]
        creative_email = Creatives.query.filter_by(email=email).first()
        creative_insta = Creatives.query.filter_by(instagram_account =instagram_name).first()
        if creative_email or creative_insta:
            db.session.rollback()
            return redirect(url_for("admin.registeration"))
        creative = Creatives(
            name= request.form["name"],
            password = request.form["name"],
            email = request.form["email"],
            active = "No",
            instagram_account = request.form["instagram_username"],
            #skill = request.form[""]
        )
        db.session.add(creative)
        db.session.commit()
    return render_template("index.html")

"""@admin.route('/login',methods=['GET','POST'])
def login():
    return render_template("")"""

@admin.route('/admin-dashboard')
def admindashboard():

    return render_template("admin-dashboard.html")

@admin.route('/create-task')
def createtask():
    return render_template("create_task.html")

@admin.route('/view-attendee')
def view_attendee():
    return render_template("view_attendee.html")

@admin.route('/add-winner')
def add_winner():
    return render_template("add winner.html")

@admin.route('/about-platform')
def about_platform():
    return render_template("about.html")


#Creatives are accepted and a mail is sent to them for their approval
@admin.route('/accept-new-creatives',methods=["GET","POST"])
def accept_new_creatives():
    creatives = Creatives.query.filter_by(active = "No")
    return render_template("add_creatives.html",creatives = creatives)

@admin.route('/accept/<int:id>')
def accept(id):
    creative = Creatives.query.filter_by(id=id).first()
    send_activation(creative)
    return redirect(url_for('admin.accept_new_creatives'))

@admin.route('/activate/<token>')
def activate(token):
    creative = Creatives.verify_accept_token(token)
    if not creative:
        return redirect(url_for('admin.registeration'))
    creative.active = "Yes"
    db.session.commit()
    return redirect(url_for('admin.accept_new_creatives'))