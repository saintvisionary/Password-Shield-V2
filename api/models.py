from . import db, bcrypt
from datetime import datetime
import uuid

class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False)

    def __init__(self, email, password, otp_secret):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.otp_secret = otp_secret

    def verify_password(self, password):
        """Verify the user's password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def save_to_db(self):
        """Save the user to the database."""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        """Find a user by email."""
        return cls.query.filter_by(email=email).first()

class HashResult(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    hash_type = db.Column(db.String(20), nullable=False)
    hash_value = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def save_to_db(self):
        """Save the hash result to the database."""
        db.session.add(self)
        db.session.commit()
