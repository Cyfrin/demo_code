# scrape.py
# 1. All websites are basically HTML/CSS and javascript
# 2. We can use python to find whatever tags we are looking for
# 3. For pages that use a lot of javascript, we can use web drivers instead to make the calls

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

hackathons = []

result = requests.get(
    "https://devpost.com/hackathons?utf8=%E2%9C%93&search=blockchain&challenge_type=all&sort_by=Submission+Deadline")
src = result.content
soup = BeautifulSoup(src, 'lxml')


featured_challenges = soup.find_all(
    'a', attrs={'data-role': 'featured_challenge'})

for featured_challenge in featured_challenges:
    try:
        time = featured_challenge.find(
            "time", attrs={"class": "value timeago"}).text
        time_left = datetime.strptime(
            time[:-4], "%b %d, %Y %I:%M %p")
        now = datetime.now()
        if now > time_left - timedelta(days=50):
            hackathons.append(featured_challenge.attrs['href'])
    except:
        continue

for hackathon in hackathons:
    print(hackathon)
