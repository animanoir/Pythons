#-*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfkit
import base64
import time

def get_driver():
  # Set options to make browsing easier
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")
  options.add_argument("--disable-images")  # Disable images

  driver = webdriver.Chrome(options=options)
  driver.get("https://asalvoenlasoledad.blogspot.com/")
  return driver

def get_blog_content(driver):
  time.sleep(5)
  # content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
  all_text = "\n\n".join([p.text for p in driver.find_elements(By.TAG_NAME, "p")])
  return all_text

def encode_font_to_base64(font_path):
    with open(font_path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode('utf-8')

def main():
  path_wkhtmltopdf = "./wkhtmltopdf/bin/wkhtmltopdf.exe"
  config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
  driver = get_driver()
  all_blog_content = ""

  #page_count = 0  # Initialize page counter

  while True:
    all_blog_content += get_blog_content(driver)
    current_url = driver.current_url  # Get the current URL
    print("///////")
    print(f"Scraping content from: {current_url}")  # Print or use the current URL
    print("///////")
    try:
      next_page = driver.find_element(By.CLASS_NAME, "blog-pager-older-link")
      next_page.click()
      time.sleep(5)
    except Exception:
      print("No more pages to load or error occurred.")
      break
    #page_count += 1  # Increment page counter

  driver.quit()

  font_face = """
  @font-face {
    font-family: 'Cardo';
    src: url(data:application/font-woff;charset=utf-8;base64,[./Cardo-Regular.ttf]) format('truetype');
  }
  """
  style = "<style>{}</style>".format(font_face)
  html_content = "<html><head>{}</head><body style='font-family:Cardo;'>{}</body></html>".format(style, all_blog_content)

  # Embed the base64 encoded font in HTML
  font_path = './Cardo-Regular.ttf'  # Replace with your actual font file path
  encoded_font = encode_font_to_base64(font_path)
  font_face = f"""
  @font-face {{
      font-family: 'Cardo';
      src: url(data:font/truetype;charset=utf-8;base64,{encoded_font}) format('truetype');
  }}
  """
  style = f"<style>{font_face}</style>"
  html_content = f"<html><head>{style}</head><body style='font-family:Cardo;'>{all_blog_content}</body></html>"

  # Use pdfkit to generate PDF from HTML
  print("Generating PDF...")
  pdfkit.from_string(html_content, "blog_content.pdf", configuration=config, options={'encoding': "UTF-8"})

if __name__ == "__main__":
    main()