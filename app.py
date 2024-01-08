import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

driver = get_driver()
driver.get('https://quotes.toscrape.com/')

quotes = driver.find_elements('xpath', '//span[@class="text"]')

data = []
for q in quotes:
    data.append(q.text)
    
driver.quit()

df = pd.DataFrame(data, columns=['Quotes'])
st.dataframe(df)
