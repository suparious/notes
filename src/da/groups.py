#!/usr/bin/env python
# coding: utf-8
from util import db,isint,isbigint,isvarchar,isdate,istext,issmallint
from datetime import datetime

is_debug=False

####### groups  ######
def create(i):
    isint(i.userid)
    isvarchar(i.name,1,50)

    return db.insert('groups',
                userid=i.userid,name=i.name,createdate=datetime.now(),
                _test=is_debug)

def update(i):
    isint(i.id)
    isvarchar(i.name,1,50)
    id = i.id
    db.update('groups',where='id=$id',name=i.name,
            vars=locals(),_test=is_debug)

def setstatus(id,status):
    db.update('groups',where='id=$id', status = status, vars=locals(),_test=is_debug)

def delete(id):
    setstatus(id,0)

def read(id,uid):
    results = db.select('groups',where='id=$id and userid=$uid',vars=locals(), _test=is_debug)
    if not results:
        return False
    return results[0]

def save(i):
    if i.id < 0:
        return create(i)
    if read(i.id):
        update(i)
    else:
        create(i)

def filter(**fields):
    filters = ' and '.join(['%s=%s' % (key,fields[key]) for key in fields])
    filters += ' and status=1'
    return list(db.select('groups', what='id,name,notescount',
            where=filters, order = 'id', _test=is_debug))
