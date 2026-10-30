# Lab 3 Estructura de un backend

Código base del curso para leer, ejecutar y modificar a mano, sin IA.
Hardware de referencia: NodeMCU ESP8266, DHT11 y LED RGB de cátodo común.
Este proyecto es una propuesta de material base para acompañar la guía.

## Backend en Windows
Desde backend, en una terminal Command Prompt de VS Code:
```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger: http://127.0.0.1:8000/docs
En macOS/Linux: python3 -m venv .venv y usar .venv/bin/python.
Los cinco endpoints base están en app/routes.py. La lista guarda como máximo
100 lecturas en memoria y se pierde al reiniciar. Ejecutar un solo proceso.
POST /lecturas retorna HTTP 201 con {"lectura": {...}, "led": "apagado"}.
PUT /led acepta rojo, verde, azul o apagado. No hay autenticación:
utilizar únicamente en la red de laboratorio autorizada.

## Firmware
Abrir firmware con PlatformIO IDE en VS Code. Copiar include/config.example.h
a include/config.h y completar WiFi, URL con IPv4 del PC e identificador.
Build, Upload y Monitor a 115200 baudios. El ESP envía cada 5 segundos y aplica
el color devuelto por POST /lecturas; PUT /led se refleja en el próximo envío.
Conexiones y pruebas: ver guía. Las dependencias se descargan la primera vez.
No publicar config.h, contraseñas ni tokens.

## Reto
Implementar GET /lecturas/promedio?n=3 a mano; no se incluye la solución.
Devolver cantidad, temperatura_promedio y humedad_promedio (dos decimales).
Validar n de 1 a 100; sin lecturas responder 404; si hay menos de n, usar todas.

## Antes de la sesión
El docente debe probar el firmware en el hardware real y la red del aula,
precargar las herramientas y validar las dependencias en los equipos.
La guía destina 105 minutos a trabajar con el entorno ya preparado.

## Datos
Nombre: Santiago Yepez Rendon
Paralelo: 101

## Objetivo
Comprender el funcionamiento de un backend mediante FastAPI, identificando sus archivos principales, ejecutando peticiones HTTP y comprobando las respuestas desde Swagger.

## Como ejecutar
Para ejecutar el backend, se utilizaron los siguientes comandos desde la carpeta backend:

python -m venv .venv
.venv\Scri
pts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

La API se puede consultar desde:

http://127.0.0.1:8000/docs

## Preguntas
Pregunta 1: ¿Qué función recibe el JSON y cuál lo guarda?
La única función fue post_lectura() en mi archivo routes.py, luego se llama a la funcion guardar_lectura() que lo guarda en service.py almacenandolo en la lista de memoria de store.py.
Pregunta 2: ¿Qué archivo cambiarías para añadir una URL?
El de routes.py que se encarga de definir las rutas de la api agregando otro decorador y una funcion que gestione la peticion.
Pregunta 3: ¿Qué ocurre con las lecturas y el color cuando se reinicia la API? ¿Por qué?
No se guarda, al reiniciar se pierde la información, solo va a estar mientras dure el proceso. Al reiniciar este archivo la luz volvio a estar en apagado y se perdió todos los cambios porque se necesitaría una base de datos para guardarlo.
Pregunta 4: ¿Por qué una petición con JSON bien escrito puede devolver 422? Indica qué archivo define esa validación.
No cumplio con la validación que hemos definido, por lo que la sintaxis no es suficiente. Como no se paso la validación no se modifico, por ejemplo que al cambiar la temperatura fuera de los parámetros se rechazo del código.
Pregunta 5: Explica el recorrido completo de una lectura: ESP8266, ruta, modelo, servicio, almacenamiento y respuesta. ¿En qué momento cambia el LED?
El ESP8266 obtiene la temperatura y la humedad mediante el sensor y envia datos en formato JSON al backend mediante peticion POST a /lecturas. La funcion post_lectura() de routes.py recibe la peticion y el modelo LecturaEntrada de schemas.py valida los datos.
Despues service.py ejecuta la funcion guardar_lectura() que almacena la informacion en la lista store.py, el backend responde con el codigo 201 incluyendo la lectura registrada y el color del LED.
El LED cambia cuando el ESP8266 recibe correctamente la respuesta del POST y aplica el color indicado, si el color se modifica con PUT /led, el cambio se refleja en el dispositivo durante el siguiente envio.

## Resultados de pruebas
GET /lecturas
[
  {
    "dispositivo": "equipo1",
    "temperatura": 15,
    "humedad": 70
  },
  {
    "dispositivo": "equipo2",
    "temperatura": 40,
    "humedad": 50
  }
]

Codigos: 200

GET /led
	
Response body
Download
{
  "color": "apagado"
}

Codigos: 200