from playwright.sync_api import sync_playwright
import time
import logging
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
import os
from datetime import datetime
import zipfile # Added for zipping files
import tempfile # Added for temporary zip file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define years to screenshot (Reduced for testing)
years_to_screenshot = [1956, 1984, 1989, 2001, 2002, 2006, 2008, 2010, 2012, 2015, 2018, 2021, 2023]

app = Flask(__name__)

# Create a directory for storing screenshots if it doesn't exist
SCREENSHOT_DIR = "screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

def maximize_window(page):
    """Maximize the browser window"""
    try:
        logger.info("Maximizing browser window...")
        # We now handle this in browser initialization with viewport
        logger.info("Browser window maximized successfully")
    except Exception as e:
        logger.error(f"Failed to maximize window: {str(e)}")

def close_initial_modal(page):
    """Close the initial modal that appears when the page loads"""
    try:
        logger.info("Closing initial modal...")
        ok_button = page.locator('div.jimu-btn.jimu-float-trailing.enable-btn[data-dojo-attach-point="okNode"]')
        ok_button.wait_for(state="visible")
        ok_button.click()
        time.sleep(0.5)  # Reduced wait time
        logger.info("Initial modal closed successfully")
    except Exception as e:
        logger.error(f"Failed to close initial modal: {str(e)}")

def click_locate_icon(page):
    """Click the locate icon to open the search panel"""
    try:
        logger.info("Clicking locate icon...")
        img = page.locator('img.icon[src*="/visor/widgets/ideibLocate/images/icon.png"]')
        img.wait_for(state="visible")
        parent = img.locator('xpath=..')
        parent.click()
        time.sleep(1)  # Reduced wait
        logger.info("Locate icon clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click locate icon: {str(e)}")

def click_cadastre_tab(page):
    """Click the Cadastre tab in the search panel"""
    try:
        logger.info("Clicking Cadastre tab...")
        cadastre_tab = page.locator('div.tab.jimu-vcenter-text[label="Cadastre"]')
        cadastre_tab.wait_for(state="visible")
        cadastre_tab.click()
        time.sleep(1)  # Reduced wait
        logger.info("Cadastre tab clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click Cadastre tab: {str(e)}")

def enter_cadastral_reference(page, referencia_catastral):
    """Enter the cadastral reference and click search"""
    try:
        logger.info(f"Entering cadastral reference: {referencia_catastral}")
        input_field = page.locator('input#RC[name="search"]')
        input_field.wait_for(state="visible")
        input_field.fill(referencia_catastral)
        
        logger.info("Clicking search button...")
        search_button = page.locator('div.locate-btn.btn-addressLocate[data-dojo-attach-point="btnRefCat"]')
        search_button.wait_for(state="visible")
        search_button.click()
        
        time.sleep(3)  # Wait for results to load
        logger.info("Search completed successfully")
    except Exception as e:
        logger.error(f"Failed to enter cadastral reference: {str(e)}")

def close_left_column(page):
    """Close/minimize the left column"""
    try:
        left_column = page.locator('.bar.max')
        if left_column.is_visible():
            time.sleep(0.3)  # Reduced wait
            left_column.click()  # First click
            time.sleep(0.3)  # Reduced wait
            left_column.click()  # Second click
            logger.info("Left column closed/minimized.")
    except Exception as e:
        logger.error(f"Failed to close/minimize left column: {str(e)}")

def close_cerca_avancada(page):
    """Close the cerca avançada panel"""
    try:
        logger.info("Closing cerca avançada panel...")
        close_button = page.locator('div.close-icon.jimu-float-trailing[data-dojo-attach-point="closeNode"]')
        close_button.wait_for(state="visible")
        close_button.click()
        time.sleep(1)  # Wait for panel to close
        logger.info("Cerca avançada panel closed successfully")
    except Exception as e:
        logger.error(f"Failed to close cerca avançada panel: {str(e)}")

def hide_ui_elements(page):
    """Hide various UI elements to clean up the view"""
    stuff_ids = [
        'themes_IDEIBTheme_widgets_AnchorBarController_Widget_20', 'widgets_ideibSearch_Widget_22',
        'themes_IDEIBTheme_widgets_Header_Widget_21', 'widgets_ZoomSlider_Widget_24',
        'widgets_ideibStreetView', 'widgets_MyLocation_Widget_26',
        'widgets_ideibHomeButton_Widget_25', 'widgets_ideibZoomExtent',
        'widgets_ZoomSlider_Widget_24', 'dijit__WidgetBase_2', 'esri_dijit_OverviewMap_1'
    ]
    
    for element_id in stuff_ids:
        try:
            element = page.locator(f'#{element_id}')
            if element.is_visible():
                page.evaluate(f"document.getElementById('{element_id}').style.display = 'none';")
                logger.info(f'Hidden: {element_id}')
        except Exception as e:
            logger.error(f'Failed to hide {element_id}: {str(e)}')

