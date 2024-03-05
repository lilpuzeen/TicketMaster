from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(50), nullable=False)
    is_sold = db.Column(db.Boolean, default=False)
    is_used = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"Ticket with id {self.ticket_id}, sold: {self.is_sold}, used: {self.is_used}"
