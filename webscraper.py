import numpy as np
from selenium import webdriver

#open a browers - http://chromedriver.chromium.org/downloads
driver = webdriver.Chrome( executable_path='/Users/meigarom/chromedriver' )

#flask application address
driver.get( 'http://127.0.0.1:5000/home' )

#find the button and click on it
clicks = 100
for click in range( clicks ):
    if np.random.random() < 0.5:
        driver.find_element_by_name( 'yescheckbox' ).click()
        driver.find_element_by_id( 'yesbtn' ).click()
    else:
        driver.find_element_by_name( 'nocheckbox' ).click()
        driver.find_element_by_id( 'nobtn' ).click()
