# -*- coding: utf-8 -*-
#########################################################################
#controller: Reads the database entries and send them to view
#########################################################################
def index():
    #select all entries
    rows = db(db.games.id > 0).select()
    #create checkboxes to select the game odds
    selForm = SQLFORM(db.checkBox)
    numOfSafes = 0
    numOfPartials = 0
    numOfFulls = 0 
    checkBoxValues = []
    if selForm.validate(keepvalues=True): #process().accepted:
        #checkboxes from view, dict
        checkBoxes = selForm.vars
        #get checkbox values in sorted order 0 -> 38
        #and replace boolean vales with 0/1
        for key in sorted(checkBoxes.keys()):
            if checkBoxes[key]:
                checkBoxValues.append(1)
            else:
                checkBoxValues.append(0)
        #create checkbox values tuples, 
        #3 checkbox values per tuple(1,x,2) (=one game)
        gameOdds = zip(*[iter(checkBoxValues)] * 3)        
        #calculate the number of checked checkboxes per row/game
        for idx in range(len(gameOdds)):
            checkBoxSum = sum(gameOdds[idx])
            #one checked in a row, safe
            if checkBoxSum == 1:
                numOfSafes += 1
            #two checked in a row, partial
            if checkBoxSum == 2:
                numOfPartials += 1
            #three checked in a row, full
            if checkBoxSum == 3:
                numOfFulls += 1
                
    return dict(rows=rows,
                selForm=selForm,
                numOfSafes=numOfSafes,
                numOfPartials=numOfPartials,
                numOfFulls=numOfFulls)