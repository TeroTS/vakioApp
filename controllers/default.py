# -*- coding: utf-8 -*-
#########################################################################
#Finnish Vakioveikkaus odds comparison application. Veikkaus.fi odds are
#compared with betfair.com odds and over/under-played targets are highlighted
#########################################################################

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import mechanize
from mechanize import Browser

HEADER = {'User-Agent':'Mozilla/5.0'}
ENCODING = 'utf-8'
ELEMENT_NUM = 52
VEIKKAUS_URL = "https://www.veikkaus.fi/mobile?area=wagering&game=sport&op=frontpage"
VEIKKAUS_LINK_TEXT = 'Pelatuimmuusprosentit'
PREMIER_URL = 'http://www.betfair.com/exchange/football/competition?id=31'
CHAMPIONSHIP_URL = 'http://www.betfair.com/exchange/football/competition?id=33'
#elements
ELE_ODDS_ENG = 'price'
ELE_HOME_ENG = 'home-team'
ELE_AWAY_ENG = 'away-team'
ELE_ODDS_FIN = 'td'

#helper functions
#check if the team name includes two words
#if so, take the first initials to create concatenated team name
#these names are used to find the correct premier/championship
#match names (== finnish vakio team names)
def createTeamName(name):
    #special cases: Nottigham Forest
    if name[0:4] == 'Nott':
        teamName = 'No'
    #normal cases
    else:
        nameList = []
        if ' ' in name:
            nameList = name.split(' ')
            teamName = nameList[0][0] + nameList[1][0]
        else:
            teamName = name[0:2]
    return teamName

#return html page as a beautifulsoup object
def getPage(url):
    hdr = HEADER
    req = urllib2.Request(url, headers=hdr)
    try:       
        page = urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        session.code = e.code
        redirect(URL('default', 'httpError'))
    else:
        return BeautifulSoup(page.read())
        

#get games and corresponding odds from english site and put them into dictionary    
def getGamesAndOddsEng(url):
    #html page as a beautifulsoup object
    page = getPage(url)
    try:
        #find games odds
        odds = page.findAll('span', {'class':ELE_ODDS_ENG})
    except:
        session.element = ELE_ODDS_ENG
        redirect(URL('default', 'elementError')) 
    try:    
        #find home team names
        homeTeams = page.findAll('span', {'class':ELE_HOME_ENG})
    except:
        session.element = ELE_HOME_ENG
        redirect(URL('default', 'elementError'))        
    try:   
        #find away team names
        awayTeams = page.findAll('span', {'class':ELE_AWAY_ENG})
    except:
        session.element = ELE_AWAY_ENG
        redirect(URL('default', 'elementError')) 
  
    #take every other element of the odds list
    #(original page includes two odds per game case (1,x,2), take always the first one)
    tmp = odds[0::2]
    oddsList = []
    #parse odds numbers (strings) into list
    for idx in range(len(tmp)):
        oddsNum = tmp[idx].string.strip().encode(ENCODING)
        oddsList.append(oddsNum)
    #create odds tuples, 3 odds per game (1,x,2)
    gameOdds = zip(*[iter(oddsList)] * 3)
    #create games list, including home and away team names
    nameList = []
    for idx in range(len(homeTeams)):
        homeTeam = homeTeams[idx].string.strip().encode(ENCODING)
        awayTeam = awayTeams[idx].string.strip().encode(ENCODING)
        gameString = createTeamName(homeTeam) + ' - ' + createTeamName(awayTeam)
        nameList.append(gameString)
    #create games dictionary including game names and corresponding odds
    return dict(zip(nameList, gameOdds))

#get games and corresponding odds from finnish site and put them into dictionary    
def getGamesAndOddsFin(url):
    br = Browser()
    #site demands a user-agent that isn't a robot
    br.addheaders = [('User-agent', 'Firefox')]
    #retrieve veikkaus vakio mobile home page and browse to game percent page
    #and store the page
    try:
        br.open(url)
    except (mechanize.HTTPError, mechanize.URLError) as e:
        session.code = e.code
        redirect(URL('default', 'browserError'))      
    for link in br.links():
        siteMatch = re.compile(VEIKKAUS_LINK_TEXT).search(link.text)
        if siteMatch:
            resp = br.follow_link(link)
            result = resp.get_data()
            break
    #html page as a beautifulsoup object
    page = BeautifulSoup(result)
    #find games names and odds
    try:
        gameData = page.findAll(ELE_ODDS_FIN)
    except:
        session.element = ELE_ODDS_FIN
        redirect(URL('default', 'elementError'))  
    #full names   
    nameList = []
    #concatenated names used to select the correct names from betfair data
    refNamesFin = []
    #full name + odds
    oddsList = []
    #parse game names (first 13 games) into list
    #4 elements per row and 13 rows => 52
    for idx in range(ELEMENT_NUM):
        if idx%4 == 0:
            gameName = gameData[idx].string.strip().encode(ENCODING)
            #full team names
            nameList.append(gameName)
            teamNames = gameName.split(' - ')
            gameString = createTeamName(teamNames[0]) + ' - ' + createTeamName(teamNames[1])
            #concatenated team names
            refNamesFin.append(gameString)
        else:
            gameOdds = gameData[idx].string.strip().encode(ENCODING)
            #calculate odds from game percents and limit decimal places
            oddsList.append('{0:.2f}'.format(100/float(gameOdds))) 
    #create odds tuples, 3 odds per game (1,x,2)
    gameOdds = zip(*[iter(oddsList)] * 3)
    #create games dictionary including game names and corresponding odds
    return (nameList, gameOdds, refNamesFin)

#exception handlers
def httpError():
    return HTML(BODY(B(session.code)))

def elementError():
    return HTML(BODY(B('Element Not Found: ' + session.element)))

def browserError():
    return HTML(BODY(B(session.code)))

def overlappingNames():
    return HTML(BODY(B('Overlapping Names !')))
   

#controller
def index():
    #get premier league/championship matches and odds from betfair.com
    preGames = getGamesAndOddsEng(PREMIER_URL)
    chaGames = getGamesAndOddsEng(CHAMPIONSHIP_URL)
    allGamesEng = dict(preGames, **chaGames)
    #check that there are no overlapping game names
    try:
        if len(preGames)+len(chaGames) != len(allGamesEng): raise Exception #assert len(preGames)+len(chaGames) == len(allGamesEng), 'Virhe, nimikonflikti !'
    except Exception as e:
        redirect(URL('default', 'overlappingNames'))    
    #from vakio site: Full team names, odds and concatenated team names
    teamNamesFin, gameOddsFin, refNamesFin = getGamesAndOddsFin(VEIKKAUS_URL)
    #get corresponding odds from betfair games
    gameOddsEng = []
    for game in refNamesFin:
        gameOddsEng.append(allGamesEng[game])
    return dict(teamNamesFin=teamNamesFin,
                gameOddsFin=gameOddsFin,
                gameOddsEng=gameOddsEng)
