

from extensions import db



# db 
class Archive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    date_upload = db.Column(db.Date, nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    chemin = db.Column(db.String(200), nullable=False)
    

