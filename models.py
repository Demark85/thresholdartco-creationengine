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
    
    # Relationship to generated content
    generated_contents = db.relationship('GeneratedContent', backref='concept_ref', lazy=True)
    
    def __repr__(self):
        return f'<Concept {self.id}: {self.text[:50]}... (used {self.usage_count} times)>'