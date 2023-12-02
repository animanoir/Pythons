from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfkit
import time

def get_driver():
  # Set options to make browsing easier
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(options=options)
  driver.get("https://asalvoenlasoledad.blogspot.com/")
  return driver

def get_blog_content(driver):
  time.sleep(2)
  content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
  return content

def main():
  path_wkhtmltopdf = "./wkhtmltopdf/bin/wkhtmltopdf.exe"
  config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
  driver = get_driver()
  blog_content = get_blog_content(driver)
  driver.quit()

  pdfkit.from_string(blog_content, "blog.pdf",configuration=config)

if __name__ == "__main__":
    main()