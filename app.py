import streamlit as st
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from PIL import Image
from io import BytesIO

def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')



def hotel_crawling(country,city,adult,kid,sort):
    # options = webdriver.ChromeOptions()
    options = Options()
    driver = get_driver()
    driver.get('https://hotels.naver.com/')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    actions = ActionChains(driver)
    # url = 'https://hotels.naver.com/'
    # driver.get(url)
    
    # 여행지 입력
    driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/button').click()
    driver.find_element('xpath','//*[@id="__next"]/div/div[2]/div[1]/div/input').send_keys(city)
    time.sleep(1)
    driver.find_element('xpath','//*[@id="__next"]/div/div[2]/div[2]/section/ul/li[1]').click()
    # 인원수 입력
    driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/div/div[3]/button').click()
    if adult == 1:
        driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/button[1]').click()
    elif adult > 2:
        for i in range(abs(adult-2)):
            driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/button[2]').click()

    if kid > 0:
        for i in range(kid):
            driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/button[2]').click()

    driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/button').click()

    driver.find_element('xpath','//*[@id="__next"]/div/div/div[2]/div/div/button').click()
    
    # 정렬
    time.sleep(3)
    select_element = driver.find_element(By.CLASS_NAME,'SortFilters_select__kyrE3')
    select = Select(select_element)
   
    if sort == '인기순':
        select.select_by_value("rkd")
    if sort == '평점 높은순':
        select.select_by_value("grd")
    if sort == '성급 높은순':
        select.select_by_value("sta")
    if sort == '가격 낮은순':
        select.select_by_value("std")
    if sort == '가격 높은순':
        select.select_by_value("prd")

    for i in range(1, 6):
        hotel_name = None
        hotel_rating = None
        hotel_review = None
        hotel_image = None
        
        try:
            hotel_name = driver.find_element('xpath', f'//*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[{i}]/div[1]/div[2]/h4').text
        except NoSuchElementException:
            pass
        
        try:
            hotel_rating = driver.find_element('xpath', f'//*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[{i}]/div[1]/div[2]/div/i[1]').text
        except NoSuchElementException:
            pass
        
        try:
            hotel_review = driver.find_element('xpath', f'//*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[{i}]/div[1]/div[2]/i[2]').text
        except NoSuchElementException:
            pass
        
        try:
            hotel_image = driver.find_element('xpath', f'//*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[{i}]/div[1]/div[1]/a/img').get_attribute('src')
        except NoSuchElementException:
            pass
        if hotel_image is not None:
            response = requests.get(hotel_image)
            image = Image.open(BytesIO(response.content))
            resized_image = image.resize((330,200))
        
        cols = st.columns(2)
        with cols[0]:
            st.image([resized_image],width=330)
        with cols[1]:
            st.write('호텔명 : ',hotel_name)
            st.write('평점 : ',hotel_rating)
            st.write('특징 : ',hotel_review)
        time.sleep(1)


sorted = ['인기순','평점 높은순','성급 높은순','가격 낮은순','가격 높은순']

with st.form('form4'):
    st.text('아래의 정보를 입력하세요')
    col1,col2 = st.columns(2)
    with col1:
        country = st.text_input(
            '국가 (필수)'
        )
    with col2:
        city = st.text_input(
            '도시 (필수)'
        )
    col1,col2,col3 = st.columns(3)
    with col1:
        adult = st.number_input(
            '성인',
            min_value = 1,
            max_value = 10,
            step = 1,
            value = 1
        )
    with col2:
        kid = st.number_input(
            '아동',
            min_value = 0,
            max_value = 10,
            step = 1,
            value = 0
        )
    with col3:
        sort = st.selectbox(
            '정렬',
            sorted
        )
    submit = st.form_submit_button('제출')
    st.write('제출 후 잠시만 기다려주세요!')
    if submit:
        if not country:
            st.error('국가를 입력해주세요')
        elif not city:
            st.error('도시를 입력해주세요')
        else:
            country = country
            city = city
            adult = adult
            kid = kid
            sort = sort
            hotel_crawling(country,city,adult,kid,sort)