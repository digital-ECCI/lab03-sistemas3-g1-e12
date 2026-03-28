Lab03: Visualización Interactiva de Datos
Raspberry Pi Zero 2W + Sensor Ultrasónico HC-SR04

Sistema de medición de distancia con visualización gráfica en tiempo real, desarrollado en Python sobre Raspberry Pi. Este proyecto integra hardware y software para monitoreo dinámico con almacenamiento de datos.

| Elemento             | Descripción                       | Conexión                         |
| -------------------- | --------------------------------- | -------------------------------- |
| Raspberry Pi Zero 2W | Ejecución del sistema (SSH / VNC) | —                                |
| Sensor HC-SR04       | Rango: 2 cm – 400 cm              | Trig → GPIO 23<br>Echo → GPIO 24 |
| Resistencia R1       | 1kΩ                               | Divisor de tensión               |
| Resistencia R2       | 2kΩ                               | Divisor de tensión               |

Divisor de Tensión (Importante)

El pin ECHO del sensor trabaja a 5V, mientras que la Raspberry Pi solo soporta 3.3V. Es obligatorio usar un divisor de tensión para evitar daños.

HC-SR04 ECHO (5V)
        │
       R1 (1kΩ)
        │──────── GPIO 24 (3.3V)
        │
       R2 (2kΩ)
        │
       GND

2. Lógica del Software
Flujo del Programa

![mermaid-diagrama.png](mermaid-diagram.png)

import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')

def actualizar_grafica(tiempos, distancias):
    ax.clear()
    ax.plot(tiempos, distancias, color='blue')
    ax.set_title("Monitoreo en Tiempo Real: HC-SR04")
    ax.set_ylabel("Distancia (cm)")
    ax.set_xlabel("Tiempo (s)")
    plt.pause(0.01)

3. Análisis Técnico
Control de Ejecución
plt.fignum_exists(): verifica si la ventana sigue abierta antes de actualizar la gráfica.
time.sleep(intervalo): evita lecturas incorrectas y reduce la carga del CPU.
Arquitectura
init:
Inicializa automáticamente el hardware y estructuras de datos.

Tiempo relativo:

tiempo_actual = time.time() - inicio

Permite que la gráfica comience desde 0 segundos.

Integración con el Sistema

subprocess.check_output():
Permite ejecutar comandos del sistema como:

vcgencmd measure_temp
ax.clear():
Limpia la gráfica antes de redibujar para evitar acumulación de datos.

4. Persistencia de Datos

Guardado de mediciones en archivo CSV:

import csv
import time

def guardar_datos(distancia):
    with open('log_distancias.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([time.ctime(), distancia])

El modo 'a' agrega datos al final sin sobrescribir el archivo existente.

5. Ejecución
Conectarse por SSH
Abrir entorno gráfico con VNC
Abrir el proyecto en VS Code (Remote SSH)
Ejecutar:
python3 lab03_sensor.py
Interactuar con el sensor y observar la gráfica en tiempo real

Resultados Esperados
Visualización gráfica en tiempo real
Medición continua de distancia
Registro automático en archivo CSV

Integrantes

Daniel Duarte 
Juan David Romero 
Sharom Cortes 
