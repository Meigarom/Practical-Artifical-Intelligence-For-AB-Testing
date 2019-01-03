import numpy as np
from selenium import webdriver
from selenium.webdriver.support.color import Color

# define the customer prob of clicks
prob_list = [0.3, 0.8]

# instantiate a web browser and pass the address where the flask app is running
driver = webdriver.Chrome( executable_path='/Users/meigarom/chromedriver' )
driver.get( 'http://127.0.0.1:5000/home' )

# define the parameter of the experiment
trials = 101
episodes = 21
clicks = trials * episodes

# interate over all cliks
for click in range( clicks ):
    if click % 100 == 0:
        print( 'Click: {} / {}'.format( click, clicks ) )

    # find the color of the YES button in this webpage
    button_color = driver.find_element_by_id( 'yesbtn' ).value_of_css_property( 'background-color' )

    color = Color.from_string( button_color ).hex

    if color == '#008cba': # blue background color
        web_page = 1
    else:
        web_page = 0


    # decide the button to click - YES or NO
    if np.random.random() < prob_list[ web_page ]:
        driver.find_element_by_name( 'yescheckbox' ).click()
        driver.find_element_by_id( 'yesbtn' ).click()
    else:
        driver.find_element_by_name( 'nocheckbox' ).click()
        driver.find_element_by_id( 'nobtn' ).click()














