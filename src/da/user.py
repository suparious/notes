#!/usr/bin/env python
# coding: utf-8
from util import db,isint,isbigint,isvarchar,isdate,istext,issmallint
from datetime import datetime

is_debug=False

####### users  ######
def register(i):
    isvarchar(i.email,1,50)
    isvarchar(i.password,1,100)

    return db.insert('users',
                id=i.id,email=i.email,password=i.password,registerdate=datetime.now(),status=1,
                _test=is_debug)

def login(email,password):
    users = db.select('users',where='email=$email',vars=locals(), _test=is_debug)
    if not users:
        return False
    user = users[0]

    if user.password != password:
        return False

    return user

def auth(uid,secretkey):
    users = db.select('users',where="id=$uid and secretkey=$secretkey",vars=locals(), _test=is_debug)
    return users


def changepwd(i):
    isbigint(i.id)
    isvarchar(i.email,1,50)
    isvarchar(i.password,1,100)
    isdatetime(i.registerdate)
    isdatetime(i.lastlogindate)
    issmallint(i.status)
    id = i.id
    db.update('users',where='id=$id',
            id=i.id,email=i.email,password=i.password,registerdate=i.registerdate,lastlogindate=i.lastlogindate,status=i.status,
            vars=locals(),_test=is_debug)

def setstatus(id,status):
    db.update('users',where='id=$id', status = status, vars=locals(),_test=is_debug)
