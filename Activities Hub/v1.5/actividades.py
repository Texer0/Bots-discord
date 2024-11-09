import datetime

ACTIVIDADES = {'SERVICIO DE TAXI': [2, 8, 11, 16, 18, 23], 'SERVICIO DE MUDANZA': [0, 4, 13, 17, 19],
               'SERVICIO DE CLIENTE VIP': [9, 14, 19, 22], 'BUS INTERURBANO (RUTA A)': 21, 'BUS INTERURBANO (RUTA B)': 5, 'BUS INTERURBANO (RUTA D)': 15}


def notificador(actividades):
    actividades_datetime = {}

    for key in actividades.keys():
        if isinstance(actividades[key], list):
            horas_datetime = []
            
            for hora in actividades[key]:
                hora_datetime = to_datetime(hora)
                horas_datetime.append(hora_datetime)
                actividades_datetime[key] = horas_datetime
        elif isinstance(actividades[key], int):
            hora_datetime = to_datetime(actividades[key])
            actividades_datetime[key] = hora_datetime
    
    return actividades_datetime

def to_datetime(dato):
    dato = str(dato)
    dato_hora = datetime.datetime.strptime(dato, "%H").time()
    return dato_hora

def hora_actividad(actividades):
    horarios_con_listas = [horario for horario in actividades.values()]
    horario_sin_listas = []
    
    for horario in horarios_con_listas:
        if isinstance(horario, list):
            for dato in horario:
                horario_sin_listas.append(dato)
        elif isinstance(horario, int):
            horario_sin_listas.append(horario)
            
    horario_ordenado = sorted(horario_sin_listas)
    horario_ordenado = list(set(horario_ordenado))
    return horario_ordenado


def tiempo_restante():
    hora_actividades_data = hora_actividad(ACTIVIDADES)
    now = datetime.datetime.now()
    intNowHour = int(now.strftime("%H"))
    intNowMinute = int(now.strftime("%M"))
    print(hora_actividades_data)
    for dato in hora_actividades_data:
        if dato > intNowHour:
            diferencia_horas = dato - intNowHour
            diferencia_minutos = (60 - intNowMinute) * 60
            diferencia = diferencia_horas + diferencia_minutos
            diferencia = abs(diferencia)
            print("Tiempo de espera para la siguiente actividad:", diferencia)
            return diferencia
        
        elif dato == intNowHour:
            diferencia = 60 - intNowMinute
            print(diferencia)
            return diferencia * 60

def get_nombre():
    vuelta = 0
    now = datetime.datetime.now()
    intNowHour = int(now.strftime("%H"))

    for key, actividad_datos in ACTIVIDADES.items():
        vuelta +=1
        if isinstance(actividad_datos, list):
            for dato in actividad_datos:
                if dato == intNowHour:
                    return key

        elif isinstance(actividad_datos, int):
            if actividad_datos == intNowHour:
                return key


actividades_datetime = notificador(ACTIVIDADES)


# print("Return:", tiempo_restante())
print(get_nombre())