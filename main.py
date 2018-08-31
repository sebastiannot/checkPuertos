#!/usr/bin/python
import sys
import socket
import time
import datetime
import logging
from termcolor import colored, cprint

logger = logging.getLogger('checkPuertos')
hdlr = logging.FileHandler('/home/checkPuertos.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


socketOwa = 17190
socketGps = 17180
web = 80
tomcat = 8080
#201.219.145.98 
skynet2 = "201.219.145.98"
puertos = [socketOwa,socketGps,web,tomcat]
now = datetime.datetime.now()
def checkPuerto(servidor,puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.send(">test string<")
    sock.settimeout(2)
    result = sock.connect_ex((skynet2,puerto))
    
    if result == 0:
        sock.send('>test string<')
        print "{} {} {}".format("PUERTO", puerto ,colored('OK!', 'green', attrs=['reverse', 'blink']))
    else:
        print "{} {} {}".format("PUERTO", puerto ,colored('CERRADO! , ERROR :'+str(result), 'red', attrs=['reverse', 'blink']))
        logger.error("{} {} {}".format("PUERTO", puerto ,str(result)))
    return result
while True:
    now = datetime.datetime.now()
    print "=================== {} ====================".format(now.strftime("%Y-%m-%d %H:%M:%S"))
    puertos = [socketOwa,socketGps,web,tomcat]
    for puerto in puertos:
        checkPuerto(skynet2,puerto)
        time.sleep(5)
    pass


