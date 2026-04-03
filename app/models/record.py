from app import db
from datetime import datetime

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # income or expense
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(300))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'type': self.type,
            'category': self.category,
            'date': self.date.isoformat(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }