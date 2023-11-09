import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv

chrome_options = Options()
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--enable-cookies")

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.mannings.com.hk/zh_hk/'
search_keywords = ['衛生巾','沐浴用品','牙膏','洗臉','Shampoo','潄口水','Hand wash','Cream','GEL','Conditioner']

current_date = date.today().strftime("%Y-%m-%d")

for keyword in search_keywords:
    # Open browser for each keyword
    driver.get(url)
    time.sleep(2)
    search = driver.find_element(By.NAME, "text")
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)
    

    search_bar = driver.find_element(By.NAME, "text")
    search_bar.clear()
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.RETURN)


    wait = WebDriverWait(driver, 10)
    
    product_name = []
    price = []
    original_price = []
    discount = []
    


    result01_list = driver.find_elements(By.XPATH, '//div[@class="col-xs-12 col-sm-6 col-md-4"]')
    
    for result in result01_list:
        try:
            product_name.append(result.find_element(By.XPATH , ".//a[@class='pull-left product_name']").text)
        except:
            product_name.append('N/A')
            
        try:
            price.append(result.find_element(By.XPATH , ".//p[@class='price']").text)
        except:
            price.append('N/A')

        try:
            original_price.append(result.find_element(By.XPATH , ".//span[@class='pdp_price_offer']/s").text)
        except:
            original_price.append('N/A')
            
        try:
            discount.append(result.find_element(By.XPATH , ".//span[@class='pdp_price_offer']").text)
        except:
            discount.append('N/A')
        


    print(f'total run of post: {len(result01_list)}')
    import pandas as pd
    df = pd.DataFrame({'product_name':product_name,'price':price,'original_price':original_price,'discount':discount})
    print(df)

    num_of_result = len(result01_list)
    safe_brake = 30
    count = 0

    target_num_result = 2000

    while (num_of_result < target_num_result and count < safe_brake):
        show_more_results_button = driver.find_element(By.CLASS_NAME, 'pagination-next')
        show_more_results_button.click()
        time.sleep(3)

        result01_list = driver.find_elements(By.XPATH, '//div[@class="col-xs-12 col-sm-6 col-md-4"]')
        for result in result01_list:
            
            try:
                product_name.append(result.find_element(By.XPATH , ".//a[@class='pull-left product_name']").text)
            except:
                product_name.append('N/A')
            
            try:
                price.append(result.find_element(By.XPATH , ".//p[@class='price']").text)
            except:
                price.append('N/A')

            try:
                original_price.append(result.find_element(By.XPATH , ".//span[@class='pdp_price_offer']/s").text)
            except:
                original_price.append('N/A')
            
            try:
                discount.append(result.find_element(By.XPATH , ".//span[@class='pdp_price_offer']").text)
            except:
                discount.append('N/A')

        
        num_of_result = len(result01_list)
        count += 1

    print(f'total run of post: {len(result01_list)}')
    df = pd.DataFrame({'product_name':product_name,'price':price,'original_price':original_price,'discount':discount})
    print(df)

     # Create the CSV file name
    csv_file_name = f"{current_date}_{keyword}.csv"

    # Save the DataFrame as a CSV file
    df.to_csv(csv_file_name, index=False)

    # Close the browser for each keyword
    


driver.quit()