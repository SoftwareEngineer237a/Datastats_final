# app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime, timezone

# Constants for roles
ROLE_ANALYST = 'analyst'
ROLE_VIEWER = 'viewer'

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_analyst(self):
        return self.role == ROLE_ANALYST

    def is_viewer(self):
        return self.role == ROLE_VIEWER


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Dataset(db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(20))
    records = db.Column(db.Integer)
    uploaded_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='datasets')

class AnalysisLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(256))
    status = db.Column(db.String(20), default='pending')  # 'pending' or 'completed'
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))  # ✅ Add this line
    analysis_type = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Graph(db.Model):
    __tablename__ = 'graphs'  # optional but clearer

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    graph_type = db.Column(db.String(50))
    
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)  # FIXED HERE
    
    analysis_type = db.Column(db.String(50))  # e.g., 'pca', 'raw', 'regression'
    file_path = db.Column(db.String(200))
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # FIXED HERE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional relationships (if you want backrefs)
    dataset = db.relationship('Dataset', backref='graphs')
    user = db.relationship('User', backref='graphs')
    
class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # 'single' or 'comprehensive'
    file_path = db.Column(db.String(500), nullable=False)  # relative path to PDF file
    analyses_included = db.Column(db.Text)  # comma-separated list of analyses
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_size = db.Column(db.Integer)  # file size in bytes
    
    # Relationships
    dataset = db.relationship('Dataset', backref='reports')
    creator = db.relationship('User', backref='created_reports', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Report {self.title}>'
    
    @property
    def formatted_size(self):
        """Return human-readable file size"""
        if not self.file_size:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    @property
    def analyses_list(self):
        """Return list of analyses included"""
        if self.analyses_included:
            return [analysis.strip() for analysis in self.analyses_included.split(',')]
        return []

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))  # ✅ Add this line
    analysis_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
