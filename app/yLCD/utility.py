import configparser
import pprint 
import unicodedata
import sys, os
import pika
import json

def konstantes(name,key):
    arqini     = "/srv/mautec/www/yLCD/config.ini"
    config     = configparser.ConfigParser()
    config.read (arqini)
    if name in config:
        Result = config[name][key]
        return Result
    else:
        raise Exception()

def sendMessage(queue, message, exch_type = 'direct'):
    connectURL   = konstantes('PIKA', 'url')
    parametros   = pika.URLParameters(connectURL)
    connect      = pika.BlockingConnection(parametros)
    channel      = connect.channel()

    if exch_type == 'direct':
        exchange = konstantes('PIKA', 'exchange_direct')
        channel.queue_declare (queue = queue)
        channel.exchange_declare (exchange=exchange, exchange_type='direct')
        channel.queue_bind       (exchange=exchange, queue=queue)
        channel.basic_publish    (exchange=exchange, routing_key=queue, body=message)
    else:    
        exchange = konstantes('PIKA', 'exchange_fanout')
        channel.exchange_declare (exchange=exchange, exchange_type='fanout')
        channel.basic_publish    (exchange=exchange, routing_key='', body=message)
        

def getOneMessage (exchange, queue):
    connectURL   = konstantes('PIKA', 'url')
    parametros   = pika.URLParameters(connectURL)
    connect      = pika.BlockingConnection(parametros)
    channel      = connect.channel()
    if queue == None:
        result     = channel.queue_declare (queue = '', exclusive=True)
        queue_name = result.method.queue
    else:
        queue_name = queue
    channel.queue_bind (exchange=exchange, queue=queue_name)
    method_frame, header_frame, body = channel.basic_get(queue = queue_name)        
    if  (not hasattr(method_frame, 'NAME'))  or method_frame.NAME == 'Basic.GetEmpty':
        connect.close()
        return '{}'
    else:            
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connect.close() 
        return body

def sendLog(api, message):
    data = {  "Api" : api, "Result" : message }
    jmsg = json.dumps(data)
    sendMessage('', jmsg, "fanout")


def showMessage (what):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(what)
