# -*- coding: utf-8 -*-
#########################################################################
#controller: Reads the database entries and send them to view
#########################################################################
def calcSum():
    #take all form variables
    #odds = selForm.vars
    ##clear the list and sums
    #oddsSelected = []
    #numOfSafes = 0
    #numOfPartial = 0
    #numOfFull = 0    
    ##calculate sums for each row/game (row/game includes three odds (1,x,2))
    ##depending how many odds selected
    ##sum = 1: safe (varma)
    ##sum = 2: partial (osittain vaihdeltu)
    ##sum = 3: full (tukko)
    #for idx, key in enumerate(odds):
        #if idx % 3 == 0:
            #oddsSum = sum(oddsSelected)
            ##number of safes
            #if oddsSum == 1:
                #numOfSafes += 1 
            ##number of partials
            #if oddsSum == 2:
                #numOfPartial += 1
            ##number of fulls
            #if oddsSum == 3:
                #numOfFull += 1
        ##is odd selected ?
        #if odds[key] == 'on':
            #oddsSelected.append(1)
    #sumList = []
    #sumList.extend((numOfSafes, numOfPartial, numOfFull))
    #return(sumList)
    return request.vars.test
    
def index():
    #select all entries
    rows = db(db.games.id > 0).select()
    #create checkboxes to select the game odds
    #session.selForm = FORM()
    #for idx in range(len(rows)*3):
    #    session.selForm.append(INPUT(_type='checkbox', _name='%d'%idx, _onclick="ajax('calcSum', ['%d'], 'target')"%idx))
#    if selForm.process().accepted:   
    return dict(rows=rows)
                #selForm=session.selForm)