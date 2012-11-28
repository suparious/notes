#!/usr/bin/env python
# coding: utf-8
import web
import api

pre='controls.'

urls=(
 "/api", api.app_api,

'/',pre+'Index',
'/ipad',pre +'iPad',
'/login',pre+'Login',
'/logout',pre +'Logout'
)

app = web.application(urls,globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'islogin':False,'usr':None})
    web.template.Template.globals['context'] = session
    web.config._session = session

if __name__ =='__main__':
    app.run()

