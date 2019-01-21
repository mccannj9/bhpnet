# BHPNet Tool 

A program for accessing a simple terminal for executing bash commands over a
server. The programs uses sockets and a Terminal server is implemented, which
executes commands via the subprocess module of Python3. The Terminal user
simply connects to the IP and port where the server is listening and then the
connection drops directly into a simple prompt which can be used to send
commands to the server.


### To Do
- Create command line utility to choose whether you want to be the terminal
server or the terminal user.
- use readline library to allow terminal user to set history files and go back
through the history using the arrow keys.
- figure out how to change directories, although for most purposes this is not
strictly necessary, since one can, in theory, list the contents of any directory
on the server.
