from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

base_url = "https://www.kroger.com/"
browser = webdriver.Firefox()
browser.get(base_url)
delay = 30 # seconds
try:
    browser.find_element_by_class_name("KImage-container").click() # getting rid of loation pop-up
    browser.find_elements_by_class_name("dpr")[18].click() # Start My Cart block -- dpr WithAmpDataInnerContainer.DynamicRender.NextBasketProductGrid
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "swiper-slide"))) # Wait for loading
    product_elems = browser.find_elements_by_class_name("swiper-slide") # Get the required list of html elements for products
    # Extract product details
    product_detail_list = []
    print("Individual product detail as dictionary :\n")
    for i in range(0,6):
        product = {}
        product["product_id"]=product_elems[i].find_element_by_class_name("Color").get_attribute("href").split("/")[-1]
        product["product_url"] = product_elems[i].find_element_by_class_name("Color").get_attribute("href")
        product["image_url"] = product_elems[i].find_elements_by_class_name("ImageLoader-image")[0].get_attribute("src")
        product["all_text"] = product_elems[i].text
        product["price"] = product_elems[i].find_element_by_class_name("kds-Price").get_attribute("value")
        product["price_text"] = product_elems[i].find_element_by_class_name("kds-Price").text
        product["product_display_name"] = product_elems[i].find_element_by_class_name("kds-Text--m").text
        product["sell_by"] = product_elems[i].find_element_by_class_name("ProductCard-sellBy").text
        print(product)
        product_detail_list.append(product)
    print("\n\nThe list of all products' details :\n")
    print(product_detail_list)
except TimeoutException:
    print("Loading took too much time!")
