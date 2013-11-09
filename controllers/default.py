# -*- coding: utf-8 -*-
#########################################################################
#controller: Reads the database entries and send them to view
#########################################################################

TEST_RESULT = 15

#convert checkbox values from form to list of tuples for easier calculation
def calcResults(form):
    checkBoxes = form.vars #selForm.vars
    checkBoxValues = []
    #get checkbox values in sorted order 0 -> 38
    #and replace boolean vales with 0/1
    for key in sorted(checkBoxes.keys()):
        if checkBoxes[key]:
            checkBoxValues.append(1)
        else:
            checkBoxValues.append(0)
    #create checkbox values tuples, 
    #3 checkbox values per tuple(1,x,2) (=one game) 
    return(zip(*[iter(checkBoxValues)] * 3))

#custom validation function for checkbox form
#validates that there is no emty rows
def validateCheckboxes(form):
    checkBoxes = calcResults(form)
    for idx in range(len(checkBoxes)):
        checkBoxSum = sum(checkBoxes[idx])
        #zero checked in a row, this is illegal row
        if checkBoxSum == 0:
            form.errors = True
           
def index():
    #select all entries
    rows = db(db.games.id > 0).select()
    #create checkboxes to select the game odds
    selForm = SQLFORM(db.checkBox, submit_button = 'Laske')
    #bot prevention form
    botForm = FORM(XML('<div id=bot>Viisi plus kymmenen (lukuna):</div>'), 
                   INPUT(_name='bot', requires=IS_INT_IN_RANGE(0, 100, error_message='Virheellinen luku!')),
                   P(''),
                   XML('<div id=email>Email:</div>'),
                   INPUT(_name='email', requires=IS_EMAIL(error_message='Virheellinen osoite!')),
                   P(''),
                   INPUT(_name='okButton', _type='submit', _value='Lähetä')
                   )
    numOfSafes = 0
    numOfPartials = 0
    numOfFulls = 0
    #calculate the number of different odds combinations:
    #1 selected in a row = safe (varma),
    #2 selected in a row = partial (osittainvaihdeltu)
    #3 selected in a row = full (tukko)
    #checkboxes from view, dict  
    if selForm.validate(formname='sel', keepvalues=True, onvalidation=validateCheckboxes): 
        gameOdds = calcResults(selForm)
        #calculate the number of checked checkboxes per row/game
        for idx in range(len(gameOdds)):
            checkBoxSum = sum(gameOdds[idx])
            #one checked in a row, safe
            if checkBoxSum == 1:
                numOfSafes += 1
            #two checked in a row, partial
            elif checkBoxSum == 2:
                numOfPartials += 1
            #three checked in a row, full
            else:
                numOfFulls += 1
        #create email message
        messageText = ""
        for idx in range(len(gameOdds)):
            column1 = '1' if gameOdds[idx][0] == 1 else ''
            columnX = 'X' if gameOdds[idx][1] == 1 else ''
            column2 = '2' if gameOdds[idx][2] == 1 else ''
            messageText += '{}. {}{}{}\n'.format(str(idx+1), column1, columnX, column2)         
        #save email message to db
        db2.email.update_or_insert(db2.email.id == 1, message = messageText)
        
    #render email form if bot prevention test passed
    if botForm.process(formname='bot', keepvalues=True).accepted:
        #get captcha number
        testNumber = int(botForm.vars.bot)
        #read message from db
        messageDb = db2(db2.email.id > 0).select()
        #if the result of test is ok, render email form
        if testNumber == TEST_RESULT:
            address = botForm.vars.email
            mail.send(to = [address],
                      subject = 'Rima vakio',
                      message = messageDb[0].message)
                
    return dict(rows=rows,
                selForm=selForm,
                botForm=botForm,
                numOfSafes=numOfSafes,
                numOfPartials=numOfPartials,
                numOfFulls=numOfFulls)