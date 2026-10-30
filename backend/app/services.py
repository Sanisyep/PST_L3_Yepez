from . import store
from .schemas import LecturaEntrada, ComandoLED

def guardar_lectura(datos: LecturaEntrada) -> dict:
    lectura = datos.model_dump()
    store.lecturas.append(lectura)
    # Conservamos como máximo las últimas 100 lecturas recibidas.
    del store.lecturas[:-100]
    return {"lectura": lectura, "led": store.estado_led["color"]}

def listar_lecturas() -> list[dict]:
    return store.lecturas

def consultar_led() -> dict:
    return store.estado_led

def cambiar_led(comando: ComandoLED) -> dict:
    store.estado_led["color"] = comando.color
    return store.estado_led

def promedio(n):
    a = store.lecturas[-n:]

    if len(a) == 0:
        return None
    
    canti = len(a)

    temp_suma = sum(b["temperatura"] for b in a)
    humed_suma = sum(b["humedad"] for b in a)

    promedio_temp = temp_suma/a
    promedio_humd = humed_suma / a

    return {
        "cantidad": canti,
        "temperatura_promedio": round(promedio_temp, 2),
        "humedad_promedio": round(promedio_humd, 2)
    }

