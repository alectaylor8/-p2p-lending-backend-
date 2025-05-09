# Backend - models.py
from . import db  # Import db from the current package
from passlib.hash import pbkdf2_sha256 as sha256

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False) # e.g., "borrower", "lender"

    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    def check_password(self, password):
        return sha256.verify(password, self.password_hash)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    term = db.Column(db.Integer, nullable=False) # in months
    status = db.Column(db.String(20), nullable=False, default="pending") # e.g., pending, funded, repaid

    borrower = db.relationship("User", backref=db.backref("loans", lazy=True))

class LenderPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    max_loan_amount = db.Column(db.Float)
    min_interest_rate = db.Column(db.Float)

    lender = db.relationship("User", backref=db.backref("preferences", lazy=True))

