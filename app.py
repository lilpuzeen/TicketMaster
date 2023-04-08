from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iamdijvmenbvnx:c3fb4b1e7dbcf54128126664720c119764a219b2ecf65fa5bfb5896ae3f10d61@ec2-44-213-228-107.compute-1.amazonaws.com:5432/d1rk7igu85ro1d'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://crowd_user:TvD3iHM4f8gDyZlf27uH9mcZ0ctcnQYk@dpg-cgoc58gu9tun42oev7jg-a.frankfurt-postgres.render.com/crowd'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.app_context().push()


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(50), nullable=False)
    is_sold = db.Column(db.Boolean, default=False)
    is_used = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"Ticket with id {self.ticket_id}, sold: {self.is_sold}, used: {self.is_used}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        ticket_id = request.form['approve']
        ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        
        if re.match(r'^\d{6}$', ticket_id) is None:
           return redirect(url_for('index'))
        
        if ticket is None:
            return redirect(url_for('ticket_doesnt_exist'))
        
        if ticket.is_used:
            return redirect(url_for('ticket_used'))
        elif ticket.is_sold and (not ticket.is_used):
            ticket.is_used = True
            db.session.commit()
            return redirect(url_for('guest_added'))
        elif (not ticket.is_sold) and (not ticket.is_used):
            return redirect(url_for('ticket_doesnt_exist'))
    
    return render_template('index.html')


@app.route('/ticket_used', methods=['GET', 'POST'])
def ticket_used():
    return render_template('ticket_used.html')


@app.route('/guest_added', methods=['GET', 'POST'])
def guest_added():
    return render_template('guest_added.html')


@app.route('/ticket_doesnt_exist', methods=['GET', 'POST'])
def ticket_doesnt_exist():
    return render_template('ticket_doesnt_exist.html')


if __name__ == '__main__':
    app.run(debug=True)
