import os
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions

def convert_html_to_pdf():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=900,1200")

    driver = webdriver.Chrome(options=options)
    try:
        html_path = os.path.abspath("DevOps_Project_Poster.html")
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        print(f"Loading {file_url}...")
        driver.get(file_url)

        driver.implicitly_wait(2)

        print_options = PrintOptions()
        print_options.orientation = "portrait"
        print_options.background = True
        print_options.page_ranges = ["1"]
        print_options.page_width = 21.0  # cm (A4 portrait)
        print_options.page_height = 29.7 # cm
        print_options.margin_top = 0.6   # cm
        print_options.margin_bottom = 0.6
        print_options.margin_left = 0.6
        print_options.margin_right = 0.6
        print_options.scale = 0.98

        pdf_b64 = driver.print_page(print_options)
        pdf_data = base64.b64decode(pdf_b64)

        output_path = os.path.abspath("DevOps_Project_Poster.pdf")
        with open(output_path, "wb") as f:
            f.write(pdf_data)

        print(f"Successfully generated Portrait single-page PDF at: {output_path}")
        print(f"File size: {len(pdf_data)} bytes")
    finally:
        driver.quit()

if __name__ == "__main__":
    convert_html_to_pdf()
