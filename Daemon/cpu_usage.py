import psutil, time
import httplib, subprocess, urlparse

from bottle import route, run, request

from bottle import get, post, request # or route




while 1:
       print("Memory= "+str(psutil.virtual_memory().available*100/psutil.virtual_memory().total)+ " %")
       time.sleep(1)

# @get('/login') # or @route('/login')
# def login():
#     return '''
#         <form action="/login" method="post">
#             Username: <input name="username" type="text" />
#             Password: <input name="password" type="password" />
#             <input value="Login" type="submit" />
#         </form>
#     '''

# @post('/login') # or @route('/login', method='POST')
# def do_login():
#     username = request.forms.get('username')
#     password = request.forms.get('password')
#     if (username == password):
#     	mem = str(psutil.virtual_memory().available)
#         return "<p>Your login information was correct. {mem} </p>".format(mem=mem)
#     else:
#         return "<p>Login failed.</p>"

# @route('/', method='POST')
# def index():
#     postdata = request.body.read()
#     print(postdata) #this goes to log file only, not to client
#     name = request.forms.get("name")
#     surname = request.forms.get("surname")
#     return "Hi {name} {surname}".format(name=name, surname=surname)

# run(host='localhost', port=8080, debug=True)



# print(psutil.cpu_percent())
# 

