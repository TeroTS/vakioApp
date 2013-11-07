# -*- coding: utf-8 -*-
#########################################################################
#controller: Reads the database entries and send them to view
#########################################################################
def index():
    #select all entries
    rows = db(db.games.id > 0).select()
    #create checkboxes to select the game odds
    #selForm = FORM()
    #for idx in range(len(rows)*3):
        #selForm.append(INPUT(_type='checkbox'))
    selForm = SQLFORM(db.checkBox)
    #selForm.append(INPUT(_type="submit", _value="OK", _name="okButton"))
    #get selected odds
    oddsSelected = []
    numOfSafes = 0
    numOfPartial = 0
    numOfFull = 0
    if selForm.validate(keepvalues=True): #process().accepted:
        odds = selForm.vars
        #calculate sums for each row/game (row/game includes three odds (1,x,2))
        #depending how many odds selected
        #sum = 1: safe (varma)
        #sum = 2: partial (osittain vaihdeltu)
        #sum = 3: full (tukko)
        for idx, key in enumerate(odds):
            if idx % 3 == 0:
                oddsSum = sum(oddsSelected)
                #number of varmat
                if oddsSum == 1:
                    numOfSafes += 1 
                #number of osittain vaihdellut
                if oddsSum == 2:
                    numOfPartial += 1
                #number of tukkokohde
                if oddsSum == 3:
                    numOfFull += 1
                #clear the list and sums
                oddsSelected = []
                numOfSafes = 0
                numOfPartial = 0
                numOfFull = 0
            #is odd selected ?
            if odds[key] == 'on':
                oddsSelected.append(1)       
    
    return dict(rows=rows,
                selForm=selForm)