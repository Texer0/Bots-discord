import datetime
from variables import ACTIVIDADES_TRANSPORTE, ACTIVIDADES_MECANICO, ACTIVIDADES_SEGURIDAD
import logging
from time import localtime, sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def selection_org(option):
    global actividades
    if option == 'Transporte':
        actividades = ACTIVIDADES_TRANSPORTE
    elif option == 'Mecanico':
        actividades = ACTIVIDADES_MECANICO
    elif option == 'Seguridad':
        actividades = ACTIVIDADES_SEGURIDAD
    print(f"La actividad elegida es: {option}")


def organizar_horarios(actividades):
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
    hora_actividades_data = organizar_horarios(actividades)
    hora_actual = localtime().tm_hour
    minuto_actual = localtime().tm_min
    
    for actividad in hora_actividades_data:
        if actividad > hora_actual:
            horas_faltantes = actividad - hora_actual
            
            print(f"Detalles de horarios:\n Hora: {hora_actual}\n Minuto: {minuto_actual}")
            print(f"\nHorario de la actividad: {actividad}")

            if minuto_actual > 0:
                horas_faltantes -=1
                minutos_faltantes = 60 - minuto_actual
                print(f"Faltan {horas_faltantes} horas y {minutos_faltantes} minutos")
                # return horas_faltantes * 3600 + minutos_faltantes * 60
            else:
                minutos_faltantes = 0
                print(f"Faltan {horas_faltantes} horas y {minutos_faltantes} minutos")
                # return horas_faltantes * 3600
            return actividad - hora_actual
                
            
    for actividad in hora_actividades_data:
        if actividad == 0 or actividad <= hora_actual:
            horas_faltantes = 24 - hora_actual + actividad
            minutos_faltantes = 60 - minuto_actual
            if minutos_faltantes != 0:
                horas_faltantes -= 1
            print(f"Faltan {horas_faltantes} horas y {minutos_faltantes} minutos")
            # return horas_faltantes * 3600 + minutos_faltantes * 60
            return horas_faltantes

def get_nombre(option):
    if option == 'Transporte':
        actividades = ACTIVIDADES_TRANSPORTE

    elif option == 'Mecanico':
        actividades = ACTIVIDADES_MECANICO
    
    elif option == 'Seguridad':
        actividades = ACTIVIDADES_SEGURIDAD

    now = datetime.datetime.now()
    intNowHour = int(now.strftime("%H"))
    
    for key, actividad_datos in actividades.items():
        if isinstance(actividad_datos, list):
            for dato in actividad_datos:
                if dato == intNowHour:
                    print(f"LA KEY ES -> {key}")
                    return key

        elif isinstance(actividad_datos, int):
            if actividad_datos == intNowHour:
                print(f"LA KEY ES -> {key}")
                return key
            
    for key, actividad_datos in actividades.items():
        if isinstance(actividad_datos, list):
            for dato in actividad_datos:
                if dato >= intNowHour:
                    print(f"LA KEY ES -> {key}")
                    return key

        elif isinstance(actividad_datos, int):
            if actividad_datos >= intNowHour:
                print(f"LA KEY ES -> {key}")
                return key
            

# print(f"""El nombre de la actividad es: {get_nombre()}""")