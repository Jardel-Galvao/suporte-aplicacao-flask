from . import database

class DataConsultaSgd(database.Model):
    id =  database.Column(database.Integer, primary_key=True)
    data = database.Column(database.Date, primary_key=True)
