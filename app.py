from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

# Initializing Flask application
app = Flask(__name__)

# Configuring the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visited_cities.db'

# Initializing the database
db = SQLAlchemy(app)

# Defining the City model
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<City {self.name}>'

# Creating the database tables
with app.app_context():
    db.create_all()

# Route for the home page
@app.route('/')
def index():
    cities = City.query.all()
    return render_template('index.html', cities=cities, date=date)  # Pass the date object to the template context

# Route for adding a new city
@app.route('/add', methods=['POST'])
def add_city():
    name = request.form['city']
    visit_date_str = request.form['visit_date']

    # Converting date string to Python date object
    visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()

    city = City(name=name, visit_date=visit_date)
    db.session.add(city)
    db.session.commit()
    return redirect(url_for('index'))

# Route for clearing messages
@app.route('/clear', methods=['POST'])
def clear_messages():
    # Delete all cities from the database
    City.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
