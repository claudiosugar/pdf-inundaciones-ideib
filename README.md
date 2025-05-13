# PDF Inundaciones IDEIB

A web application that automates the process of retrieving flood risk information for properties in the Balearic Islands (Spain) using cadastral references. The application interacts with the IDEIB (Infraestructura de Dades Espacials de les Illes Balears) website to generate flood risk maps and reports.

## Features

- Web interface for entering cadastral references
- Automated browser interaction with the IDEIB website
- Retrieval of flood risk information for specific properties
- PDF generation of flood risk maps
- Docker support for easy deployment

## How It Works

The application uses Playwright to automate browser interactions with the IDEIB website. When a user submits a cadastral reference:

1. The application launches a browser and navigates to the IDEIB website
2. It interacts with the website to:
   - Close initial modals
   - Add flood risk data layers to the map
   - Search for the specified cadastral reference
   - Zoom in to the property
   - Generate a PDF of the flood risk information

## Requirements

- Python 3.6+
- Flask 2.3.3
- Playwright 1.41.0
- Gunicorn 21.2.0 (for production deployment)

## Installation

### Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/claudiosugar/pdf-inundaciones-ideib.git
   cd pdf-inundaciones-ideib
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   python install_playwright.py
   ```

### Docker Installation

1. Build the Docker image:
   ```
   docker build -t pdf-inundaciones-ideib .
   ```

2. Run the container:
   ```
   docker run -p 8080:8080 pdf-inundaciones-ideib
   ```

## Usage

1. Start the application:
   ```
   python pdf-inundaciones-ideib.py
   ```
   
   Or with Gunicorn (for production):
   ```
   gunicorn --bind 0.0.0.0:8080 --timeout 600 pdf-inundaciones-ideib:app
   ```

2. Open a web browser and navigate to `http://localhost:8080`

3. Enter a cadastral reference in the form and submit

4. The application will generate a PDF with flood risk information for the specified property

## API Endpoints

- `GET /`: Main page with the form
- `POST /get_pdf`: Endpoint to generate and download a PDF for a given cadastral reference
- `GET /<referencia_catastral>`: Direct URL access to generate a PDF for a specific cadastral reference

## Deployment

The application includes a Dockerfile and is configured to run on platforms like Heroku with the included Procfile.

## License

[Specify your license here]

## Author

[Your name or organization]
