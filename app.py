from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, User, LeadSearch, Lead, Campaign
from services.lead_service import LeadService
from services.messaging_service import MessagingService
from services.ad_service import AdService, AnalyticsService
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-for-dev'

db.init_app(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if not username:
        return redirect(url_for('index'))

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password='password')
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('dashboard', user_id=user.id))

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    searches = LeadSearch.query.filter_by(user_id=user.id).order_by(LeadSearch.timestamp.desc()).all()
    campaigns = Campaign.query.filter_by(user_id=user.id).order_by(Campaign.created_at.desc()).all()
    return render_template('dashboard.html', user=user, searches=searches, campaigns=campaigns)

@app.route('/api/generate_leads', methods=['POST'])
def generate_leads():
    data = request.json
    user_id = data.get('user_id')
    industry = data.get('industry')
    location = data.get('location')

    if not all([user_id, industry, location]):
        return jsonify({'error': 'Missing data'}), 400

    search_id, leads = LeadService.generate_leads(user_id, industry, location)

    return jsonify({
        'message': 'Leads generated successfully',
        'leads_count': len(leads),
        'search_id': search_id
    })

@app.route('/api/leads/<int:search_id>')
def get_leads(search_id):
    leads = LeadService.get_leads_by_search(search_id)
    results = [{
        'id': l.id,
        'company': l.company_name,
        'contact': l.contact_name,
        'email': l.email,
        'phone': l.phone,
        'score': l.score
    } for l in leads]
    return jsonify(results)

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    data = request.json
    result = MessagingService.send_message(
        user_id=data.get('user_id'),
        lead_id=data.get('lead_id'),
        channel=data.get('channel'),
        content=data.get('content')
    )
    return jsonify(result)

@app.route('/api/campaigns/launch', methods=['POST'])
def launch_campaign():
    data = request.json
    campaign = AdService.launch_campaign(
        user_id=data.get('user_id'),
        name=data.get('name'),
        platform=data.get('platform'),
        budget=data.get('budget'),
        target_audience=data.get('target')
    )
    return jsonify({
        'success': True,
        'campaign_id': campaign.id,
        'status': campaign.status
    })

@app.route('/api/analytics/<int:campaign_id>')
def get_analytics(campaign_id):
    metric = AnalyticsService.get_campaign_stats(campaign_id)
    if not metric:
        return jsonify({'error': 'No data found'}), 404

    return jsonify({
        'impressions': metric.impressions,
        'clicks': metric.clicks,
        'conversions': metric.conversions,
        'cost': round(metric.cost_spent, 2),
        'timestamp': metric.timestamp.isoformat()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
