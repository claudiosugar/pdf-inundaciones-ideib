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
        time.sleep(0.5)  # Reduced wait time
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
        add_button = page.locator('div.item-card-inner:has(h3.title[title="Xarxa Hidrogràfica i Risc Inundació"]):has(div.info:has-text("Servei de: GOIB: Direcció General de Recursos Hídrics")) a[data-dojo-attach-point="addButton"]')
        add_button.wait_for(state="visible", timeout=5000)  # Wait for the button to be visible
        add_button.click()  # Click the 'Afegir' button
        logger.info("'Afegir' button for Risc Inundació clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click 'Afegir' button for Risc Inundació: {str(e)}")

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

def get_flood_area_pdf(referencia_catastral):
    """
    Navigate to the IDEIB website and generate a PDF for the given cadastral reference
    Returns the path to the generated PDF
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Changed to False to see browser actions
        page = browser.new_page()
        page.goto('https://ideib.caib.es/visor/')
        maximize_window(page)
        close_initial_modal(page)
        click_afegir_dades(page)
        input_inundacio_search(page)
        add_layer_risc_inundacio(page)
        click_locate_icon(page)
        click_cadastre_tab(page)
        enter_cadastral_reference(page, referencia_catastral)
        zoom_in_three_times(page)
        time.sleep(100)

        
        pdf_path = generate_pdf(page, referencia_catastral)
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
    sample_referencia_catastral = 'YOUR_CADASTRAL_REFERENCE'  # Replace with an actual reference
    pdf_path = get_flood_area_pdf(sample_referencia_catastral)
    if pdf_path:
        print(f"PDF generated successfully: {pdf_path}")
    else:
        print("Failed to generate PDF.")


        #app.run(debug=True)