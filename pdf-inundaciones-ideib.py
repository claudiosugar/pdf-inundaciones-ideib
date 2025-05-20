from playwright.sync_api import sync_playwright
import time
import logging
from flask import Flask, render_template, request, send_file, jsonify, after_this_request
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def maximize_window(page):
    """Maximize the browser window"""
    try:
        logger.info("Maximizing browser window...")
        logger.info("Browser window maximized successfully")
    except Exception as e:
        logger.error(f"Failed to maximize window: {str(e)}")

def close_initial_modal(page):
    """Close the initial modal that appears when the page loads"""
    try:
        logger.info("Waiting for the initial modal to appear...")
        ok_button = page.locator('div.jimu-btn.jimu-float-trailing.enable-btn[data-dojo-attach-point="okNode"]')
        time.sleep(5)
        ok_button.wait_for(state="visible")  # Wait for the button to be visible
        logger.info("Closing initial modal...")
        ok_button.click()
        time.sleep(2)  # Reduced wait time
        logger.info("Initial modal closed successfully")
    except Exception as e:
        logger.error(f"Failed to close initial modal: {str(e)}")

def click_afegir_dades(page):
    """Click the afegir dades button"""
    try:
        logger.info("Clicking afegir dades button...")
        afegir_dades_button = page.locator('div[data-dojo-attach-point="btnAddData"].layerList-btn')
        afegir_dades_button.wait_for(state="visible")
        afegir_dades_button.click()
        logger.info("Afegir dades button clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click afegir dades button: {str(e)}")

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

def input_inundacio_search(page):
    """Input 'inund' into the search box and click the search button"""
    try:
        logger.info("Entering 'inund' into the search box...")
        search_input = page.locator('input.search-textbox[data-dojo-attach-point="searchTextBox"]')
        search_input.wait_for(state="visible")
        search_input.fill("inund")  # Input the text "inund"

        logger.info("Clicking the search button...")
        search_button = page.locator('button.btn.btn-confirm[data-dojo-attach-point="searchButton"]')
        search_button.wait_for(state="visible")
        search_button.click()  # Click the search button

        time.sleep(3)  # Wait for results to load
        logger.info("Search completed successfully")
    except Exception as e:
        logger.error(f"Failed to input inundacio search: {str(e)}")


def add_layer_risc_inundacio(page):
    """Click the 'Afegir' button for the Risc Inundació layer"""
    try:
        logger.info("Clicking the 'Afegir' button for Risc Inundació...")
        # Locate the button based on the text in the info div and the title of the layer
        item_card_locator = page.locator('div.item-card-inner:has(h3.title:text("Xarxa Hidrogràfica i Risc Inundació de les Illes Balears"))')
        add_button = item_card_locator.locator('[data-dojo-attach-point="addButton"]')
        add_button.wait_for(state="visible")  # Wait for the button to be visible
        add_button.click()  # Click the 'Afegir' button
        logger.info("'Afegir' button for Risc Inundació clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click 'Afegir' button for Risc Inundació: {str(e)}")

def close_afegir_dades(page):
    """Close the afegir dades"""
    try:
        logger.info("Closing afegir dades...")
        close_button = page.locator('div.close-btn.jimu-vcenter[data-dojo-attach-point="closeNode"]')
        close_button.wait_for(state="visible")
        close_button.click()  # Click the close button
        logger.info("Afegir dades closed successfully")
    except Exception as e:
        logger.error(f"Failed to close afegir dades: {str(e)}")

def zoom_in_twice(page):
    """Zoom in two times"""
    try:
        logger.info("Zooming in two times...")
        zoom_in_button = page.locator('div.zoom.zoom-in.jimu-corner-top.firstFocusNode[data-dojo-attach-point="btnZoomIn"]')
        zoom_in_button.wait_for(state="visible")
        
        for i in range(2):
            zoom_in_button.click()
            time.sleep(0.5)  # Reduced wait
            logger.info(f"Zoomed in {i+1}/2 times")
    except Exception as e:
        logger.error(f"Failed to zoom in: {str(e)}")

