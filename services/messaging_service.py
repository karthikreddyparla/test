from models import db, MessageLog
import datetime

class MessagingService:
    @staticmethod
    def send_message(user_id, lead_id, channel, content):
        """
        Simulates sending a message (Email/SMS).
        In a real app, this would integrate with SendGrid, Twilio, etc.
        """
        # Logic to "send"
        status = 'Sent'

        # Log the message
        msg = MessageLog(
            user_id=user_id,
            lead_id=lead_id,
            channel=channel,
            content=content,
            status=status,
            sent_at=datetime.datetime.utcnow()
        )
        db.session.add(msg)
        db.session.commit()

        return {
            'success': True,
            'message_id': msg.id,
            'status': status
        }
