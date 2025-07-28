import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import random
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Fallback configuration for development
if not app.config["SQLALCHEMY_DATABASE_URI"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///thresholdartco.db"

# Initialize the app with the extension
db.init_app(app)

def generate_midjourney_prompts(concept):
    """Generate 2-3 MidJourney prompts based on the creative concept"""
    
    # Art styles and techniques
    styles = [
        "watercolor painting", "oil painting", "digital art", "acrylic painting",
        "ink illustration", "pencil sketch", "gouache", "mixed media",
        "impressionist style", "abstract expressionism", "minimalist design"
    ]
    
    # Lighting and mood descriptors
    lighting = [
        "golden hour lighting", "soft diffused light", "dramatic shadows",
        "ethereal glow", "warm sunset light", "cool morning mist",
        "dappled sunlight", "moody atmosphere", "cinematic lighting"
    ]
    
    # Technical parameters
    technical = [
        "--ar 3:4 --v 6", "--ar 2:3 --v 6", "--ar 4:5 --v 6",
        "--ar 3:4 --stylize 750", "--ar 2:3 --stylize 500"
    ]
    
    prompts = []
    
    # Generate 3 different styled prompts
    for i in range(3):
        style = random.choice(styles)
        light = random.choice(lighting)
        tech = random.choice(technical)
        
        if i == 0:
            # Detailed artistic prompt
            prompt = f"{concept}, {style}, {light}, highly detailed, beautiful composition, trending on artstation {tech}"
        elif i == 1:
            # Mood-focused prompt
            prompt = f"{concept}, {light}, dreamy atmosphere, soft colors, {style}, serene and peaceful {tech}"
        else:
            # Abstract/artistic interpretation
            prompt = f"abstract interpretation of {concept}, {style}, {light}, artistic, expressive brushstrokes {tech}"
        
        prompts.append(prompt)
    
    return prompts

def generate_etsy_titles(concept):
    """Generate 3 SEO-focused Etsy titles that are emotional and poetic"""
    
    # Emotional descriptors
    emotions = [
        "Dreamy", "Serene", "Mystical", "Enchanting", "Peaceful",
        "Romantic", "Whimsical", "Ethereal", "Magical", "Tranquil"
    ]
    
    # Art types
    art_types = [
        "Digital Art Print", "Wall Art Download", "Printable Art",
        "Digital Download", "Art Print", "Instant Download"
    ]
    
    # Room/decor descriptors
    rooms = [
        "Bedroom Decor", "Living Room Art", "Office Wall Art",
        "Home Decor", "Nursery Art", "Boho Decor"
    ]
    
    titles = []
    
    # Title 1: Emotional + Concept + Art Type
    emotion1 = random.choice(emotions)
    art_type1 = random.choice(art_types)
    title1 = f"{emotion1} {concept.title()} {art_type1} | {random.choice(rooms)}"
    titles.append(title1)
    
    # Title 2: Concept + Poetic descriptor + Download
    emotion2 = random.choice(emotions)
    title2 = f"{concept.title()} Art Print | {emotion2} Digital Download | Instant Wall Art"
    titles.append(title2)
    
    # Title 3: Room-focused with concept
    room = random.choice(rooms)
    emotion3 = random.choice(emotions)
    title3 = f"{emotion3} {concept.title()} Print | {room} | Downloadable Art"
    titles.append(title3)
    
    return titles

def generate_etsy_tags(concept):
    """Generate 13 Etsy tags (20 characters or fewer each)"""
    
    # Base tags related to digital art
    base_tags = [
        "digital download", "printable art", "wall art", "home decor",
        "instant download", "digital print", "art print", "boho decor"
    ]
    
    # Concept-related tags (extract keywords from concept)
    concept_words = concept.lower().split()
    concept_tags = []
    
    # Add individual words from concept if they're under 20 chars
    for word in concept_words:
        if len(word) <= 20 and word not in ['a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to']:
            concept_tags.append(word)
    
    # Style tags
    style_tags = [
        "watercolor", "abstract", "modern art", "minimalist", "nature art",
        "landscape art", "botanical print", "floral art", "vintage style"
    ]
    
    # Combine and select 13 unique tags
    all_tags = base_tags + concept_tags + style_tags
    
    # Ensure all tags are under 20 characters
    valid_tags = [tag for tag in all_tags if len(tag) <= 20]
    
    # Remove duplicates and select 13
    unique_tags = list(dict.fromkeys(valid_tags))  # Preserves order while removing duplicates
    
    return unique_tags[:13] if len(unique_tags) >= 13 else unique_tags + ["digital art"]*(13-len(unique_tags))

def generate_etsy_description(concept, titles):
    """Generate a complete Etsy description with emotional hook, art story, download info, decor use, and CTA"""
    
    # Use the first title for consistency
    main_title = titles[0] if titles else f"{concept.title()} Art Print"
    
    description = f"""✨ Transform your space with this {concept} digital art print! ✨

🎨 THE STORY
This beautiful {concept} artwork was created to bring tranquility and natural beauty into your home. Whether you're looking to create a peaceful sanctuary in your bedroom or add a touch of nature to your living space, this print captures the essence of {concept} in stunning detail.

📥 WHAT YOU GET
• High-resolution digital files (300 DPI)
• Multiple sizes included: 8x10, 11x14, 16x20, 18x24
• JPEG format for easy printing
• Instant download - no waiting!
• Print as many times as you want

🏠 PERFECT FOR
• Bedroom wall art
• Living room decor
• Office inspiration
• Nursery art
• Gallery walls
• Housewarming gifts
• Any space needing natural beauty

🖨️ PRINTING TIPS
• Use high-quality photo paper for best results
• Print at your local photo center or at home
• Frame with a mat for a professional look
• No physical item will be shipped

💝 This makes a thoughtful gift for nature lovers, art enthusiasts, or anyone who appreciates beautiful home decor!

📧 Questions? I'm here to help! Message me anytime.

#DigitalDownload #PrintableArt #WallArt #HomeDecor #InstantDownload"""
    
    return description

def generate_pinterest_caption(concept):
    """Generate a Pinterest caption with relevant hashtags"""
    
    caption = f"""Beautiful {concept} art print perfect for your home! 🏠✨

This dreamy digital download adds instant charm to any room. Perfect for bedroom decor, living room walls, or as a thoughtful gift! 

💝 Instant download - print at home or your local photo center
🖼️ Multiple sizes included
🌿 Brings nature indoors

#HomeDecor #WallArt #PrintableArt #DigitalDownload #BedroomDecor #LivingRoomArt #NatureArt #InstantDownload #WallDecor #ArtPrint #HomeDesign #InteriorDesign #BohoDecor #ModernArt #WallArtPrint"""
    
    return caption

def track_analytics_event(event_type, content_id=None, concept_id=None, event_data=None):
    """Helper function to track analytics events"""
    try:
        from models import AnalyticsEvent
        
        # Get client information
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        user_agent = request.environ.get('HTTP_USER_AGENT', '')
        
        # Create analytics event
        event = AnalyticsEvent(
            event_type=event_type,
            content_id=content_id,
            concept_id=concept_id,
            event_data=event_data,
            ip_address=ip_address[:45] if ip_address else None,  # Truncate if too long
            user_agent=user_agent[:500] if user_agent else None  # Truncate if too long
        )
        
        db.session.add(event)
        db.session.commit()
        app.logger.debug(f"Analytics event tracked: {event_type} for content {content_id}")
        
    except Exception as e:
        app.logger.error(f"Error tracking analytics event: {str(e)}")
        # Don't fail the main operation if analytics tracking fails
        db.session.rollback()

@app.route('/')
def index():
    """Display the main form for inputting creative concepts"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Process the form input and generate all content"""
    
    concept = request.form.get('concept', '').strip()
    
    if not concept:
        flash('Please enter a creative concept to generate content.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Generate all content
        midjourney_prompts = generate_midjourney_prompts(concept)
        etsy_titles = generate_etsy_titles(concept)
        etsy_tags = generate_etsy_tags(concept)
        etsy_description = generate_etsy_description(concept, etsy_titles)
        pinterest_caption = generate_pinterest_caption(concept)
        
        # Save to database
        from models import GeneratedContent, Concept
        
        # Check if concept already exists and update usage
        existing_concept = Concept.query.filter_by(text=concept).first()
        if existing_concept:
            existing_concept.usage_count += 1
            existing_concept.last_used = datetime.utcnow()
            concept_id = existing_concept.id
        else:
            new_concept = Concept(text=concept)
            db.session.add(new_concept)
            db.session.flush()  # Get the ID without committing
            concept_id = new_concept.id
        
        # Save generated content
        generated_content = GeneratedContent(
            concept=concept,
            concept_id=concept_id,
            midjourney_prompts=midjourney_prompts,
            etsy_titles=etsy_titles,
            etsy_tags=etsy_tags,
            etsy_description=etsy_description,
            pinterest_caption=pinterest_caption
        )
        
        db.session.add(generated_content)
        db.session.commit()
        
        app.logger.info(f"Saved generated content with ID: {generated_content.id}")
        
        # Track analytics: content generation
        track_analytics_event('generate', 
                            content_id=generated_content.id, 
                            concept_id=concept_id,
                            event_data={
                                'prompt_count': len(midjourney_prompts),
                                'title_count': len(etsy_titles),
                                'tag_count': len(etsy_tags)
                            })
        
        # Generate placeholder image URLs
        placeholder_images = [
            f"https://picsum.photos/400/500?random={i+1}&blur=1" for i in range(3)
        ]
        
        return render_template('results.html',
                             concept=concept,
                             midjourney_prompts=midjourney_prompts,
                             etsy_titles=etsy_titles,
                             etsy_tags=etsy_tags,
                             etsy_description=etsy_description,
                             pinterest_caption=pinterest_caption,
                             placeholder_images=placeholder_images,
                             content_id=generated_content.id)
    
    except Exception as e:
        app.logger.error(f"Error generating content: {str(e)}")
        db.session.rollback()
        flash('An error occurred while generating content. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    """Display a list of all previously generated content"""
    try:
        from models import GeneratedContent
        
        # Get all generated content, ordered by most recent first
        generated_contents = GeneratedContent.query.order_by(
            GeneratedContent.created_at.desc()
        ).limit(50).all()  # Limit to 50 most recent entries
        
        return render_template('history.html', generated_contents=generated_contents)
    
    except Exception as e:
        app.logger.error(f"Error fetching history: {str(e)}")
        flash('Error loading history. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/view/<int:content_id>')
def view_content(content_id):
    """View a specific generated content by ID"""
    try:
        from models import GeneratedContent, AnalyticsEvent, Concept
        
        content = GeneratedContent.query.get_or_404(content_id)
        
        # Track analytics: content view
        track_analytics_event('view', content_id=content_id, concept_id=content.concept_id)
        
        # Update content view metrics
        content.view_count += 1
        content.last_viewed = datetime.utcnow()
        
        # Update concept view metrics if linked
        if content.concept_id:
            concept = Concept.query.get(content.concept_id)
            if concept:
                concept.total_views += 1
        
        db.session.commit()
        
        # Generate placeholder image URLs (same as in generate route)
        placeholder_images = [
            f"https://picsum.photos/400/500?random={content_id+i+1}&blur=1" for i in range(3)
        ]
        
        return render_template('results.html',
                             concept=content.concept,
                             midjourney_prompts=content.midjourney_prompts,
                             etsy_titles=content.etsy_titles,
                             etsy_tags=content.etsy_tags,
                             etsy_description=content.etsy_description,
                             pinterest_caption=content.pinterest_caption,
                             placeholder_images=placeholder_images,
                             content_id=content.id,
                             created_at=content.created_at,
                             is_viewing_saved=True,
                             view_count=content.view_count,
                             copy_count=content.copy_count)
    
    except Exception as e:
        app.logger.error(f"Error viewing content {content_id}: {str(e)}")
        flash('Content not found or error occurred.', 'error')
        return redirect(url_for('history'))

@app.route('/analytics')
def analytics_dashboard():
    """Display comprehensive analytics dashboard"""
    try:
        from models import GeneratedContent, Concept, AnalyticsEvent
        from sqlalchemy import func
        
        # Get basic statistics
        total_generations = GeneratedContent.query.count()
        unique_concepts = Concept.query.count()
        total_views = db.session.query(func.sum(GeneratedContent.view_count)).scalar() or 0
        total_copies = db.session.query(func.sum(GeneratedContent.copy_count)).scalar() or 0
        
        # Get top performing content
        top_viewed = GeneratedContent.query.order_by(
            GeneratedContent.view_count.desc()
        ).limit(10).all()
        
        top_copied = GeneratedContent.query.order_by(
            GeneratedContent.copy_count.desc()
        ).limit(10).all()
        
        # Get popular concepts
        popular_concepts = Concept.query.order_by(
            Concept.usage_count.desc()
        ).limit(10).all()
        
        # Get recent analytics events (last 100)
        recent_events = AnalyticsEvent.query.order_by(
            AnalyticsEvent.created_at.desc()
        ).limit(100).all()
        
        # Event type summary
        event_summary = db.session.query(
            AnalyticsEvent.event_type,
            func.count(AnalyticsEvent.id).label('count')
        ).group_by(AnalyticsEvent.event_type).all()
        
        return render_template('analytics.html',
                             total_generations=total_generations,
                             unique_concepts=unique_concepts,
                             total_views=total_views,
                             total_copies=total_copies,
                             top_viewed=top_viewed,
                             top_copied=top_copied,
                             popular_concepts=popular_concepts,
                             recent_events=recent_events,
                             event_summary=event_summary)
    
    except Exception as e:
        app.logger.error(f"Error loading analytics dashboard: {str(e)}")
        flash('Error loading analytics dashboard. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/track-copy', methods=['POST'])
def track_copy_event():
    """API endpoint to track copy events from frontend"""
    try:
        from models import GeneratedContent, Concept
        
        data = request.get_json()
        content_id = data.get('content_id')
        copy_type = data.get('copy_type', 'general')  # 'prompt', 'title', 'tags', etc.
        
        if content_id:
            # Update content copy metrics
            content = GeneratedContent.query.get(content_id)
            if content:
                content.copy_count += 1
                content.last_copied = datetime.utcnow()
                
                # Update concept copy metrics if linked
                if content.concept_id:
                    concept = Concept.query.get(content.concept_id)
                    if concept:
                        concept.total_copies += 1
                
                db.session.commit()
                
                # Track analytics event
                track_analytics_event('copy', 
                                    content_id=content_id, 
                                    concept_id=content.concept_id,
                                    event_data={'copy_type': copy_type})
        
        return jsonify({'status': 'success'})
    
    except Exception as e:
        app.logger.error(f"Error tracking copy event: {str(e)}")
        return jsonify({'error': 'Failed to track copy event'}), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint to get comprehensive usage statistics"""
    try:
        from models import GeneratedContent, Concept, AnalyticsEvent
        from sqlalchemy import func, desc
        
        # Basic counts
        total_generations = GeneratedContent.query.count()
        unique_concepts = Concept.query.count()
        total_views = db.session.query(func.sum(GeneratedContent.view_count)).scalar() or 0
        total_copies = db.session.query(func.sum(GeneratedContent.copy_count)).scalar() or 0
        
        # Most popular concepts by usage
        most_popular_concepts = Concept.query.order_by(
            Concept.usage_count.desc()
        ).limit(5).all()
        
        # Most viewed content
        most_viewed_content = GeneratedContent.query.order_by(
            GeneratedContent.view_count.desc()
        ).limit(5).all()
        
        # Most copied content
        most_copied_content = GeneratedContent.query.order_by(
            GeneratedContent.copy_count.desc()
        ).limit(5).all()
        
        # Recent activity
        recent_activity = GeneratedContent.query.order_by(
            GeneratedContent.created_at.desc()
        ).limit(10).all()
        
        # Analytics events summary (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_events = db.session.query(
            AnalyticsEvent.event_type,
            func.count(AnalyticsEvent.id).label('count')
        ).filter(
            AnalyticsEvent.created_at >= thirty_days_ago
        ).group_by(AnalyticsEvent.event_type).all()
        
        return jsonify({
            'overview': {
                'total_generations': total_generations,
                'unique_concepts': unique_concepts,
                'total_views': total_views,
                'total_copies': total_copies
            },
            'popular_concepts': [
                {
                    'text': c.text,
                    'usage_count': c.usage_count,
                    'total_views': c.total_views,
                    'total_copies': c.total_copies
                } 
                for c in most_popular_concepts
            ],
            'top_performing_content': {
                'most_viewed': [
                    {
                        'id': c.id,
                        'concept': c.concept,
                        'view_count': c.view_count,
                        'copy_count': c.copy_count,
                        'created_at': c.created_at.isoformat()
                    }
                    for c in most_viewed_content
                ],
                'most_copied': [
                    {
                        'id': c.id,
                        'concept': c.concept,
                        'view_count': c.view_count,
                        'copy_count': c.copy_count,
                        'created_at': c.created_at.isoformat()
                    }
                    for c in most_copied_content
                ]
            },
            'recent_activity': [
                {
                    'id': r.id,
                    'concept': r.concept,
                    'view_count': r.view_count,
                    'copy_count': r.copy_count,
                    'created_at': r.created_at.isoformat()
                }
                for r in recent_activity
            ],
            'event_summary': {
                event_type: count for event_type, count in recent_events
            }
        })
    
    except Exception as e:
        app.logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500

# Database initialization
with app.app_context():
    # Import models after app and db are configured
    import models
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
