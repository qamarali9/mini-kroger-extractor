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
    #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "swiper-slide")))
    #ActionChains(browser).move_to_element(browser.find_element_by_class_name("kds-Button")).click() 
    browser.find_element_by_class_name("KImage-container").click()
    #print(browser.find_element_by_class_name("kds-Button"))
    #ActionChains(browser).move_to_element(browser.find_element_by_class_name("ProductCard")).click().perform()
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.find_elements_by_class_name("dpr")[18].click() # dpr WithAmpDataInnerContainer.DynamicRender.NextBasketProductGrid
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "swiper-slide")))
    #myElem = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, "kds-Button")))#"swiper-slide"
    product_elems = browser.find_elements_by_class_name("swiper-slide")
    #print("Page is ready!")#print(product_elems)#print(product_elems[0].text)

    product_detail_list = []
    for i in range(0,10):
        product = {}
        product["product_id"]=product_elems[i].find_element_by_class_name("Color").get_attribute("href").split("/")[-1]
        product["product_url"] = product_elems[i].find_element_by_class_name("Color").get_attribute("href")
        product["image_url"] = product_elems[i].find_element_by_class_name("ImageLoader-image").get_attribute("src")
        product["all_text"] = product_elems[i].text
        product["price"] = product_elems[i].find_element_by_class_name("kds-Price").get_attribute("value")
        product["price_text"] = product_elems[i].find_element_by_class_name("kds-Price").text
        product["product_display_name"] = product_elems[i].find_element_by_class_name("kds-Text--m").text
        product["sell_by"] = product_elems[i].find_element_by_class_name("ProductCard-sellBy").text
        print(product)
        product_detail_list.append(product)

    print(product_detail_list)
except TimeoutException:
    print("Loading took too much time!")
