import matplotlib.pyplot as plt
import time
import subprocess

class MonitorTemperaturaRPI:
    def __init__(self, duracion_max=60, intervalo=0.5):
        self.duracion_max = duracion_max  # Ventana máxima de tiempo visible en la gráfica (segundos)
        self.intervalo = intervalo        # Tiempo de espera entre cada lectura (segundos)
        self.tiempos = []                 # Lista que almacena los tiempos de cada lectura
        self.temperaturas = []            # Lista que almacena las temperaturas leídas
        self.inicio = time.time()         # Guarda el momento exacto en que arrancó el programa
        plt.ion()                         # Activa modo interactivo para no bloquear el programa
        self.fig, self.ax = plt.subplots() # Crea la ventana y los ejes de la gráfica

    def leer_temperatura(self):
        try:
            # Ejecuta el comando del sistema y captura su salida como texto
            salida = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            # Limpia el texto eliminando "temp=" y "'C", dejando solo el número
            temp_str = salida.strip().replace("temp=", "").replace("'C", "")
            return float(temp_str)  # Convierte el texto a número decimal y lo retorna
        except Exception as e:
            print("Error leyendo temperatura:", e)  # Muestra el error si el comando falla
            return None  # Retorna None para indicar que la lectura falló

    def actualizar_datos(self):
        ahora = time.time() - self.inicio  # Calcula los segundos transcurridos desde el inicio
        temp = self.leer_temperatura()     # Obtiene la temperatura actual
        if temp is not None:               # Solo guarda el dato si la lectura fue exitosa
            self.tiempos.append(ahora)         # Agrega el tiempo actual a la lista
            self.temperaturas.append(temp)     # Agrega la temperatura actual a la lista
            # Elimina datos más antiguos que la ventana de tiempo permitida
            while self.tiempos and self.tiempos[0] < ahora - self.duracion_max:
                self.tiempos.pop(0)        # Borra el tiempo más antiguo
                self.temperaturas.pop(0)   # Borra la temperatura más antigua

    def graficar(self):
        self.ax.clear()  # Borra la gráfica anterior para redibujar desde cero
        self.ax.plot(self.tiempos, self.temperaturas, color='red')  # Dibuja la línea roja con los datos
        self.ax.set_title("Temperatura CPU Raspberry Pi")  # Título de la gráfica
        self.ax.set_xlabel("Tiempo transcurrido (s)")      # Etiqueta del eje X
        self.ax.set_ylabel("Temperatura (°C)")             # Etiqueta del eje Y
        self.ax.grid(True)                                 # Activa la cuadrícula de fondo
        self.fig.canvas.draw()          # Renderiza los cambios en la ventana
        self.fig.canvas.flush_events()  # Procesa los eventos pendientes de la interfaz gráfica

    def ejecutar(self):
        try:
            # Repite el ciclo mientras la ventana de la gráfica siga abierta
            while plt.fignum_exists(self.fig.number):
                self.actualizar_datos()       # Lee y guarda el nuevo dato
                self.graficar()               # Actualiza la gráfica con los datos recientes
                time.sleep(self.intervalo)    # Espera el intervalo definido antes de repetir
        except KeyboardInterrupt:
            print("Monitoreo interrumpido por el usuario.")  # Ctrl+C detiene el programa limpiamente
        finally:
            # Este bloque siempre se ejecuta al terminar, sin importar cómo
            print("Monitoreo finalizado.")
            plt.ioff()           # Desactiva el modo interactivo
            plt.close(self.fig)  # Cierra la ventana de la gráfica

if __name__ == "__main__":
    monitor = MonitorTemperaturaRPI()  # Crea el objeto monitor con valores por defecto
    monitor.ejecutar()                 # Inicia el monitoreo
