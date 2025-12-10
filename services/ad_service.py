from models import db, Campaign, CampaignMetric
import random
import datetime

class AdService:
    @staticmethod
    def launch_campaign(user_id, name, platform, budget, target_audience):
        """
        Simulates launching a campaign on an ad platform.
        """
        # Create Campaign Record
        campaign = Campaign(
            user_id=user_id,
            name=name,
            platform=platform,
            budget=float(budget),
            status='Active'
        )
        db.session.add(campaign)
        db.session.commit()

        # Initialize some empty metrics or initial "spend"
        # In a real app, this would be fetched via webhooks/cron jobs

        return campaign

class AnalyticsService:
    @staticmethod
    def generate_mock_performance(campaign_id):
        """
        Simulates gathering performance data for a campaign.
        """
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return None

        # Mock logic: impressions based on budget
        impressions = int(campaign.budget * random.randint(10, 50))
        clicks = int(impressions * random.uniform(0.01, 0.05)) # 1-5% CTR
        conversions = int(clicks * random.uniform(0.05, 0.2)) # 5-20% CR
        cost = campaign.budget * random.uniform(0.5, 1.0) # Spent so far

        metric = CampaignMetric(
            campaign_id=campaign_id,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            cost_spent=cost,
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add(metric)
        db.session.commit()

        return metric

    @staticmethod
    def get_campaign_stats(campaign_id):
        metrics = CampaignMetric.query.filter_by(campaign_id=campaign_id).order_by(CampaignMetric.timestamp.desc()).all()
        # For simple dashboard, just return the latest "snapshot" or aggregate
        # Here we return the latest for simplicity
        if not metrics:
            # Generate on the fly if missing (for demo)
            return AnalyticsService.generate_mock_performance(campaign_id)
        return metrics[0]
