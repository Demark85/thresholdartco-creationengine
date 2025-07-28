import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
import random

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

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
                             placeholder_images=placeholder_images)
    
    except Exception as e:
        app.logger.error(f"Error generating content: {str(e)}")
        flash('An error occurred while generating content. Please try again.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
