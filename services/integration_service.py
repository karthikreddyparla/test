from models import db, AdAccount
from datetime import datetime
import uuid

class IntegrationService:
    @staticmethod
    def get_user_integrations(user_id):
        return AdAccount.query.filter_by(user_id=user_id).all()

    @staticmethod
    def toggle_integration(user_id, platform, action):
        """
        Connect or Disconnect a platform.
        action: 'connect' | 'disconnect'
        """
        account = AdAccount.query.filter_by(user_id=user_id, platform=platform).first()

        if action == 'connect':
            if not account:
                account = AdAccount(user_id=user_id, platform=platform)

            # Simulate OAuth Token Generation
            account.access_token = f"mock_token_{platform}_{uuid.uuid4()}"
            account.is_connected = True
            account.last_connected_at = datetime.utcnow()
            db.session.add(account)
            db.session.commit()
            return {'success': True, 'status': 'connected'}

        elif action == 'disconnect':
            if account:
                account.is_connected = False
                account.access_token = None
                db.session.add(account)
                db.session.commit()
            return {'success': True, 'status': 'disconnected'}

        return {'success': False, 'error': 'Invalid action'}

    @staticmethod
    def is_platform_connected(user_id, platform):
        account = AdAccount.query.filter_by(
            user_id=user_id,
            platform=platform,
            is_connected=True
        ).first()
        return account is not None
