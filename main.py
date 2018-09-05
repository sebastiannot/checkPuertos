#!/usr/bin/python
import sys
import socket
import time
import datetime
import logging
from termcolor import colored, cprint
import smtplib
contadorCorreo = 0
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("sorrego@tsensor.cl", "password")
 
logger = logging.getLogger('checkPuertos')
hdlr = logging.FileHandler('/home/checkPuertos.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)
socketOwa = "IPOWA"
socketGps = "IPGPS"
web = 80
tomcat = 8080
skynet2 = "IP SERVIDOR"
puertos = [socketOwa,socketGps,web,tomcat]
numeroPuertos = len(puertos)
now = datetime.datetime.now()
def checkPuerto(servidor,puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.send(">test string<")
    sock.settimeout(2)
    result = sock.connect_ex((skynet2,puerto))
    
    if result == 0:
        sock.send('>test string<')
        print "{} {} {}".format("PUERTO", puerto ,colored('OK!', 'green', attrs=['reverse', 'blink']))
        estado = True
    else:
        print "{} {} {}".format("PUERTO", puerto ,colored('CERRADO! , ERROR :'+str(result), 'red', attrs=['reverse', 'blink']))
        logger.error("{} {} {}".format("PUERTO", puerto ,str(result)))
        estado = False
    return estado

def enviarCorreo(puerto):
    now = datetime.datetime.now()
    horaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    msg = "Se verifico que el puerto {} se encuentra cerrado , verificar estado del servidor  ".format(puerto)
    server.sendmail("sorrego@tsensor.cl", "sebastian.orrego@fleischmann.cl", msg)

while True:
    now = datetime.datetime.now()
    print "=================== {} ====================".format(now.strftime("%Y-%m-%d %H:%M:%S"))
    puertos = [socketOwa,socketGps,web,tomcat]
    contador = 0

    for puerto in puertos:
        if checkPuerto(skynet2,puerto):
            #print "{} {}".format(puerto,"OK")
            contador+=1
        else:
            pass
            #print "{} {}".format(puerto,"NO OK")
    if contador==numeroPuertos:
        contadorCorreo = 0
    else:
        enviarCorreo(puerto)
    time.sleep(600)
    


