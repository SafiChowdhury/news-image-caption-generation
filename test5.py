
#
# # set up the driver
# driver = webdriver.Chrome()
#
# # navigate to the webpage
# driver.get('https://www.prothomalo.com/photo/bangladesh')
#
# # find the "load-more-content" button
# load_more_btn = driver.find_element(By.CLASS_NAME, 'load-more-content')
#
# # loop until there are no more images to load
# while True:
#     try:
#         # wait for the button to be clickable
#         load_more_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'load-more-content')))
#
#         # click the button to load more images
#         load_more_btn.click()
#     except:
#         # if there are no more images to load, break out of the loop
#         break
#
# # get all the image elements
# image_elements = driver.find_elements(By.CLASS_NAME, 'left_image_right_news')
#
# # print the URLs of all the images
# for image in image_elements:
#     ftitle = image.find_element(By.CLASS_NAME, 'headline-title').text
#     block_link = image.find_element(By.TAG_NAME, 'a')
#     flink = block_link.get_attribute('href')
#     print(ftitle)
#
# # close the browser window
# driver.quit()
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# # set up the driver
# driver = webdriver.Chrome()
#
# # navigate to the webpage
# driver.get('https://www.prothomalo.com/photo/bangladesh')
#
# # find the "load-more-content" button
# load_more_xpath = '//*[@id="container"]/div/div[2]/div/div/div[3]/div[2]/div[17]/div'
# load_more_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, load_more_xpath)))
# page=1
# # loop until there are no more images to load
# while page<20:
#     try:
#         # click the button to load more images
#         load_more_btn.click()
#     except:
#         # if there are no more images to load, break out of the loop
#         break
#
# # get all the image elements
# image_elements = driver.find_elements(By.CLASS_NAME, 'left_image_right_news')
#
# # print the URLs of all the images
# for image in image_elements:
#     ftitle = image.find_element(By.CLASS_NAME, 'headline-title').text
#     block_link = image.find_element(By.TAG_NAME, 'a')
#     flink = block_link.get_attribute('href')
#     print(ftitle)
# #close the browser window
# driver.quit()
dataset = pd.DataFrame(columns=['news_title', 'news_link'])
driver = webdriver.Chrome()

# navigate to the page
driver.get('https://www.prothomalo.com/photo/bangladesh')

# find all the image elements
title = []
link = []
blocks = driver.find_elements(By.CLASS_NAME, 'left_image_right_news')
count = 0
# loop over the images and print their captions
for block in blocks:
    time.sleep(5)


    ftitle = block.find_element(By.CLASS_NAME, 'headline-title').text
    block_link = block.find_element(By.TAG_NAME, 'a')
    flink = block_link.get_attribute('href')

    title.append(ftitle)
    link.append(flink)
    caption_data = {'News_title': title, 'News_link': link}
    news = pd.DataFrame(data=caption_data)
    data = {'title': title, 'link': link}
    review = pd.DataFrame(data=data)
    dataset = pd.concat([review], ignore_index=True)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # wait for 2 seconds
    time.sleep(2)
    count +=1

    try:
            # find the load more button on the webpage

        load_more = driver.find_element(By.CLASS_NAME, 'load-more-content')
            # click on that button
        load_more.click()
            # move on to next loadmore button
    except:
        # If couldnt find any button to click, stop
        break



print(len(title))
print(title)





driver.quit()