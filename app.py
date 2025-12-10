from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-for-dev'

db = SQLAlchemy(app)
fake = Faker()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Simple auth for demo - no password hashing
    password = db.Column(db.String(80), nullable=False)

class LeadSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('lead_search.id'), nullable=False)
    company_name = db.Column(db.String(100))
    contact_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    score = db.Column(db.Integer) # Lead score 0-100

# Helper to generate mock leads
def generate_mock_leads(search_id, industry, location, count=5):
    leads = []
    for _ in range(count):
        lead = Lead(
            search_id=search_id,
            company_name=f"{fake.company()} {industry}",
            contact_name=fake.name(),
            email=fake.company_email(),
            phone=fake.phone_number(),
            score=random.randint(50, 99)
        )
        leads.append(lead)
    return leads

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if not username:
        return redirect(url_for('index'))

    # For MVP, just log them in as a generic user or create if not exists
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password='password')
        db.session.add(user)
        db.session.commit()
    # In a real app, use session management
    return redirect(url_for('dashboard', user_id=user.id))

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    searches = LeadSearch.query.filter_by(user_id=user.id).order_by(LeadSearch.timestamp.desc()).all()
    return render_template('dashboard.html', user=user, searches=searches)

@app.route('/api/generate_leads', methods=['POST'])
def generate_leads():
    data = request.json
    user_id = data.get('user_id')
    industry = data.get('industry')
    location = data.get('location')

    if not all([user_id, industry, location]):
        return jsonify({'error': 'Missing data'}), 400

    # Create Search Record
    search = LeadSearch(user_id=user_id, industry=industry, location=location)
    db.session.add(search)
    db.session.commit()

    # Generate Leads
    leads = generate_mock_leads(search.id, industry, location)
    for lead in leads:
        db.session.add(lead)
    db.session.commit()

    return jsonify({
        'message': 'Leads generated successfully',
        'leads_count': len(leads),
        'search_id': search.id
    })

@app.route('/api/leads/<int:search_id>')
def get_leads(search_id):
    leads = Lead.query.filter_by(search_id=search_id).all()
    results = [{
        'company': l.company_name,
        'contact': l.contact_name,
        'email': l.email,
        'phone': l.phone,
        'score': l.score
    } for l in leads]
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
