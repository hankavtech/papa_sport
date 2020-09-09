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
    fil= open("C:/Users/keshav/PycharmProjects/papa_sport/papa_football/football_fixtures.txt","w+")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="C:/bin/chromedriver.exe", options=options)
    driver.get("https://www.dafabet.com/en/dfgoal/sports/240-football")
    time.sleep(20)
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    cards=soup.find_all(True,{'class':['event_path-content asian-event-path-component','event_path-content asian-event-path-component row-colors-inverted']})
    events=[]
    for card in cards:
        event_title=card.find('div',class_='event-header-title').h2.a.text.strip()
        event_divs=card.find('div', class_='event_path_events_container').find_all('div',class_='asian-event-component')
        for event_div in event_divs:
            event={"id":"","date_time":"","tournament":event_title,"team1":"","team2":"","markets":""}
            event["id"]=event_div.find('div',attrs={'data-event-id' : True})['data-event-id']

            event_time_div=event_div.find('div',class_='event-time')
            time_spans=event_time_div.find('span',class_='period-description').find_all('span')
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
            markets = {"goals_handicap": {"goals_handicap_team": "", "goals_handicap_value": "","goals_handicap_team1_price": "", "goals_handicap_team2_price": ""},"ou_match_goals":{"over_price":"","under_price":"","lines":""},"h2h_match":{"team1_price":"","team2_price":""},"first_half_goals_handicap": {"goals_handicap_team": "", "goals_handicap_value": "","goals_handicap_team1_price": "", "goals_handicap_team2_price": ""},"ou_first_half_goals":{"over_price":"","under_price":"","lines":""},"h2h_first_half":{"team1_price":"","team2_price":"","draw_price":""}}

            #goals_handicap_market extraction
            goals_handicap_market_container=""
            #goals_handicap_market_container=event_div.find_element_by_xpath('//div[@data-market-description="Asian Handicap - Games" and @data-market_period_description="Match"]')
            goals_handicap_market_container=event_div.find('div',attrs={'data-market-description': 'Asian Handicap','data-market_period_description':'Regular Time'})

            try:
                goals_handicap_divs=goals_handicap_market_container.find_all('div',class_='outcome-button-wrapper')
                k = 0
                for goals_handicap_div in goals_handicap_divs:
                    k = k + 1
                    if k == 1:
                        markets["goals_handicap"]["goals_handicap_team1_price"]=goals_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["goals_handicap"]["goals_handicap_value"]=goals_handicap_div.find('span',class_='hcap').text.strip()
                            markets["goals_handicap"]["goals_handicap_team"]="team1"
                        except:
                            markets["goals_handicap"]["goals_handicap_team"] = "team2"

                    else:
                        markets["goals_handicap"]["goals_handicap_team2_price"] = goals_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["goals_handicap"]["goals_handicap_value"]=goals_handicap_div.find('span',class_='hcap').text.strip()
                            markets["goals_handicap"]["goals_handicap_team"]="team2"
                        except:
                            pass

            except:
                pass
            
            
            
             # over_under_goals_match extraction
            over_under_match_goals_market_container = ""
            over_under_match_goals_market_container = event_div.find('div', attrs={'data-market-description': 'Over / Under', 'data-market_period_description': 'Regular Time'})

            try:
                over_under_match_goals_divs = over_under_match_goals_market_container.find_all('div',class_='outcome-button-wrapper')
                l = 0
                for over_under_match_goals_div in over_under_match_goals_divs:
                    l = l + 1
                    if l == 1:
                        markets["ou_match_goals"]["over_price"] = over_under_match_goals_div.find('span',class_='formatted_price').text.strip()
                        markets["ou_match_goals"]["lines"] = over_under_match_goals_div.find('span',class_='hcap').text.strip()

                    else:
                        markets["ou_match_goals"]["under_price"] = over_under_match_goals_div.find('span',class_='formatted_price').text.strip()

            except:
                pass


            # h2h_match extraction
            h2h_market_container = ""
            h2h_market_container = event_div.find('div', attrs={'data-market-description': 'Win/Draw/Win', 'data-market_period_description': 'Regular Time'})

            try:
                h2h_match_divs = h2h_market_container.find_all('div',class_='outcome-button-wrapper')
                m = 0
                for h2h_match_div in h2h_match_divs:
                    m = m + 1
                    if m == 1:
                        markets["h2h_match"]["team1_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()

                    if m==2:
                        markets["h2h_match"]["team2_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()

                    else:
                        markets["h2h_match"]["draw_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()



            except:
                pass
            
            
            # first_half_goals_handicap_market extraction
            # goals_handicap_market_container=event_div.find_element_by_xpath('//div[@data-market-description="Asian Handicap" and @data-market_period_description="Match"]')
            first_half_goals_handicap_market_container = event_div.find('div', attrs={'data-market-description': 'Asian Handicap', 'data-market_period_description': 'First Half'})

            try:
                first_half_goals_handicap_divs = first_half_goals_handicap_market_container.find_all('div', class_='outcome-button-wrapper')
                n = 0
                for first_half_goals_handicap_div in first_half_goals_handicap_divs:
                    n = n + 1
                    if n == 1:
                        markets["first_half_goals_handicap"]["goals_handicap_team1_price"] = first_half_goals_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["first_half_goals_handicap"]["goals_handicap_value"] = first_half_goals_handicap_div.find('span',class_='hcap').text.strip()
                            markets["first_half_goals_handicap"]["goals_handicap_team"] = "team1"
                        except:
                            markets["first_half_goals_handicap"]["goals_handicap_team"] = "team2"

                    else:
                        markets["first_half_goals_handicap"]["goals_handicap_team2_price"] = first_half_goals_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["first_half_goals_handicap"]["goals_handicap_value"] = first_half_goals_handicap_div.find('span',class_='hcap').text.strip()
                            markets["first_half_goals_handicap"]["goals_handicap_team"] = "team2"
                        except:
                            pass

            except:
                pass

            # over_under_first_half_match extraction
            over_under_first_half_goals_market_container = event_div.find('div', attrs={'data-market-description': 'Over / Under', 'data-market_period_description': 'First Half'})

            try:
                over_under_first_half_goals_divs = over_under_first_half_goals_market_container.find_all('div',class_='outcome-button-wrapper')
                o = 0
                for over_under_first_half_goals_div in over_under_first_half_goals_divs:
                    o = o + 1
                    if o == 1:
                        markets["ou_first_half_goals"]["over_price"] = over_under_first_half_goals_div.find('span',class_='formatted_price').text.strip()
                        markets["ou_first_half_goals"]["lines"] = over_under_first_half_goals_div.find('span',class_='hcap').text.strip()

                    else:
                        markets["ou_first_half_goals"]["under_price"] = over_under_first_half_goals_div.find('span',class_='formatted_price').text.strip()

            except:
                pass

            # h2h_first half extraction
            h2h_first_half_container = event_div.find('div', attrs={'data-market-description': 'Win/Draw/Win','data-market_period_description': 'First Half'})

            try:
                h2h_first_half_divs = h2h_first_half_container.find_all('div', class_='outcome-button-wrapper')
                p = 0
                for h2h_first_half_div in h2h_first_half_divs:
                    p = p + 1
                    if p == 1:
                        markets["h2h_first_half"]["team1_price"] = h2h_first_half_div.find('span',class_='formatted_price').text.strip()

                    if p==2:
                        markets["h2h_first_half"]["team2_price"] = h2h_first_half_div.find('span',class_='formatted_price').text.strip()

                    else:
                        markets["h2h_first_half"]["draw_price"] = h2h_first_half_div.find('span',class_='formatted_price').text.strip()

            except:
                pass
            

            event["markets"] = markets
            events.append(event)
            pprint.pprint(event)


    fil.write(json.dumps(eval(str(events).strip())))
    fil.close()

    driver.close()

reqpage()

