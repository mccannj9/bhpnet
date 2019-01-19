# BHPNet Tool 

A program for accessing a simple terminal for executing bash commands over a
server. The programs uses sockets and a Terminal server is implemented, which
executes commands via the subprocess module of Python3. The Terminal user
simply connects to the IP and port where the server is listening and then the
connection drops directly into a simple prompt which can be used to send
commands to the server.
