# -*- coding: utf-8 -*-
from gluon.tools import Mail

## configure email
mail = Mail()
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'tero.t.suhonen@gmail.com'
mail.settings.login = 'tero.t.suhonen@gmail.com:terorules'

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db = DAL('sqlite://games.db', migrate = False)

db.define_table('games',
   Field('date', 'text'),
   Field('game', 'text'),
   Field('odds_fin_1', 'text'),
   Field('odds_fin_x', 'text'),
   Field('odds_fin_2', 'text'),
   Field('odds_eng_1', 'text'),
   Field('odds_eng_x', 'text'),
   Field('odds_eng_2', 'text'))

#generate check boxes, these are not going to be real 
#db entries. These are here so that SQLFORM can be used in controller =>
#easier to create custom forms
#binary names, easier to sort them later
db.define_table('checkBox',
                Field('box000000', 'boolean'),
                Field('box000001', 'boolean'),
                Field('box000010', 'boolean'),
                Field('box000011', 'boolean'),
                Field('box000100', 'boolean'),
                Field('box000101', 'boolean'),
                Field('box000110', 'boolean'),
                Field('box000111', 'boolean'),
                Field('box001000', 'boolean'),
                Field('box001001', 'boolean'),
                Field('box001010', 'boolean'),
                Field('box001011', 'boolean'),
                Field('box001100', 'boolean'),
                Field('box001101', 'boolean'),
                Field('box001110', 'boolean'),
                Field('box001111', 'boolean'),
                Field('box010000', 'boolean'),
                Field('box010001', 'boolean'),
                Field('box010010', 'boolean'),
                Field('box010011', 'boolean'),
                Field('box010100', 'boolean'),
                Field('box010101', 'boolean'),
                Field('box010110', 'boolean'),
                Field('box010111', 'boolean'),
                Field('box011000', 'boolean'),
                Field('box011001', 'boolean'),
                Field('box011010', 'boolean'),
                Field('box011011', 'boolean'),
                Field('box011100', 'boolean'),
                Field('box011101', 'boolean'),
                Field('box011110', 'boolean'),
                Field('box011111', 'boolean'),
                Field('box100000', 'boolean'),
                Field('box100001', 'boolean'),
                Field('box100010', 'boolean'),
                Field('box100011', 'boolean'),
                Field('box100100', 'boolean'),
                Field('box100101', 'boolean'),
                Field('box100110', 'boolean')
                )
                
                