def click_print_icon(page):
    """Click the print icon to open the print panel"""
    try:
        logger.info("Clicking print icon...")
        img = page.locator('img.icon[src*="/visor/widgets/ideibPrint/images/icon.png"]')
        img.wait_for(state="visible")
        parent = img.locator('xpath=..')
        parent.click()
        time.sleep(1)  # Reduced wait
        logger.info("Locate icon clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click locate icon: {str(e)}")

def click_imprimir(page):
    """Click imprimir"""
    try:
        logger.info("Clicking imprimir...")
        print_button = page.locator('[data-dojo-attach-point="printButtonDijit"]')
        print_button.wait_for(state="visible")
        print_button.click()
        time.sleep(1)  # Reduced wait
        logger.info("Imprimir clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click imprimir: {str(e)}")

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

def click_pdf(page):
    """Click on the printed pdf and get its URL"""
    time.sleep(5)
    try:
        logger.info("Clicking on the pdf...")
        mapa_ideib = page.locator(':text("Mapa IDEIB")')
        mapa_ideib.wait_for(state="visible", timeout=180000)  # Increased timeout to 60 seconds
        
        # Set up download listener before clicking
        with page.expect_download() as download_info:
            mapa_ideib.click()
            time.sleep(1)  # Wait for panel to close
            logger.info("Mapa IDEIB clicked")
            
            # Wait for download to start
            download = download_info.value
            logger.info(f"Download started: {download.suggested_filename}")
            
            # Define the download path
            download_dir = os.path.join(os.getcwd(), 'downloads')
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
                
            # Generate a unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            original_filename = download.suggested_filename
            # Sanitize filename to prevent issues
            safe_filename = "".join([c for c in original_filename if c.isalpha() or c.isdigit() or c in (' ', '.', '_')]).rstrip()
            if not safe_filename.lower().endswith('.pdf'):
                safe_filename += '.pdf'
            
            pdf_filename = f'flood_area_{timestamp}_{safe_filename}'
            pdf_path = os.path.join(download_dir, pdf_filename)

            # Save the downloaded file
            download.save_as(pdf_path)
            logger.info(f"PDF downloaded successfully to {pdf_path}")
            return pdf_path
            
    except Exception as e:
        logger.error(f"Failed to click mapa IDEIB: {str(e)}")
        return None

def next_tab(page):
    """Go to next tab"""
    try:
        logger.info("Switching to next tab...")
        # Wait for the new tab to be created
        page.wait_for_timeout(5000)  # Increased wait time to 5 seconds
        # Get all pages
        pages = page.context.pages
        # Switch to the last opened page (the new tab)
        new_page = pages[-1]
        new_page.wait_for_load_state('networkidle', timeout=60000)  # Increased timeout to 60 seconds
        logger.info(f"Successfully switched to new tab. URL: {new_page.url}")
        return new_page
    except Exception as e:
        logger.error(f"Failed to switch to next tab: {str(e)}")
        return None

def click_download_button(page):
    """Click the download button in the PDF viewer"""
    try:
        logger.info("Waiting for PDF viewer to load...")
        # Wait longer for the PDF to load
        page.wait_for_timeout(10000)  # Wait 10 seconds
        
        # Wait for the page to be fully loaded
        page.wait_for_load_state('networkidle', timeout=60000)  # Increased timeout to 60 seconds
        
        # Get the viewport size
        viewport = page.viewport_size
        if not viewport:
            raise Exception("Could not get viewport size")
            
        # Take a screenshot first to help with positioning
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(os.getcwd(), f'pdf_viewer_{timestamp}.png')
        page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"Full page screenshot saved to {screenshot_path}")
        
        # Log the page content for debugging
        logger.info("Page content:")
        logger.info(page.content())
        
        # Try to find the download button by various selectors
        download_button = page.locator('button.download-button, a.download-link, [aria-label="Download"], [title="Download"]')
        if download_button.is_visible():
            logger.info("Found download button by selector")
            download_button.click()
        else:
            # If no download button is found, try clicking at coordinates
            logger.info("Download button not found by selector, trying coordinates")
            x = viewport['width'] - 95  # Approximately 95 pixels from the right edge
            y = 35  # Approximately 35 pixels from the top
            
            logger.info(f"Clicking at coordinates: x={x}, y={y}")
            page.mouse.click(x, y)
        
        logger.info("Download button clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click download button: {str(e)}")
        # Log the page content for debugging
        logger.error("Complete page HTML content:")
        logger.error(page.content())
        # Take a screenshot for debugging
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(os.getcwd(), f'pdf_viewer_error_{timestamp}.png')
            page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Error screenshot saved to {screenshot_path}")
        except Exception as screenshot_error:
            logger.error(f"Failed to take error screenshot: {str(screenshot_error)}")

