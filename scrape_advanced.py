# Get a web driver, and figure out how to install it here:
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f

# 1. Download firefox or Chrome https://www.mozilla.org/en-US/firefox/new/
# 2. Download the firefox driver
# https://github.com/mozilla/geckodriver/releases/tag/v0.26.0
# 3. Notarize the application (you may have to fix something in system preferences as well)
# 4. Move the file to your $PATH executable
# 5. Restart terminal and press on
# 6. # Selenium
# pip install selenium
# do the driver code

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

BASE_URL = "https://gitcoin.co{}"

# You can totally find the hackathons by perusing the networking tabs, and seeing what's being done
# Using a web driver is much easier though
# We want to get all the github repos of a hackathon that finished in the last week

# 1. Find the hackathons that finished in the past week
# 2. Find all the github repos manually, then by script
# 3. Try bsoup - oh no! We run into an issue!
# 4. Use a web driver - yes :)


def get_finished_hackathons_from_last_week(finished_hackathons):
    recent_finished_hackathons = []
    for finished_hackathon in finished_hackathons:
        time_set = finished_hackathon.find_all("time")
        time_end = datetime.strptime(time_set[1].text, "%m/%d/%Y")
        now = datetime.now()
        if now < time_end + timedelta(days=7):
            recent_finished_hackathons.append(finished_hackathon)
    return recent_finished_hackathons


result = requests.get("https://gitcoin.co/hackathon-list")
src = result.content
soup = BeautifulSoup(src, 'lxml')
finished_hackathons = soup.find(text=re.compile('Finished Hackathons')).parent.parent.find_all(
    'div', attrs={"class": "card-body col-9 col-sm-8"})
recent_finished_hackathons = get_finished_hackathons_from_last_week(
    finished_hackathons)

for recent_finished_hackathon in recent_finished_hackathons:
    links = recent_finished_hackathon.find_all('a')
    for link in links:
        if "projects" in link.attrs['href']:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get(BASE_URL.format(link.attrs['href']))
            time.sleep(10)
            html = driver.page_source
            projects_soup = BeautifulSoup(html, 'lxml')
            driver.quit()
            github_links = projects_soup.find_all('a')
            for github_link in github_links:
                if 'href' in github_link.attrs and 'github.com' in github_link.attrs['href']:
                    print(github_link.attrs['href'])
