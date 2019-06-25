from .. import mail,create_app
from flask import render_template
from flask_mail import Message


#A function to send email to recipients
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

#Send activation tokens to creatives for them to accept
def send_activation(user):
    """
    token gets a user specified token from the model
    :param user:
    :return:
    """
    token = user.get_activation_token()
    send_email('[Social app] Activation of Account',
               sender="olusakintimmy@gmail.com",
               recipients=[user.email],
               text_body='',
               html_body=render_template('email/activate.html',user=user, token = token))


