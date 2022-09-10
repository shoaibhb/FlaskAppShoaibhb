from flask_login import UserMixin
from . import db, create_app

# stop your app and open up a Python REPL
# from project import db, create_app
# db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.

# ***** checking UserAdmin PM
class Tbl_pm(UserMixin, db.Model):
    pm_id = db.Column(db.Integer, primary_key=True)
    pm_date = db.Column(db.String(30))
    pm_train = db.Column(db.String(5))
    pm_doc = db.Column(db.String(20))
    pm_mileage = db.Column(db.String(20))
    pm_2w = db.Column(db.String(10))
    pm_1m = db.Column(db.String(10))
    pm_2m = db.Column(db.String(10))
    pm_3m = db.Column(db.String(10))
    pm_6m = db.Column(db.String(10))
    pm_9m = db.Column(db.String(10))
    pm_1y = db.Column(db.String(10))


    # pm_date = db.StringField()
    # pm_train = db.StringField()
    # pm_doc = db.StringField()
    # pm_mileage = db.StringField()
    #
    # def __init__(self, pm_date, pm_train, pm_doc, pm_mileage, pm_2w,pm_1m):
    #     self.pm_date = pm_date
    #     self.pm_train = pm_train
    #     self.pm_doc = pm_doc
    #     self.pm_mileage = pm_mileage
    #     self.pm_2w = pm_2w
    #     self.pm_1m = pm_1m

# ***** End checking UserAdmin PM


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

#    def __repr__(self):
#        return '<User %r>' % self.name