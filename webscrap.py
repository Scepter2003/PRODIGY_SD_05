import csv
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Function to scrape product data from Amazon
def scrape_amazon(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    products = []
    product_containers = driver.find_elements(By.CSS_SELECTOR, 'div.puisg-row')

    for container in product_containers:
        product = {}
        try:
            name_element = container.find_element(By.CSS_SELECTOR, 'h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2')
            product['name'] = name_element.text.strip()

            price_element = container.find_element(By.CSS_SELECTOR, 'span.a-price')
            product['price'] = price_element.text.strip()

            rating_element = container.find_element(By.CSS_SELECTOR, 'div.a-row.a-size-small')
            product['rating'] = rating_element.text.split()[0]
        except:
            continue
        products.append(product)

    driver.quit()
    return products

# Function to save product data to a CSV file
def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'price', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

# Tkinter GUI
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Amazon Product Scraper")
        self.geometry("600x400")

        # Create GUI elements
        self.url_label = ttk.Label(self, text="Enter Amazon Search URL:")
        self.url_label.pack(pady=10)

        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.pack()

        self.scrape_button = ttk.Button(self, text="Scrape Products", command=self.scrape_products)
        self.scrape_button.pack(pady=10)

        self.output_label = ttk.Label(self, text="Output:")
        self.output_label.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(self, width=60, height=10)
        self.output_text.pack()

    def scrape_products(self):
        url = self.url_entry.get()
        products = scrape_amazon(url)

        self.output_text.delete('1.0', tk.END)
        for product in products:
            self.output_text.insert(tk.END, f"Name: {product['name']}\nPrice: {product['price']}\nRating: {product['rating']}\n\n")

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            save_to_csv(products, filename)
            self.output_text.insert(tk.END, f"Product data saved to {filename}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
