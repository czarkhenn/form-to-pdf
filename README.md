# Form to PDF Generator

A Django web application that allows users to fill out a form and generate a PDF document from the submitted data. The application uses WeasyPrint for PDF generation and provides a clean web interface for form input and preview.

## Features

- **Dynamic Form Input**: User-friendly web form for data collection
- **Preview Functionality**: HTML preview before PDF generation
- **PDF Generation**: High-quality PDF creation using WeasyPrint
- **Docker Support**: Easy deployment with Docker and docker-compose

## Dependencies
- **Docker**

### Python Dependencies
- **Django**
- **WeasyPrint** 

## Setup Instructions


1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd form-to-pdf
   ```

2. **Build and start the application:**
   ```bash
   make build
   make start
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8000`

4. **View logs (if needed):**
   ```bash
   make logs
   ```

5. **Stop the application:**
   ```bash
   make stop
   ```
## Usage

1. **Fill out the form**: Navigate to the main page and complete the user data form
2. **Preview your data**: After submission, review the HTML preview of your information
3. **Generate PDF**: Click the PDF generation button to create and download your document


## Development Commands

- `make build`: Build Docker containers
- `make start`: Start the application
- `make stop`: Stop the application
- `make restart`: Restart the application
- `make logs`: View application logs
- `make test`: Run tests
- `make makemigrations`: Create database migrations
- `make migrate`: Apply database migrations

## Configuration

The application uses Django's settings system. For local development:
- `core/settings/local.py`: Development settings with debug enabled
- `core/settings/base.py`: Base configuration shared across environments
