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
    fil= open("C:/Users/keshav/Desktop/matches.txt","w+")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="C:/bin/chromedriver.exe", options=options)
    driver.get(f"https://www.dafabet.com/en/dfgoal/sports/239-tennis")
    time.sleep(10)
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    cards=soup.find_all(True,{'class':['event_path-content asian-event-path-component','event_path-content asian-event-path-component row-colors-inverted']})
    events=[]
    for card in cards:
        event_title=card.find('div',class_='event-header-title').h2.a.text.strip()
        event_divs=card.find('div', class_='event_path_events_container').find_all('div',class_='asian-event-component')
        for event_div in event_divs:
            event={"id":"","date_time":"","tournament":event_title,"player1":"","player2":"","markets":""}
            event["id"] = event_div.find('div', attrs={'data-event-id': True})['data-event-id']
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

            player_divs=event_div.find('div',class_='event-description').find_all('div',class_='opponent-name-wrapper serving')
            j=0
            for player_div in player_divs:
                j=j+1
                if j==1:
                    event["player1"]=player_div.find('a',class_='opponent-name').text.strip()
                if j==2:
                    event["player2"] = player_div.find('a', class_='opponent-name').text.strip()

            #object to store all markets
            markets = {"games_handicap": {"games_handicap_player": "", "games_handicap_value": "","games_handicap_player1_price": "", "games_handicap_player2_price": ""},"ou_match_games":{"over_price":"","under_price":"","lines":""},"h2h_match":{"player1_price":"","player2_price":""},"first_set_games_handicap": {"games_handicap_player": "", "games_handicap_value": "","games_handicap_player1_price": "", "games_handicap_player2_price": ""},"ou_first_set_games":{"over_price":"","under_price":"","lines":""},"h2h_first_set":{"player1_price":"","player2_price":""}}

            #games_handicap_market extraction
            games_handicap_market_container=""
            #games_handicap_market_container=event_div.find_element_by_xpath('//div[@data-market-description="Asian Handicap - Games" and @data-market_period_description="Match"]')
            games_handicap_market_container=event_div.find('div',attrs={'data-market-description': 'Asian Handicap - Games','data-market_period_description':'Match'})

            try:
                games_handicap_divs=games_handicap_market_container.find_all('div',class_='outcome-button-wrapper')
                k = 0
                for games_handicap_div in games_handicap_divs:
                    k = k + 1
                    if k == 1:
                        markets["games_handicap"]["games_handicap_player1_price"]=games_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["games_handicap"]["games_handicap_value"]=games_handicap_div.find('span',class_='hcap').text.strip()
                            markets["games_handicap"]["games_handicap_player"]="player1"
                        except:
                            markets["games_handicap"]["games_handicap_player"] = "player2"

                    else:
                        markets["games_handicap"]["games_handicap_player2_price"] = games_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["games_handicap"]["games_handicap_value"]=games_handicap_div.find('span',class_='hcap').text.strip()
                            markets["games_handicap"]["games_handicap_player"]="player2"
                        except:
                            pass

            except:
                pass

            # over_under_games_match extraction
            over_under_match_games_market_container = ""
            over_under_match_games_market_container = event_div.find('div', attrs={'data-market-description': 'Over/Under Games', 'data-market_period_description': 'Match'})

            try:
                over_under_match_games_divs = over_under_match_games_market_container.find_all('div',class_='outcome-button-wrapper')
                l = 0
                for over_under_match_games_div in over_under_match_games_divs:
                    l = l + 1
                    if l == 1:
                        markets["ou_match_games"]["over_price"] = over_under_match_games_div.find('span',class_='formatted_price').text.strip()
                        markets["ou_match_games"]["lines"] = over_under_match_games_div.find('span',class_='hcap').text.strip()

                    else:
                        markets["ou_match_games"]["under_price"] = over_under_match_games_div.find('span',class_='formatted_price').text.strip()

            except:
                pass

            # h2h_match extraction
            h2h_market_container = ""
            h2h_market_container = event_div.find('div', attrs={'data-market-description': 'Head To Head', 'data-market_period_description': 'Match'})

            try:
                h2h_match_divs = h2h_market_container.find_all('div',class_='outcome-button-wrapper')
                m = 0
                for h2h_match_div in h2h_match_divs:
                    m = m + 1
                    if m == 1:
                        markets["h2h_match"]["player1_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()

                    else:
                        markets["h2h_match"]["player2_price"] = h2h_match_div.find('span',class_='formatted_price').text.strip()

            except:
                pass

            # first_set_games_handicap_market extraction
            # games_handicap_market_container=event_div.find_element_by_xpath('//div[@data-market-description="Asian Handicap - Games" and @data-market_period_description="Match"]')
            first_set_games_handicap_market_container = event_div.find('div', attrs={'data-market-description': 'Asian Handicap - Games', 'data-market_period_description': '1st Set'})

            try:
                first_set_games_handicap_divs = first_set_games_handicap_market_container.find_all('div', class_='outcome-button-wrapper')
                n = 0
                for first_set_games_handicap_div in first_set_games_handicap_divs:
                    n = n + 1
                    if n == 1:
                        markets["first_set_games_handicap"]["games_handicap_player1_price"] = first_set_games_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["first_set_games_handicap"]["games_handicap_value"] = first_set_games_handicap_div.find('span',class_='hcap').text.strip()
                            markets["first_set_games_handicap"]["games_handicap_player"] = "player1"
                        except:
                            markets["first_set_games_handicap"]["games_handicap_player"] = "player2"

                    else:
                        markets["first_set_games_handicap"]["games_handicap_player2_price"] = first_set_games_handicap_div.find('span',class_='formatted_price').text.strip()
                        try:
                            markets["first_set_games_handicap"]["games_handicap_value"] = first_set_games_handicap_div.find('span',class_='hcap').text.strip()
                            markets["first_set_games_handicap"]["games_handicap_player"] = "player2"
                        except:
                            pass

            except:
                pass

            # over_under_first_set_match extraction
            over_under_first_set_games_market_container = event_div.find('div', attrs={'data-market-description': 'Over/Under Games', 'data-market_period_description': '1st Set'})

            try:
                over_under_first_set_games_divs = over_under_first_set_games_market_container.find_all('div',class_='outcome-button-wrapper')
                o = 0
                for over_under_first_set_games_div in over_under_first_set_games_divs:
                    o = o + 1
                    if o == 1:
                        markets["ou_first_set_games"]["over_price"] = over_under_first_set_games_div.find('span',class_='formatted_price').text.strip()
                        markets["ou_first_set_games"]["lines"] = over_under_first_set_games_div.find('span',class_='hcap').text.strip()

                    else:
                        markets["ou_first_set_games"]["under_price"] = over_under_first_set_games_div.find('span',class_='formatted_price').text.strip()

            except:
                pass

            # h2h_first set extraction
            h2h_first_set_container = event_div.find('div', attrs={'data-market-description': 'Head To Head','data-market_period_description': '1st Set'})

            try:
                h2h_first_set_divs = h2h_first_set_container.find_all('div', class_='outcome-button-wrapper')
                p = 0
                for h2h_first_set_div in h2h_first_set_divs:
                    p = p + 1
                    if p == 1:
                        markets["h2h_first_set"]["player1_price"] = h2h_first_set_div.find('span',class_='formatted_price').text.strip()

                    else:
                        markets["h2h_first_set"]["player2_price"] = h2h_first_set_div.find('span',class_='formatted_price').text.strip()

            except:
                pass





            event["markets"]=markets

            # over_under_market_container = event_div.find_element_by_xpath('//div[@data-market-description="Over/Under Games" and @data-market_period_description="Match"]')
            # h2h_market_container = event_div.find_element_by_xpath('//div[@data-market-description="Head To Head" and @data-market_period_description="Match"]')
            # first_set_games_handicap_market_container = event_div.find_element_by_xpath('//div[@data-market-description="Asian Handicap - Games" and @data-market_period_description="1st Set"]')
            # first_set_over_under_market_container = event_div.find_element_by_xpath('//div[@data-market-description="Over/Under Games" and @data-market_period_description="1st Set"]')
            # first_set_h2h_market_container = event_div.find_element_by_xpath('//div[@data-market-description="Head To Head" and @data-market_period_description="1st Set"]')

            events.append(event)


            tot=tot+1
            #print(tot,"||",event_title,'||',event_day,'||',event_time,'||',player1,'||',player2,'||',markets)

    fil.write(json.dumps(eval(str(events).strip())))
    fil.close()

    driver.close()

reqpage()

