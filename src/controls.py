#!/usr/bin/env python
# coding: utf-8
import web
import da

render = web.template.render('templates')

def getuserid():
    if web.config._session.get('usr') is None:
        return False
    return web.config._session.usr.id

class Index:
    def GET(self):
        uid = getuserid()
        if not uid:
            return render.login()
        model = web.storage()
        model.groups = da.groups.filter(userid=uid) #
        model.notes = da.notes.all(uid) #
        model.onotes = da.notes.opened(uid); #common notes
        model.dnotes = da.notes.deleted(uid)
        return render.index(model)

class Pad:
    def GET(self):
        return render.pad()

class Phone:
    def GET(self):
        return render.phone()

class Login:
    def GET(self):
        return render.login()

    def POST(self):
        i = web.input()
        usr = da.user.login(i.email,i.password)
        if not usr:
            raise web.badrequest() #?

        session = web.config._session
        session.islogin = True
        session.usr = usr
        web.setcookie('userid', usr.id, 360000)
        web.setcookie('secretkey', usr.secretkey, 360000)
        raise web.seeother('/')

class Logout:
    def GET(self):
        web.config._session.kill()
        raise web.seeother('/')






