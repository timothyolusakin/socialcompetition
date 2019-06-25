from ..model import Competition_Creatives
import datetime


#This is to check the time against 24hrs mark
def check_time():
    time2 = datetime.datetime.now()
    time = Competition_Creatives.query.filter_by(id = time2)