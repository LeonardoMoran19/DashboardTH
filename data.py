
import mysql.connector  as mc
from datetime import datetime
from datetime import timedelta

tempdata={}
humdata={}
config ={
    'host':'',
    'port': ,
    'user':'',
    'password':'', 
    'database':'',
}    

def actdata():
    now = datetime.now()
    delta = timedelta(minutes=10)
    onehour = now - delta
    cnx = mc.connect(**config)  
    cur = cnx.cursor()
    print("SELECT Sensor, Temperatura, Humedad, Lectura FROM TestTable WHERE Lectura BETWEEN '%s' AND '%s'"%(onehour,now))

    cur.execute("SELECT Sensor, Temperatura, Humedad, Lectura FROM TestTable WHERE Lectura BETWEEN '%s' AND '%s'"%(onehour,now))  
    tempdata.clear()
    humdata.clear()
    for (Sensor, Temperatura, Humedad, Lectura) in cur:
        time=datetime.strptime(Lectura.strftime("%H:%M:%S"),"%H:%M:%S")
        tempdata.update({time:Temperatura})
        humdata.update({time:Humedad})
    cur.close()
    cnx.close()
    
    

def obtdata(fecha):
    cnx = mc.connect(**config)  
    cur = cnx.cursor()
    cur.execute("SELECT Sensor, Temperatura, Humedad, Lectura FROM TestTable WHERE Lectura BETWEEN '%s 00:00:00' AND '%s 23:59:59'"%(fecha,fecha))  
    tempdata.clear()
    humdata.clear()
    for (Sensor, Temperatura, Humedad, Lectura) in cur:
        time=datetime.strptime(Lectura.strftime("%H:%M:%S"),"%H:%M:%S")
        tempdata.update({time:Temperatura})
        humdata.update({time:Humedad})
    cur.close()
    cnx.close()


   

