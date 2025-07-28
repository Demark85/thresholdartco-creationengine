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
- **Database**: PostgreSQL database for persistent storage
- **Models**: SQLAlchemy ORM with GeneratedContent and Concept models
- **Data Persistence**: All generated content automatically saved with timestamps
- **Analytics**: Concept usage tracking and statistics
- **Session Data**: In-memory session storage via Flask sessions
- **Static Assets**: Served via Flask's static file handling

## Key Components

### Core Application Logic
- **main.py**: Primary Flask application with route handlers, database integration, and prompt generation logic
- **models.py**: SQLAlchemy database models for GeneratedContent and Concept entities
- **Prompt Generator**: Algorithm that combines creative concepts with artistic styles, lighting conditions, and technical parameters to create MidJourney prompts

### Frontend Components
- **index.html**: Main input form for creative concepts with navigation to history
- **results.html**: Display page for generated MidJourney prompts with copy-to-clipboard functionality
- **history.html**: List view of all previously generated content with statistics
- **script.js**: Client-side JavaScript for clipboard operations and UI feedback

### Database Schema
- **GeneratedContent**: Stores all generated prompts, titles, tags, descriptions, and Pinterest captions
- **Concept**: Tracks unique creative concepts with usage statistics and timestamps

### Styling and UI
- **Bootstrap 5**: Responsive grid system and component styling
- **Dark Theme**: Consistent dark color scheme throughout the application
- **Interactive Elements**: Copy buttons with visual feedback and toast notifications

## Data Flow

1. **User Input**: User enters creative concept via textarea on index page
2. **Form Submission**: POST request to `/generate` endpoint with concept data
3. **Prompt Generation**: Backend processes concept through generation algorithm
4. **Content Creation**: Multiple MidJourney prompts created with varied styles and parameters
5. **Database Storage**: All generated content automatically saved to PostgreSQL database
6. **Concept Tracking**: Creative concepts tracked for usage analytics and statistics
7. **Results Display**: Generated prompts displayed on results page with copy functionality
8. **Content History**: Users can access previously generated content via history page
9. **Individual Viewing**: Each generated content item can be viewed by unique ID
10. **User Interaction**: Users can copy individual prompts to clipboard for use in MidJourney

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN
- **Bootstrap Icons**: Icon library loaded via CDN
- **CDN Strategy**: All external assets loaded from CDNs for faster loading

### Python Dependencies
- **Flask**: Web framework for Python
- **Flask-SQLAlchemy**: ORM for database interactions
- **psycopg2-binary**: PostgreSQL adapter for Python
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

## Recent Changes (July 28, 2025)

### Database Integration Implementation
- **PostgreSQL Integration**: Added full database support with Flask-SQLAlchemy
- **Data Models**: Created GeneratedContent and Concept models with proper relationships
- **Content Persistence**: All generated prompts, titles, tags, and descriptions now automatically saved
- **History Functionality**: Added `/history` route to view all past generations
- **Individual Content Viewing**: Added `/view/<id>` route for accessing specific saved content
- **Usage Analytics**: Concept tracking with usage statistics and timestamps
- **Navigation Enhancement**: Added history links throughout the application
- **API Endpoint**: Created `/api/stats` for retrieving usage statistics

### Analytics Tracking System Implementation
- **Performance Metrics**: Added view count and copy count tracking for all generated content
- **Analytics Events**: Created AnalyticsEvent model to log all user interactions
- **Real-time Tracking**: JavaScript integration for copy event tracking via API
- **Analytics Dashboard**: Comprehensive `/analytics` route with performance insights
- **Content Performance**: View and copy metrics displayed on content pages
- **Popular Content Identification**: Analytics for most viewed and most copied content
- **Concept Performance**: Usage, view, and copy analytics for creative concepts
- **Event Logging**: Detailed tracking of generate, view, and copy activities

## Future Enhancement Opportunities

- User authentication and personalized prompt history
- Enhanced prompt generation algorithms with machine learning
- Image preview integration with MidJourney API
- Bulk export functionality for generated content
- Advanced search and filtering in history
- User preferences and customizable generation settings