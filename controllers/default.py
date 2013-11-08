# -*- coding: utf-8 -*-
#########################################################################
#controller: Reads the database entries and send them to view
#########################################################################

TEST_RESULT = 15

def index():
    drawEmailForm = False
    #select all entries
    rows = db(db.games.id > 0).select()
    #create checkboxes to select the game odds
    selForm = SQLFORM(db.checkBox)
    #bot prevention form
    #botForm = FORM(TABLE(TR('Viisi plus kymmenen (lukuna):', 
                            #INPUT(_name='bot', requires=IS_INT_IN_RANGE(0, 100, error_message='Virheellinen luku!'))),
                         #TR(INPUT(_name='okButton', _type='submit'))
                         #))
    botForm = FORM(XML('<div id=bot>Viisi plus kymmenen (lukuna):</div>'), 
                   INPUT(_name='bot', requires=IS_INT_IN_RANGE(0, 100, error_message='')),
                   P(''),
                   XML('<div id=email>Email osoite:</div>'),
                   INPUT(_name='email', requires=IS_EMAIL(error_message='Virheellinen osoite!')),
                   P(''),
                   INPUT(_name='okButton', _type='submit')
                   )
    #mail address form
    #emailForm = FORM('Email osoite:', 
                     #INPUT(_name='email', requires=IS_EMAIL(error_message='Virheellinen osoite!')),
                     #P(''),
                     #INPUT(_name='okButton1', _type='submit')
                     #)
    numOfSafes = 0
    numOfPartials = 0
    numOfFulls = 0 
    checkBoxValues = []
    #calculate the number of different odds combinations:
    #1 selected in a row = safe (varma),
    #2 selected in a row = partial (osittainvaihdeltu)
    #3 selected in a row = full (tukko)
    if selForm.validate(formname='sel', keepvalues=True):
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
    #render email form if bot prevention test passed
    if botForm.process(formname='bot', keepvalues=True).accepted:
        testNumber = int(botForm.vars.bot)
        #if the result of test is ok, render email form
        if testNumber == TEST_RESULT:
            address = botForm.vars.email
            mail.send(to=[address],
                      subject='test',
                      message= "Hello this is an email")
                
    return dict(rows=rows,
                selForm=selForm,
                botForm=botForm,
                numOfSafes=numOfSafes,
                numOfPartials=numOfPartials,
                numOfFulls=numOfFulls,
                drawEmailForm=drawEmailForm)