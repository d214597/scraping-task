import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure WebDriver options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# List of product URLs
product_urls = [
    'https://store.igefa.de/merchants/14A76F3B4C23954C/?pv=446918203&cv=1&ca=&cp=1&vi=6BF88EAB50F9AB7B&p=2134089%7C1730378266',
    # Add more product URLs here if needed
]

# List to store all product data
all_product_data = []

# Scrape each product page
for product_url in product_urls:
    product_data = {}
    try:
        driver.get(product_url)

        # Wait for the product title to be visible
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-title')))

        # Extract data
        product_data['Produktbild'] = driver.find_element(By.TAG_NAME, 'img').get_attribute('src')
        product_data['Produktbezeichnung'] = driver.find_element(By.CLASS_NAME, 'product-title').text

        # Extract Article Number
        try:
            product_data['Herstellerartikelnummer'] = driver.find_element(By.XPATH,
                                                                          '//div[contains(text(), "Article number")]/following-sibling::div').text
        except:
            product_data['Herstellerartikelnummer'] = 'Not available'

        # Extract EAN/GTIN
        try:
            product_data['EAN/GTIN'] = driver.find_element(By.XPATH,
                                                           '//div[contains(text(), "EAN")]/following-sibling::div').text
        except:
            product_data['EAN/GTIN'] = 'Not available'

        # Extract Manufacturer Number
        try:
            product_data['Lieferantenartikelnummer'] = driver.find_element(By.XPATH,
                                                                           '//div[contains(text(), "Manufacturer number")]/following-sibling::div').text
        except:
            product_data['Lieferantenartikelnummer'] = 'Not available'

        # Extract additional characteristics
        try:
            product_data['Original Data Column 2 (Ausführung)'] = driver.find_element(By.XPATH,
                                                                                      '//div[contains(text(), "CLEAN and CLEVER SMART")]/following-sibling::div').text
        except:
            product_data['Original Data Column 2 (Ausführung)'] = 'Not available'

        # Extract product description
        try:
            product_data['Produktbeschreibung'] = driver.find_element(By.CLASS_NAME, 'product-description').text
        except:
            product_data['Produktbeschreibung'] = 'Not available'

        # Manufacturer Name (Replace with actual logic if needed)
        product_data['Herstellername'] = 'CLEAN and CLEVER SMART'

        # Additional Description (Replace with actual logic if needed)
        product_data['Original Data Column 3 (Add. Description)'] = 'Additional Description'

        # Breadcrumb (assuming it's available in the same context, replace with actual logic if needed)
        product_data['Original Data Column 1 (Breadcrumb)'] = 'Breadcrumb'

        # Append the data to the list
        all_product_data.append(product_data)

    except Exception as e:
        print(f"Error while scraping {product_url}: {e}")

# Close the driver
driver.quit()

# Save the data to a CSV file
if all_product_data:  # Check if data was scraped
    df = pd.DataFrame(all_product_data)
    df.to_csv('product_data.csv', index=False, encoding='utf-8-sig')
    print("Data saved to 'product_data.csv'")
else:
    print("No product data was scraped.")
