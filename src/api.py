#!/usr/bin/env python
# coding: utf-8
import web
import datetime,json,re,base64,string
import da

urls = (
'/groups',          'Groups',
'/group/(\d+)',     'Group',
'/notes/opened',    'OpenedNotes',
'/notes/deleted',   'DeletedNotes',
'/notes/(\d+)',     'Notes',
'/note/(\d+)',      'Note',
)

app_api = web.application(urls, locals())

def httpmethod_hook():
    '''REST, because some browsers ajax does not support PUT,DELETE method. '''
    web.ctx.method = web.input().get("__method", web.ctx.method)

unauth_urls=('/login','/register','/getpwd')
def auth_hook():
    '''except urls: /login, /register, /getpwd'''
    path = web.ctx.path
    if any(url in path for url in unauth_urls):
        return
    web.ctx.currentuserid = authenticate()

def json_hook():
    '''should we foce all the response is json, or only the GET method ?'''
    web.header('Content-Type', 'application/json')
    #how to get the result and output via json?

app_api.add_processor(web.loadhook(auth_hook))
app_api.add_processor(web.loadhook(httpmethod_hook)) #has order ?
app_api.add_processor(web.unloadhook(json_hook))


################### common function ###########################

class ExtendedEncoder(json.JSONEncoder):
    '''http://stackoverflow.com/questions/6182967/how-to-format-a-mysql-query-into-json-using-webpy'''
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder(self, o)

def authenticate():
    '''http://webpy.org/cookbook/userauthbasic'''
    uid = False
    auth = web.ctx.env.get('HTTP_AUTHORIZATION')
    authreq = False
    if auth is None:
        authreq = True
    else:
        auth = re.sub('^Basic','',auth)
        uid,secretkey=base64.decodestring(auth).split(':')
        if not da.user.auth(uid,secretkey):
            authreq = True
    if authreq:
        web.header('WWW-Authenticate','Basic realm="Unauthorized!"')
        raise web.unauthorized()
    return uid

def getgroup(gid,uid):
    group = da.groups.read(gid,uid)
    if not group:
        raise web.notfound()
    else:
        return group

def getnote(nid,uid):
    note = da.notes.read(nid,uid)
    if not note:
        raise web.notfound()
    else:
        return note

#########  rest api, need authenticate  #######################
class Login:
    def POST(self):
        i = web.input()
        usr = da.user.login(i.email,i.password)
        if not usr:
            raise web.unauthorized()
        usr = {id:usr.id, secretkey:usr.secretkey}
        web.header('Content-Type', 'application/json')
        return json.dumps(usr)

class Groups:
    def GET(self):
        groups = da.groups.filter(userid=web.ctx.currentuserid)
        return json.dumps(groups)

class Group:
    def GET(self,id):
        group = getgroup(id,web.ctx.currentuserid)
        return json.dumps(group,cls=ExtendedEncoder)

    def POST(self,id):
        i = web.input()
        i.userid = web.ctx.currentuserid
        gid = da.groups.create(i)
        return gid  #json or not?

    def PUT(self,id):
        group = getgroup(id,web.ctx.currentuserid)  #it's the wasted to get full group info to validate the owner? use cache
        i = web.input()
        i.id = id
        da.groups.update(i)
        return id

    def DELETE(self,id):
        group = getgroup(id,web.ctx.currentuserid)
        da.groups.delete(id)

class Notes:
    def GET(self,gid):
        uid = web.ctx.currentuserid
        #gid if int, group
        #if string, merge OpenedNotes/DeletedNotes into this function.
        if string.atoi(gid) > 0:
            group = getgroup(gid,uid)
            notes = da.notes.group(gid)
        else:
            notes = da.notes.all(uid) #all notes of current user

        return json.dumps(notes) #,cls=ExtendedEncoder

class OpenedNotes:
    def GET(self):
        notes = da.notes.opened(web.ctx.currentuserid)
        return json.dumps(notes)

    def POST(self):
        ## StringIO.StringIO(web.data())
        d = web.data()
        pass

class DeletedNotes:
    def GET(self):
        notes = da.notes.deleted(userid=web.ctx.currentuserid)
        return json.dumps(notes)

class Note:
    def GET(self,id):
        note = getnote(id,web.ctx.currentuserid)
        return json.dumps(note,cls=ExtendedEncoder)

    def POST(self,id):
        uid = web.ctx.currentuserid
        i = web.input()
        gid = string.atoi(i.groupid)
        if gid > 0:
            group = getgroup(gid,uid)
        else:
            pass ##how to get the default group id?
        nid = da.notes.create(uid,gid,i.notes)
        return nid;


    def PUT(self,id):
        uid = web.ctx.currentuserid
        note = getnote(id,uid) ##is note owner
        i = web.input()
        if note.groupid != i.groupid:
            gid = string.atoi(i.groupid)
            if gid > 0:
                group = getgroup(gid,uid) ##is group owner
            else:
                pass ##how to get the default group id?

        i.id = id
        da.notes.update(i)
        return id

    def DELETE(self,id):  ##delete from normal or trash?
        note = getnote(id,web.ctx.currentuserid)
        if note.status == 1:
            da.notes.setdel(id)
        else:
            da.notes.setdel(id) ##?
        return
