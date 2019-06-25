from flask import current_app
import datetime
import jwt
from ..model import Creatives,Skills,Skill
#SET TOKEN FOR EMAIL AND CREATE TIME EXPIRATION
def generate_email_tokens(self):
    return jwt.encode(
        {'email': self.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours = 24)},
        current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

@staticmethod
def decode_email_tokens(token):
    try:
        public_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['email']
    except jwt.ExpiredSignatureError:
            user =  Creatives.query.filter_by(public_id=public_id)
            return