def zoom_in_three_times(page):
    """Zoom in three times"""
    try:
        logger.info("Zooming in three times...")
        zoom_in_button = page.locator('div.zoom.zoom-in.jimu-corner-top.firstFocusNode[data-dojo-attach-point="btnZoomIn"]')
        zoom_in_button.wait_for(state="visible")
        
        for i in range(3):
            zoom_in_button.click()
            time.sleep(0.5)  # Reduced wait
            logger.info(f"Zoomed in {i+1}/3 times")
    except Exception as e:
        logger.error(f"Failed to zoom in: {str(e)}")

def take_screenshot(page, referencia_catastral, year=None):
    """Take a screenshot of the current view"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Ensure screenshot directory exists (might be redundant but safe)
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
            
        if year:
            # Use only the base filename for the zip archive, store in SCREENSHOT_DIR
            base_filename = f"foto_{referencia_catastral}_{year}_{timestamp}.png"
            screenshot_path = os.path.join(SCREENSHOT_DIR, base_filename)
        else:
            base_filename = f"foto_{referencia_catastral}_{timestamp}.png"
            screenshot_path = os.path.join(SCREENSHOT_DIR, base_filename)
            
        page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved as {screenshot_path}")
        return os.path.normpath(screenshot_path) # Return the full path
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None

def select_historical_photos(page):
    """Click on the historical photos option"""
    try:
        logger.info("Selecting historical photos option...")
        historical_photos = page.locator('img[alt="Fotografies històriques de totes les illes"]')
        historical_photos.wait_for(state="visible")
        historical_photos.click()
        time.sleep(2)  # Wait for the options to load
        logger.info("Historical photos option selected successfully")
    except Exception as e:
        logger.error(f"Failed to select historical photos: {str(e)}")

def select_year_and_screenshot(page, year, referencia_catastral):
    """Select a specific year and take a screenshot"""
    try:
        logger.info(f"Selecting year {year}...")
        year_element = page.locator(f'span:text("{year}")')
        year_element.wait_for(state="visible")
        year_element.click()
        time.sleep(5)  # Wait for the image to load
        screenshot_path = take_screenshot(page, referencia_catastral, year)
        logger.info(f"Year {year} selected and screenshot taken successfully")
        return screenshot_path
    except Exception as e:
        logger.error(f"Failed to select year {year}: {str(e)}")
        return None

def get_aerial_photos(referencia_catastral):
    """
    Navigate to the IDEIB website and retrieve aerial photos for the given cadastral reference
    Returns a list of screenshot paths
    """
    screenshot_paths = []
    try:
        # Check if running on Fly.io or similar cloud environment
        is_production = os.environ.get('FLY_APP_NAME') is not None

        with sync_playwright() as p:
            # Launch browser - use headless True in production, False in local testing
            launch_options = {
                "headless": is_production, 
                # Add args for better containerized browser support and memory optimization
                "args": [
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                    "--single-process",
                    "--disable-extensions",
                    "--disable-popup-blocking"
                ] if is_production else []
            }
            
            # Add timeout for page operations
            browser = p.chromium.launch(**launch_options)
            
            # Increase timeout to 60 seconds for all operations
            # Set a viewport size that's not too large to reduce memory usage
            page = browser.new_page(
                viewport={"width": 1280, "height": 800}
            )
            page.set_default_timeout(60000)  # 60 seconds
            
            # Navigate to the IDEIB website with longer timeout
            logger.info("Navigating to IDEIB website...")
            page.goto("https://ideib.caib.es/visor/", timeout=90000)  # 90 seconds timeout for initial load
            page.wait_for_load_state("networkidle", timeout=90000)
            
            # Execute all steps in sequence
            # Skip maximize_window as we already set viewport size
            logger.info("Setting up the view...")
            
            # Reduce wait times between actions
            close_initial_modal(page)
            close_left_column(page)
            click_locate_icon(page)
            click_cadastre_tab(page)
            enter_cadastral_reference(page, referencia_catastral)
            close_cerca_avancada(page)
            zoom_in_three_times(page)
            hide_ui_elements(page)
            
            # Process years in batches to reduce memory pressure
            logger.info(f"Taking screenshots for years: {years_to_screenshot}")
            select_historical_photos(page)
            
            # Process years in batches to reduce memory pressure
            batch_size = 4
            for i in range(0, len(years_to_screenshot), batch_size):
                batch = years_to_screenshot[i:i+batch_size]
                logger.info(f"Processing batch of years: {batch}")
                
                for year in batch:
                    screenshot_path = select_year_and_screenshot(page, year, referencia_catastral)
                    if screenshot_path:
                        screenshot_paths.append(screenshot_path)
                
                # Close and reopen contexts between batches to free memory
                if i + batch_size < len(years_to_screenshot):
                    logger.info("Freeing memory between batches...")
                    # Do a simple browser operation to flush memory
                    page.evaluate("() => { try { window.gc && window.gc(); } catch(e) {} }")
            
            browser.close()
            
    except Exception as e:
        logger.error(f"Error retrieving aerial photos: {str(e)}")
        # Ensure partial results aren't returned on error
        return [] # Return empty list on failure
    
    return screenshot_paths # Returns list of full paths

@app.route('/')
def index():
    return render_template('index.html')

# Add a route to explicitly handle favicon requests and avoid triggering photo generation
@app.route('/favicon.ico')
def favicon():
    # Return an empty 204 No Content response, or 404 Not Found
    # return '', 204
    return jsonify({'error': 'Not Found'}), 404 

@app.route('/get_photos', methods=['POST'])
def get_photos():
    referencia_catastral = request.form.get('referencia_catastral')
    if not referencia_catastral:
        # Maybe render index with an error message instead of JSON?
        return jsonify({'error': 'Please provide a cadastral reference'}), 400
    
    return process_and_zip_photos(referencia_catastral)

# New route to fetch photos directly via URL path
@app.route('/<string:referencia_catastral>', methods=['GET'])
def get_photos_by_url(referencia_catastral):
    logger.info(f"Received request via URL path for: {referencia_catastral}")
    if not referencia_catastral:
        return jsonify({'error': 'Please provide a cadastral reference in the URL path'}), 400
    
    return process_and_zip_photos(referencia_catastral)

def process_and_zip_photos(referencia_catastral):
    """Helper function to get photos, zip them, and return for download."""
    try:
        screenshot_paths = get_aerial_photos(referencia_catastral)
        if not screenshot_paths:
            return jsonify({'error': 'No screenshots were generated, check the reference or logs'}), 500
        
        # Create a temporary zip file
        # Using tempfile ensures it's created securely and OS-independently
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip", prefix=f"fotos_{referencia_catastral}_")
        zip_path = temp_zip.name
        logger.info(f"Creating zip archive at: {zip_path}")
        
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in screenshot_paths:
                # Add file to zip, using only the base filename inside the archive
                zipf.write(file_path, os.path.basename(file_path))
        
        temp_zip.close() # Close the file handle
        
        # Schedule the zip file for deletion after the request is sent
        @after_this_request
        def cleanup(response):
            try:
                os.remove(zip_path)
                logger.info(f"Successfully removed temporary zip file: {zip_path}")
                # Optionally remove the original screenshots too
                # for file_path in screenshot_paths:
                #     os.remove(file_path)
                # logger.info(f"Successfully removed original screenshot files.")
            except Exception as error:
                logger.error(f"Error removing temporary zip file {zip_path}: {error}")
            return response
            
        # Send the zip file as an attachment
        zip_download_name = f"fotos_{referencia_catastral}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        logger.info(f"Sending zip file {zip_path} as attachment: {zip_download_name}")
        return send_file(zip_path, as_attachment=True, download_name=zip_download_name)

    except Exception as e:
        logger.error(f"Error processing request for {referencia_catastral}: {str(e)}")
        # Clean up zip file if it exists and an error occurred before sending
        if 'zip_path' in locals() and os.path.exists(zip_path):
             try:
                 os.remove(zip_path)
                 logger.info(f"Cleaned up zip file {zip_path} after error.")
             except Exception as cleanup_error:
                 logger.error(f"Error cleaning up zip file {zip_path} after error: {cleanup_error}")
        return jsonify({'error': str(e)}), 500

# Removed the /screenshots/<path:filename> route as it's no longer needed
# @app.route('/screenshots/<path:filename>')
# def serve_screenshot(filename):
#     return send_file(os.path.join(SCREENSHOT_DIR, filename))

# Uncomment and modify for deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)