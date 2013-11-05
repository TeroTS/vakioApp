# -*- coding: utf-8 -*-

## configure email
#mail = auth.settings.mailer
#mail.settings.server = 'logging' or 'smtp.gmail.com:587'
#mail.settings.sender = 'you@gmail.com'
#mail.settings.login = 'username:password'

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
