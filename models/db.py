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

#generate check boxes, these are not going to be real 
#db entries. These are here so that SQLFORM can be used in controller =>
#easier to create custom forms
db.define_table('checkBox',
                Field('box0', 'boolean'),
                Field('box1', 'boolean'),
                Field('box2', 'boolean'),
                Field('box3', 'boolean'),
                Field('box4', 'boolean'),
                Field('box5', 'boolean'),
                Field('box6', 'boolean'),
                Field('box7', 'boolean'),
                Field('box8', 'boolean'),
                Field('box9', 'boolean'),
                Field('box10', 'boolean'),
                Field('box11', 'boolean'),
                Field('box12', 'boolean'),
                Field('box13', 'boolean'),
                Field('box14', 'boolean'),
                Field('box15', 'boolean'),
                Field('box16', 'boolean'),
                Field('box17', 'boolean'),
                Field('box18', 'boolean'),
                Field('box19', 'boolean'),
                Field('box20', 'boolean'),
                Field('box21', 'boolean'),
                Field('box22', 'boolean'),
                Field('box23', 'boolean'),
                Field('box24', 'boolean'),
                Field('box25', 'boolean'),
                Field('box26', 'boolean'),
                Field('box27', 'boolean'),
                Field('box28', 'boolean'),
                Field('box29', 'boolean'),
                Field('box30', 'boolean'),
                Field('box31', 'boolean'),
                Field('box32', 'boolean'),
                Field('box33', 'boolean'),
                Field('box34', 'boolean'),
                Field('box35', 'boolean'),
                Field('box36', 'boolean'),
                Field('box37', 'boolean'),
                Field('box38', 'boolean')
                )
