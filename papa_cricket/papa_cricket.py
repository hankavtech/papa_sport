import re
import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pprint



def reqpage():
    tot=0
    fil= open("C:/Users/keshav/Desktop/cricket_matches.txt","w+")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="C:/bin/chromedriver.exe", options=options)
    driver.get("https://www.dafabet.com/en/dfgoal/sports/215-cricket")
    time.sleep(20)
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    cards=soup.find_all(True,{'class':['event_path-content event-path-component','event_path-content event-path-component row-colors-inverted']})
    events=[]
    for card in cards:
        event_title=card.find('div',class_='event-header-title').h2.a.text.strip()
        restricted=['Electronic','Simulated']
        if any(s in event_title for s in restricted):
            continue
        event_divs=card.find('div', class_='event_path_events_container columns-1').find_all('div',class_='event-component')
        for event_div in event_divs:
            event={"id":"","date_time":"","tournament":event_title,"team1":"","team2":"","markets":""}
            event["id"]=event_div.find('div',attrs={'data-event-id' : True})['data-event-id']

            event_time_div=event_div.find('div',class_='event-time')
            time_spans=event_time_div.find('span',class_='event-time-content').find_all('span')
            i=0
            date_time = {"day": "", "time": ""}
            for time_span in time_spans:
                i=i+1
                if i==1:
                    date_time["day"]=time_span.text.strip()
                if i==2:
                    date_time["time"]=time_span.text.strip()
            event["date_time"]=date_time

            team_divs=event_div.find('div',class_='event-description').find_all('div',class_='opponent-name-wrapper')
            j=0
            for team_div in team_divs:
                j=j+1
                if j==1:
                    event["team1"]= team_div.find('a',attrs={'class':re.compile('^opponent-name.*')}).text.strip()
                if j==2:
                    event["team2"] = team_div.find('a',attrs={'class':re.compile('^opponent-name.*')}).text.strip()

            #object to store all markets
            markets = {"h2h_match":{"team1_price":"","team2_price":""}}

            # h2h_match extraction
            h2h_market_container = ""
            h2h_market_container = event_div.find('div', attrs={'data-description': 'Head To Head', 'data-market_period_description': 'Match'})

            try:
                h2h_match_divs = h2h_market_container.find_all('div',class_='outcome-button-wrapper')
                m = 0
                for h2h_match_div in h2h_match_divs:
                    m = m + 1
                    if m == 1:
                        markets["h2h_match"]["team1_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()

                    if m==2:
                        markets["h2h_match"]["team2_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()

            except:
                pass

            event["markets"] = markets
            events.append(event)
            pprint.pprint(event)


    fil.write(json.dumps(eval(str(events).strip())))
    fil.close()

    driver.close()

reqpage()
