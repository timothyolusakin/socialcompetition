from flask import  Blueprint

creatives = Blueprint('creative',__name__)

from . import views