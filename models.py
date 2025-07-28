from main import db
from datetime import datetime

class GeneratedContent(db.Model):
    """Model to store generated MidJourney prompts and Etsy listings"""
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.Text, nullable=False)
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=True)
    midjourney_prompts = db.Column(db.JSON, nullable=False)  # Store as JSON array
    etsy_titles = db.Column(db.JSON, nullable=False)  # Store as JSON array
    etsy_tags = db.Column(db.JSON, nullable=False)  # Store as JSON array
    etsy_description = db.Column(db.Text, nullable=False)
    pinterest_caption = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Analytics tracking
    view_count = db.Column(db.Integer, default=0)
    last_viewed = db.Column(db.DateTime, nullable=True)
    copy_count = db.Column(db.Integer, default=0)  # Track clipboard usage
    last_copied = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<GeneratedContent {self.id}: {self.concept[:50]}...>'
    
    def to_dict(self):
        """Convert model to dictionary for easy JSON serialization"""
        return {
            'id': self.id,
            'concept': self.concept,
            'midjourney_prompts': self.midjourney_prompts,
            'etsy_titles': self.etsy_titles,
            'etsy_tags': self.etsy_tags,
            'etsy_description': self.etsy_description,
            'pinterest_caption': self.pinterest_caption,
            'created_at': self.created_at.isoformat()
        }

class Concept(db.Model):
    """Model to store unique creative concepts for analytics and reuse"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=True, nullable=False)
    usage_count = db.Column(db.Integer, default=1)
    first_used = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Analytics tracking
    total_views = db.Column(db.Integer, default=0)
    total_copies = db.Column(db.Integer, default=0)
    
    # Relationship to generated content
    generated_contents = db.relationship('GeneratedContent', backref='concept_ref', lazy=True)
    
    def __repr__(self):
        return f'<Concept {self.id}: {self.text[:50]}... (used {self.usage_count} times)>'

class AnalyticsEvent(db.Model):
    """Model to track analytics events for performance measurement"""
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # 'view', 'copy', 'generate', etc.
    content_id = db.Column(db.Integer, db.ForeignKey('generated_content.id'), nullable=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'), nullable=True)
    event_data = db.Column(db.JSON, nullable=True)  # Store additional event metadata
    ip_address = db.Column(db.String(45), nullable=True)  # Track user sessions (anonymized)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    content = db.relationship('GeneratedContent', backref='analytics_events')
    concept = db.relationship('Concept', backref='analytics_events')
    
    def __repr__(self):
        return f'<AnalyticsEvent {self.id}: {self.event_type} at {self.created_at}>'