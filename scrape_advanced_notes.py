# Get a web driver, and figure out how to install it here:
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f

# 1. Download firefox or Chrome https://www.mozilla.org/en-US/firefox/new/
# 2. Download the firefox driver
# https://github.com/mozilla/geckodriver/releases/tag/v0.26.0
# 3. Notarize the application (you may have to fix something in system preferences as well)
# 4. Move the file to your $PATH executable
# 5. Restart terminal and press on


import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import time

# You can totally find the hackathons by perusing the networking tabs, and seeing what's being done
# Using a web driver is much easier though
# We want to get all the github repos of a hackathon that finished in the last week

# 1. Find the hackathons that finished in the past week
# 2. Find all the github repos manually, then by script
# 3. Try bsoup - oh no!
# 4. Use a web driver - yes :) Mention you can use networking but eeehhhh


def get_finished_hackathons_from_last_week(finished_hackathons):
    recent_finished_hackathons = []
    for finished_hackathon in finished_hackathons:
        time_set = finished_hackathon.find_all("time")
        time_end = datetime.strptime(time_set[1].text, "%m/%d/%Y")
        now = datetime.now()
        if now < time_end + timedelta(days=7):
            recent_finished_hackathons.append(finished_hackathon)
    return recent_finished_hackathons


hackathons = []
result = requests.get("https://gitcoin.co/hackathon-list")
src = result.content
soup = BeautifulSoup(src, 'lxml')
finished_hackathons = soup.find(
    text=re.compile('Finished Hackathons')).parent.parent.find_all(
    'div', attrs={"class": "card-body col-9 col-sm-8"})
recent_finished_hackathons = get_finished_hackathons_from_last_week(
    finished_hackathons)
for recent_finished_hackathon in recent_finished_hackathons:
    links = recent_finished_hackathon.find_all('a')
    for link in links:
        if "projects" in link.attrs['href']:
            # Spaghetti code
            # methods should be at max 5 lines of code
            # print("https://gitcoin.co{}".format(link.attrs['href']))
            # hackathon_result = requests.get(
            #     "https://gitcoin.co/{}".format(link.attrs['href']))
            # hackathon_src = hackathon_result.content
            # hackathon_soup = BeautifulSoup(src, 'lxml')
            # github_links = hackathon_soup.find_all('a')
            # for github_link in github_links:
            #     if 'href' in github_link.attrs and 'github.com' in github_link.attrs['href']:
            #         print(github_link)
            options = Options()
            # Make it go faster!
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get("https://gitcoin.co/{}".format(link.attrs['href']))
            time.sleep(20)
            html = driver.page_source
            driver.quit()
            # print(html)
            projects_soup = BeautifulSoup(html, 'lxml')
            github_links = projects_soup.find_all('a')
            for github_link in github_links:
                if 'href' in github_link.attrs and 'github.com' in github_link.attrs['href']:
                    hackathons.append(github_link.attrs['href'])
for hack in hackathons:
    print(hack)


# Selenium
# pip install selenium
# pip install pandas
