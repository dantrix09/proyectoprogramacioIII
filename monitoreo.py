import random as r
import time as y
from datetime import datetime
historial = []

def monitorearTemp(z):
    ronda = z
    while ronda < 15:
        lista = []
        temperatura = r.randint(0, 10)
        latitud = 10.6543
        longitud = -71.6123
        fechaHora= datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f'temperatura: {temperatura}')
        if 2 < temperatura < 8:
            ronda = 15
            print('TODO BIEN')
        else: 
            ronda += 1
            print(f'ronda: {ronda}')
            if ronda == 15:
                print('ALERTA ROJA')
            y.sleep(60)

        lista.append(fechaHora)
        lista.append(latitud)
        lista.append(longitud)
        lista.append(temperatura)
        historial.append(lista)

        

monitorearTemp(0)
print(historial)