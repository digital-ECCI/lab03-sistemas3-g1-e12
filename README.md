Lab03: Visualización Interactiva de Datos en Raspberry Pi (Python + Matplotlib)Este proyecto implementa un sistema de monitoreo de distancia en tiempo real utilizando una Raspberry Pi Zero 2W y un sensor ultrasónico HC-SR04. La solución integra la adquisición de datos de hardware con una interfaz gráfica dinámica e interactiva.🛠️ Requerimientos de HardwareComponenteFunciónEspecificaciónRaspberry Pi Zero 2WCerebro del sistemaLinux OS + Python Sensor HC-SR04Medición de distanciaRango: $2cm$ a $400cm$ Resistencias (1k $\Omega$ y 2k $\Omega$)Divisor de tensiónProtege el GPIO (5V $\rightarrow$ 3.3V)Protoboard y JumpersConexión físicaInterfaz de prototipado Esquema de Conexión (Divisor de Tensión)Dado que el sensor HC-SR04 opera a $5V$ y los pines GPIO de la Raspberry Pi solo toleran $3.3V$, es obligatorio usar un divisor de tensión en el pin ECHO.Diagrama ConceptualHC-SR04 (ECHO) ---- ----+---- GPIO 24 (Input)||GNDCálculo del Voltaje de Salida ($V_{out}$)Utilizamos la fórmula del divisor resistivo para asegurar que la señal sea segura:$$V_{out} = V_{in} \cdot \frac{R_2}{R_1 + R_2}$$$$V_{out} = 5V \cdot \frac{2000 \Omega}{1000 \Omega + 2000 \Omega} \approx 3.33V$$💻 Implementación de SoftwareEl código utiliza el modo interactivo de Matplotlib (plt.ion()) para actualizar la gráfica sin bloquear el flujo principal de ejecución.Pythonimport RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

# Configuración de Pines
TRIG, ECHO = 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Inicialización de Datos
tiempos, distancias =,
plt.ion() # Modo interactivo activo
fig, ax = plt.subplots()
inicio = time.time()

# Ciclo de Adquisición
try:
    while True:
        # Lógica del pulso ultrasónico y medición
        #... (ver código fuente completo)...
        
        # Actualización de la Gráfica
        ax.clear()
        ax.plot(tiempos, distancias)
        plt.pause(0.01) # Refresco visual interactivo
except KeyboardInterrupt:
    GPIO.cleanup()
 Análisis Teórico (Cuestionario)1. ¿Qué función cumple plt.fignum_exists?Verifica si la ventana de la gráfica sigue abierta. Si el usuario cierra la ventana manualmente, esta función devuelve False, permitiendo que el script se detenga o reinicie la figura sin lanzar errores de "objeto destruido".2. time.sleep(self.intervalo) vs quitarloEl sleep estabiliza la frecuencia de muestreo. Si se quita, el procesador intentará leer el sensor a máxima velocidad, lo que genera:Sobrecalentamiento innecesario del CPU.Ruido por ondas ultrasónicas residuales que no han terminado de disiparse.3. Ventaja de usar __init__Permite inicializar el estado inicial del objeto (pines, listas de datos, variables de tiempo) automáticamente al crear la instancia. Esto garantiza que el hardware esté configurado correctamente antes de llamar a cualquier método de medición.4. ¿Qué mide self.inicio = time.time()?Establece una marca de tiempo de referencia (tiempo cero). Esto permite que el eje X de la gráfica represente el "tiempo transcurrido desde el inicio" en lugar de la hora absoluta del sistema.5. ¿Qué hace subprocess.check_output(...)?Ejecuta comandos del sistema Linux desde Python y captura su salida. Se usa comúnmente para obtener la temperatura del CPU mediante vcgencmd measure_temp.6. Tiempo relativo vs Tiempo absolutoSe almacena ahora = time.time() - self.inicio porque es más intuitivo visualizar una gráfica que comienza en $0s$ y avanza progresivamente, en lugar de usar marcas de tiempo Unix largas y difíciles de leer.7. ¿Por qué usar self.ax.clear()?Limpia los ejes antes de dibujar el nuevo conjunto de datos. Sin esto, cada nueva línea se dibujaría encima de la anterior, creando un "manchón" de datos en lugar de una línea dinámica limpia.8. El bloque try...except en leer_temperatura()Captura errores de comunicación o fallos del sistema al consultar el hardware. Si el comando del sistema falla, el bloque except evita que el programa principal se cierre, permitiendo que el sistema siga funcionando o reporte el error.9. Modificación para guardar en CSVPara guardar los datos, se debe importar el módulo csv e implementar la apertura en modo a (append):Pythonimport csv
with open('datos_distancia.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow([tiempo_actual, distancia]) # Escribe fila sin borrar anteriores
El modo 'a' es crítico para no sobrescribir el historial cada vez que se toma una medida.🚀 Guía de UsoConectar por SSH a la Raspberry Pi.Habilitar VNC para ver la interfaz gráfica remota.Ejecutar desde VS Code mediante la extensión Remote-SSH.Cerrar la ventana de Matplotlib para finalizar el proceso de forma segura.