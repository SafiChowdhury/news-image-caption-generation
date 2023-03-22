import os
from PIL import Image
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import json


# Define a function to convert WebP images to PNG and save them, and return a dictionary containing the filename and caption.
def convert_save_image(image_url, caption_text, folder_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        files = os.listdir(folder_name)
        # Encode caption text in UTF-8 and remove any invalid characters
        encoded_caption = caption_text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        # Use a numerical index for the filename
        filename = f"{len(files)+1}.png"

        with open(os.path.join(folder_name, filename), "wb") as f:
            f.write(response.content)

        with Image.open(os.path.join(folder_name, filename)) as im:
            im.save(os.path.join(folder_name, filename))

        # Return filename and caption text as a dictionary
        return {"filename": filename, "caption": [encoded_caption]}

    return None

# Set up the driver
dataset = pd.DataFrame(columns=['news_title', 'news_link'])
driver = webdriver.Chrome()

# Navigate to the page
driver.get('https://www.prothomalo.com/photo/bangladesh')
time.sleep(2)

# Find all the image elements
title = []
link = []
blocks = driver.find_elements(By.CLASS_NAME, 'left_image_right_news')

# Loop over the images and store their titles and links in a DataFrame
for block in blocks:
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

# Close the driver
driver.quit()

# Download each image and extract its caption, and store the filename and caption in a list of dictionaries
folder_name = 'images'
captions_list = []

for url in link:
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for the page to load completely.
    time.sleep(2)

    # Find all the news items on the page.
    news_items = driver.find_elements(By.CLASS_NAME, "photo-story-element")

    # Loop over each news item to extract its image URL and caption.
    for i, news_item in enumerate(news_items):
        # Check if the news item has an image element.
        driver.execute_script("arguments[0].scrollIntoView();", news_item)
        time.sleep(2)

        if news_item.find_elements(By.CLASS_NAME, "story-element-image"):
            # Find the image element and its source URL.
            image_element = news_item.find_element(By.CLASS_NAME, "story-element-image").find_element(By.TAG_NAME,
                                                                                                      "img")
            image_url = image_element.get_attribute("src")

            # Check if the news item has a caption element.
            if news_item.find_elements(By.CLASS_NAME, "story-element-image-title"):
                # Find the caption element and its text content.
                caption_element = news_item.find_element(By.CLASS_NAME, "story-element-image-title")
                caption_text = caption_element.text

                # Print the image URL and caption.
                print("Image URL:", image_url)
                print("Caption:", caption_text)

                # Convert the WebP image to PNG and save it, and store the filename and caption in a dictionary
                caption_dict = convert_save_image(image_url, caption_text, folder_name)
                if caption_dict is not None:
                    captions_list.append(caption_dict)

    driver.quit()

    # Write captions_list to a .json file
    with open('captions.json', 'w', encoding='utf-8') as f:
        json.dump(captions_list, f, ensure_ascii=False)

    # Save the DataFrame to a .csv file
    dataset.to_csv('bangla news caption dataset.csv')