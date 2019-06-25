import os
from flask_script import Manager, Shell
from app import create_app,db
from app.model import Creatives,Skill,Skills,Competition_Information,Competition_Skills,Competition_Creatives,Competiton_Attendee,Competiton_Winners

from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(
                app = app,db=db,Creatives=Creatives,Skill=Skill,Skills=Skills,Competition_Information=Competition_Information,Competition_Skills=Competition_Skills,Competition_Creatives=Competition_Creatives,Competiton_Attendee=Competiton_Attendee,Competiton_Winners=Competiton_Winners
                )
manager.add_command("shell",Shell(make_context = make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():

    import unittest
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(test)

if __name__ == '__main__':
    manager.run()
