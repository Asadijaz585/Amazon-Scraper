import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# , options=chrome_options

products = []

chrome_path = 'chromedriver'
driver = webdriver.Chrome(chrome_path)
i = 1
Loginin
driver.get('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F%26tag%3Dgoogleglobalp-20%26ref%3Dnav_ya_signin%26adgrpid%3D82342659060%26hvpone%3D%26hvptwo%3D%26hvadid%3D585475370855%26hvpos%3D%26hvnetw%3Dg%26hvrand%3D16654465061235460169%26hvqmt%3De%26hvdev%3Dc%26hvdvcmdl%3D%26hvlocint%3D%26hvlocphy%3D1011082%26hvtargid%3Dkwd-10573980%26hydadcr%3D2246_13468515&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')
time.sleep(3)
driver.find_element(By.XPATH, "//input[@type='email']").send_keys('@gmail.com')
time.sleep(1)
driver.find_element(By.XPATH, "//input[@id='continue']").click()
time.sleep(1)
driver.find_element(By.XPATH, "//input[@type='password']").send_keys('*****')
time.sleep(1)
driver.find_element(By.XPATH, "//input[@id='signInSubmit']").click()
time.sleep(2)
import pdb;pdb.set_trace()
while True:
    i = i
    try:
        driver.get('https://www.amazon.com/s?srs=21217035011&bbn=21217035011&rh=n%3A21217035011%2Cp_85%3A1&dc&page={}&qid=1681964618&ref=sr_pg_{}'.format(int(i),int(i)))
        time.sleep(3)
    except:
        pass
    try:
        driver.find_element(By.XPATH,"//span[@id='a-autoid-0']").click()
        time.sleep(1)
    except:
        pass
    for link in driver.find_elements(By.XPATH,"//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']/a"):
        products.append(link.get_attribute('href'))
        
    time.sleep(2)
    print(len(products))
    i = int(i) + 1
    driver.execute_script("window.scrollTo(0, 4000)") 
    time.sleep(2)
    try:
        print(driver.find_element(By.XPATH,"//a[@class='s-pagination-item s-pagination-button'][last()]").get_attribute('text'))
        time.sleep(2)
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']").click()
        time.sleep(3)
    except:
        df = pd.DataFrame(products)
        df.to_csv('URLS_kitchen Appliences.csv', index=False)
        if driver.find_element(By.XPATH, "//span[@class='s-pagination-item s-pagination-next s-pagination-disabled ']").text == 'Next':
            break
        break
    
# print(len(products))


print('url done')
