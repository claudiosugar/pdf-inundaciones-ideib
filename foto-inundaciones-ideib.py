from playwright.sync_api import sync_playwright
import time
import logging
from flask import Flask, render_template, request, send_file, jsonify
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

def take_screenshot(page, referencia_catastral):
    """Take a screenshot of the map"""
    try:
        logger.info("Taking screenshot...")
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'flood_area_{referencia_catastral}_{timestamp}.png'
        filepath = os.path.join(screenshots_dir, filename)
        
        # Take the screenshot
        page.screenshot(path=filepath, full_page=True)
        logger.info(f"Screenshot saved to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None

def close_left_column(page):
    """Close/minimize the left column"""
    try:
        left_column = page.locator('.bar.max')
        if left_column.is_visible():
            time.sleep(0.5)
            left_column.click()  # First click
            time.sleep(0.5)
            left_column.click()  # Second click
            logger.info("Left column closed/minimized.")
    except Exception as e:
        logger.error(f"Failed to close/minimize left column: {str(e)}")

def get_flood_area_image(referencia_catastral):
    """
    Navigate to the IDEIB website and generate a screenshot for the given cadastral reference
    Returns the path to the generated image
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://ideib.caib.es/visor/')
        maximize_window(page)
        close_initial_modal(page)
        click_afegir_dades(page)
        input_inundacio_search(page)
        add_layer_risc_inundacio(page)
        close_afegir_dades(page)
        
        # Close the left column after adding our layers
        close_left_column(page)
        
        click_locate_icon(page)
        click_cadastre_tab(page)
        enter_cadastral_reference(page, referencia_catastral)
        close_cerca_avancada(page)
        zoom_in_twice(page)
        
        # Hide UI elements and take screenshot
        hide_ui_elements(page)
        time.sleep(10)
        image_path = take_screenshot(page, referencia_catastral)
        time.sleep(39)
        
        browser.close()
        return image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/get_image', methods=['GET', 'POST'])
def get_image():
    if request.method == 'POST':
        referencia_catastral = request.form.get('referencia_catastral')
    else:  # GET
        referencia_catastral = request.args.get('referencia_catastral')
        
    if not referencia_catastral:
        return jsonify({'error': 'No cadastral reference provided'}), 400
    image_path = get_flood_area_image(referencia_catastral)
    if image_path:
        return send_file(image_path, as_attachment=True)
    else:
        return jsonify({'error': 'Failed to generate image'}), 500

@app.route('/<string:referencia_catastral>', methods=['GET'])
def get_image_by_url(referencia_catastral):
    image_path = get_flood_area_image(referencia_catastral)
    if image_path:
        return send_file(image_path, as_attachment=True)
    else:
        return jsonify({'error': 'Failed to generate image'}), 500

if __name__ == '__main__':
    app.run(debug=True) 