def download_pdf(page):
    """Download the PDF from the current page"""
    try:
        logger.info("Starting PDF download...")
        # Wait for the PDF to be loaded
        page.wait_for_timeout(3000)  # Wait for 3 seconds for PDF to load
        
        # Get the download path
        download_path = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            
        # Generate unique filename based on timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f'flood_area_{timestamp}.pdf'
        pdf_path = os.path.join(download_path, pdf_filename)
        
        # Set up download behavior
        page.context.set_default_download_behavior('accept', download_path)
        
        # Click the download button (usually a save icon or download button)
        download_button = page.locator('button.download-button, a.download-link, [aria-label="Download"]')
        if download_button.is_visible():
            download_button.click()
            logger.info("Download button clicked")
        else:
            # If no download button is found, try to save the page as PDF
            page.pdf(path=pdf_path)
            logger.info("Page saved as PDF")
            
        # Wait for download to complete
        page.wait_for_timeout(5000)  # Wait for 5 seconds for download to complete
        
        logger.info(f"PDF downloaded successfully to {pdf_path}")
        return pdf_path
    except Exception as e:
        logger.error(f"Failed to download PDF: {str(e)}")
        return None

def get_flood_area_pdf(referencia_catastral):
    """
    Navigate to the IDEIB website and generate a PDF for the given cadastral reference
    Returns the path to the generated PDF
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode for better performance
        
        # Set up download directory
        download_dir = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            
        # Create context with download behavior
        context = browser.new_context(
            accept_downloads=True
        )
        page = context.new_page()
        
        page.goto('https://ideib.caib.es/visor/')
        maximize_window(page)
        close_initial_modal(page)
        click_afegir_dades(page)
        input_inundacio_search(page)
        add_layer_risc_inundacio(page)
        close_afegir_dades(page)
        click_locate_icon(page)
        click_cadastre_tab(page)
        enter_cadastral_reference(page, referencia_catastral)
        close_cerca_avancada(page)
        zoom_in_twice(page)
        click_print_icon(page)
        click_imprimir(page)
        
        # Handle PDF download in the main tab
        pdf_path = click_pdf(page)
        
        browser.close()
        return pdf_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/get_pdf', methods=['POST'])
def get_pdf():
    referencia_catastral = request.form.get('referencia_catastral')
    if not referencia_catastral:
        return jsonify({'error': 'No cadastral reference provided'}), 400
    pdf_path = get_flood_area_pdf(referencia_catastral)
    if pdf_path:
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': 'Failed to generate PDF'}), 500

@app.route('/<string:referencia_catastral>', methods=['GET'])
def get_pdf_by_url(referencia_catastral):
    pdf_path = get_flood_area_pdf(referencia_catastral)
    if pdf_path:
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': 'Failed to generate PDF'}), 500

if __name__ == '__main__':
    # Test the PDF generation with a sample cadastral reference
    # sample_referencia_catastral = '07040A04900017'  # Replace with an actual reference
    # pdf_path = get_flood_area_pdf(sample_referencia_catastral)
    # if pdf_path:
    #     print(f"PDF generated successfully: {pdf_path}")
    # else:
    #     print("Failed to generate PDF.")


    app.run(debug=True)