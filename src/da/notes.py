#!/usr/bin/env python
# coding: utf-8
from util import db,isint,isbigint,isvarchar,isdate,istext,issmallint
from datetime import datetime

is_debug=False

####### notes  ######
def create(uid,gid,content):
    isbigint(uid)
    isbigint(gid)
    istext(gid)
    summary = content[:150]

    return db.insert('notes',
                groupid=gid,userid=uid,notes=content,summary= summary,createdate=datetime.now(),status=1,
                _test=is_debug)

def update(i):
    isbigint(i.id)
    isbigint(i.groupid)
    istext(i.notes)
    i.summary = i.notes[:150]
    id = i.id
    db.update('notes',where='id=$id',
            groupid=i.groupid,notes=i.notes,summary=i.summary,
            vars=locals(),_test=is_debug)

def setstatus(id,status):
    isbigint(id)
    issmallint(status)
    db.update('notes',where='id=$id', status = status, vars=locals(),_test=is_debug)

def setdel(id):
    isbigint(id)
    setstatus(id,0)

def delete():
    db.delete('notes',where='status=0',_test=is_debug)

def read(id,uid):
    isbigint(id)
    isbigint(uid)
    results = db.select('notes',where='id=$id and userid=$uid',vars=locals(), _test=is_debug)
    if not results:
        return False
    return results[0]

def save(i):
    if read(i.id):
        update(i)
    else:
        create(i)

def all(uid):
    return list(db.select('notes', what='id,summary',
            where='userid=$uid and status=1', order="openorder",vars=locals(), _test=is_debug))

def group(gid):
    return list(db.select('notes', what='id,summary',
            where='groupid=$gid and status=1', order="openorder",vars=locals(), _test=is_debug))

def opened(uid):
    return list(db.select('notes', what='id,summary',
            where='userid=$uid and openorder>0', order="openorder",vars=locals(), _test=is_debug))

def deleted(uid):
    return list(db.select('notes', what='id,summary',
            where='userid=$uid and status=0', order="openorder",vars=locals(), _test=is_debug))

def filter(**fields):
    filters = ' and '.join(['%s=%s' % (key,fields[key]) for key in fields])
    return list(db.select('notes', what='id,summary',
            where=filters, order="lastmodifieddate desc",  _test=is_debug))


