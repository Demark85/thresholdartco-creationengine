# ThresholdArtCo Creation Engine

## Overview

This is a Flask-based web application designed to help artists and creators generate MidJourney prompts and Etsy listings from creative concepts. The application takes user input describing a creative concept and transforms it into multiple MidJourney prompts with different artistic styles, lighting, and technical parameters.

**Current Status**: Fully functional prototype deployed and tested successfully (July 28, 2025)

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating engine)
- **CSS Framework**: Bootstrap 5 with dark theme variant
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JavaScript for clipboard functionality
- **Theme**: Dark theme with purple/primary color scheme

### Backend Architecture
- **Framework**: Flask (lightweight Python web framework)
- **Session Management**: Flask's built-in session handling with secret key
- **Logging**: Python's standard logging module configured for DEBUG level
- **Environment Configuration**: Environment variables for sensitive data

### Data Storage Solutions
- **Database**: PostgreSQL with Flask-SQLAlchemy ORM
- **Models**: GeneratedContent and Concept models with proper foreign key relationships
- **Features**: Content history, concept tracking, usage analytics
- **Session Data**: In-memory session storage via Flask sessions
- **Static Assets**: Served via Flask's static file handling

## Key Components

### Core Application Logic
- **main.py**: Primary Flask application with route handlers, prompt generation logic, and database integration
- **models.py**: SQLAlchemy models for GeneratedContent and Concept with proper relationships
- **Prompt Generator**: Algorithm that combines creative concepts with artistic styles, lighting conditions, and technical parameters to create MidJourney prompts

### Frontend Components
- **index.html**: Main input form for creative concepts with navigation to history
- **results.html**: Display page for generated MidJourney prompts with copy-to-clipboard functionality
- **history.html**: List view of all previously generated content with statistics
- **script.js**: Client-side JavaScript for clipboard operations and UI feedback

### Database Components
- **GeneratedContent Model**: Stores all generated prompts, titles, tags, descriptions, and captions
- **Concept Model**: Tracks unique creative concepts with usage statistics and timestamps
- **Relationships**: Foreign key linking content to concepts for analytics

### Styling and UI
- **Bootstrap 5**: Responsive grid system and component styling
- **Dark Theme**: Consistent dark color scheme throughout the application
- **Interactive Elements**: Copy buttons with visual feedback and toast notifications
- **Navigation**: Seamless movement between creation, viewing, and history pages

## Data Flow

1. **User Input**: User enters creative concept via textarea on index page
2. **Form Submission**: POST request to `/generate` endpoint with concept data
3. **Prompt Generation**: Backend processes concept through generation algorithm
4. **Content Creation**: Multiple MidJourney prompts created with varied styles and parameters
5. **Results Display**: Generated prompts displayed on results page with copy functionality
6. **User Interaction**: Users can copy individual prompts to clipboard for use in MidJourney

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN
- **Bootstrap Icons**: Icon library loaded via CDN
- **CDN Strategy**: All external assets loaded from CDNs for faster loading

### Python Dependencies
- **Flask**: Web framework for Python
- **Standard Library**: Uses built-in modules (os, logging, random) for core functionality

### Browser APIs
- **Clipboard API**: Modern clipboard access for copy functionality
- **Fallback Support**: Graceful degradation for older browsers

## Deployment Strategy

### Environment Configuration
- **Secret Key**: Configurable via `SESSION_SECRET` environment variable
- **Development Mode**: Default secret key provided for development
- **Logging**: Debug level logging enabled for development

### Static Asset Handling
- **Flask Static**: Built-in static file serving for JavaScript and other assets
- **CDN Dependencies**: External CSS and icon libraries loaded from CDNs

### Scalability Considerations
- **Stateless Design**: No persistent data storage required
- **Session-based**: Minimal server-side state management
- **Simple Architecture**: Easy to containerize and deploy to various platforms

### Security Features
- **Session Security**: Secret key for session management
- **XSS Protection**: Jinja2 template auto-escaping enabled
- **Environment Variables**: Sensitive configuration externalized

## Future Enhancement Opportunities

- Database integration for saving generated prompts
- User authentication and prompt history
- Etsy listing generation (referenced in templates but not implemented)
- API endpoints for programmatic access
- Enhanced prompt generation algorithms
- Image preview integration with MidJourney API