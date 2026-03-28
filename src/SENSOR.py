import matplotlib.pyplot as plt
import time
import RPi.GPIO as GPIO

class MonitorDistanciaRPI:
    def __init__(self, duracion_max=60, intervalo=0.5):
        self.duracion_max = duracion_max  # Ventana máxima de tiempo visible en la gráfica (segundos)
        self.intervalo = intervalo        # Tiempo de espera entre cada lectura (segundos)
        self.tiempos = []                 # Lista que almacena los tiempos de cada lectura
        self.distancias = []              # Lista que almacena las distancias medidas
        self.inicio = time.time()         # Guarda el momento exacto en que arrancó el programa

        # --- Configuración pines GPIO ---
        self.TRIG = 23  # Pin que envía el pulso ultrasónico (salida)
        self.ECHO = 24  # Pin que recibe el eco del pulso (entrada)
        GPIO.setmode(GPIO.BCM)                  # Usa numeración BCM para los pines
        GPIO.setup(self.TRIG, GPIO.OUT)         # Configura TRIG como salida
        GPIO.setup(self.ECHO, GPIO.IN)          # Configura ECHO como entrada
        GPIO.output(self.TRIG, False)           # Asegura que TRIG inicie en LOW
        time.sleep(2)                           # Espera 2 segundos para estabilizar el sensor

        # --- Configuración gráfica ---
        plt.ion()                               # Activa modo interactivo para no bloquear el programa
        self.fig, self.ax = plt.subplots()      # Crea la ventana y los ejes de la gráfica

    def leer_distancia(self):
        # Envía un pulso ultrasónico de 10 microsegundos
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)       # Pulso de 10µs
        GPIO.output(self.TRIG, False)

        inicio = time.time()
        timeout = inicio

        # Espera a que ECHO suba a HIGH (inicio del eco)
        while GPIO.input(self.ECHO) == 0:
            inicio = time.time()
            if inicio - timeout > 0.02:  # Timeout de 20ms para evitar bloqueo infinito
                return None

        fin = time.time()
        timeout = fin

        # Espera a que ECHO baje a LOW (fin del eco)
        while GPIO.input(self.ECHO) == 1:
            fin = time.time()
            if fin - timeout > 0.02:  # Timeout de 20ms para evitar bloqueo infinito
                return None

        duracion = fin - inicio               # Tiempo que tardó el eco en regresar
        distancia = (duracion * 34300) / 2    # Convierte tiempo a cm (velocidad del sonido / 2 por ida y vuelta)
        return distancia

    def actualizar_datos(self):
        ahora = time.time() - self.inicio  # Segundos transcurridos desde el inicio
        dist = self.leer_distancia()       # Obtiene la distancia actual
        if dist is not None:               # Solo guarda si la lectura fue exitosa
            self.tiempos.append(ahora)         # Agrega el tiempo actual a la lista
            self.distancias.append(dist)       # Agrega la distancia actual a la lista
            # Elimina datos más antiguos que la ventana de tiempo permitida
            while self.tiempos and self.tiempos[0] < ahora - self.duracion_max:
                self.tiempos.pop(0)       # Borra el tiempo más antiguo
                self.distancias.pop(0)    # Borra la distancia más antigua

    def graficar(self):
        self.ax.clear()                                      # Borra la gráfica anterior
        self.ax.plot(self.tiempos, self.distancias)          # Dibuja la línea con los datos
        self.ax.set_title("Distancia Sensor HC-SR04")        # Título de la gráfica
        self.ax.set_xlabel("Tiempo (s)")                     # Etiqueta del eje X
        self.ax.set_ylabel("Distancia (cm)")                 # Etiqueta del eje Y
        self.ax.grid(True)                                   # Activa la cuadrícula de fondo
        self.fig.canvas.draw()                               # Renderiza los cambios en pantalla
        self.fig.canvas.flush_events()                       # Procesa eventos pendientes de la interfaz

    def ejecutar(self):
        try:
            # Repite el ciclo mientras la ventana de la gráfica siga abierta
            while plt.fignum_exists(self.fig.number):
                self.actualizar_datos()     # Lee y guarda el nuevo dato
                self.graficar()             # Actualiza la gráfica
                time.sleep(self.intervalo)  # Espera antes de la siguiente lectura
        except KeyboardInterrupt:
            print("Monitoreo detenido por el usuario")  # Ctrl+C detiene limpiamente
        finally:
            # Siempre se ejecuta al terminar, sin importar cómo
            GPIO.cleanup()         # Libera todos los pines GPIO
            plt.ioff()             # Desactiva el modo interactivo
            plt.close(self.fig)    # Cierra la ventana de la gráfica
            print("Programa finalizado")

if __name__ == "__main__":
    monitor = MonitorDistanciaRPI()  # Crea el objeto monitor con valores por defecto
    monitor.ejecutar()               # Inicia el monitoreo
