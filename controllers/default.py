# -*- coding: utf-8 -*-
#########################################################################
#controller: Reads the database entries and send them to view
#########################################################################
def index():
    #select all entries
    rows = db(db.games.id > 0).select()
    return dict(rows=rows)