import simpy
import random
import math

class Producto:
    def __init__(self, env, nombre, demanda_media, desviacion_demanda, costo_pedido, costo_almacenamiento, cantidad_inicial):
        self.env = env
        self.nombre = nombre
        self.demanda_media = demanda_media
        self.desviacion_demanda = desviacion_demanda
        self.costo_pedido = costo_pedido
        self.costo_almacenamiento = costo_almacenamiento
        self.stock = cantidad_inicial
        self.orden_pendiente = False
        self.env.process(self.gestion_inventario())

    def gestion_inventario(self):
        print(f"Inicia simulación para {self.nombre}")
        while True:
            cantidad_pedido = self.calcular_cantidad_pedido()
            if cantidad_pedido > 0:
                self.orden_pendiente = True
                self.env.process(self.realizar_pedido(cantidad_pedido))
                print(f"Realizando pedido para {self.nombre} con demanda {cantidad_pedido} con stock {self.stock} (Tiempo: {self.env.now:.2f})")

            yield self.env.timeout(1)

    def realizar_pedido(self, cantidad_pedido):
        yield self.env.timeout(3)  # Tiempo que tarda en llegar el pedido
        self.stock += cantidad_pedido
        self.orden_pendiente = False
        print(f"Pedido recibido para {self.nombre}. Stock actual: {self.stock} (Tiempo: {self.env.now:.2f})")

    def calcular_cantidad_pedido(self):
        # Cálculo del tamaño óptimo de pedido (EOQ)
        cantidad_pedido = math.sqrt((2 * self.demanda_media * self.costo_pedido) / self.costo_almacenamiento)
        return round(cantidad_pedido)

class Inventario:
    def __init__(self, env):
        self.env = env
        self.productos = []
        self.env.process(self.iniciar_simulacion())

    def iniciar_simulacion(self):
        nombres = ["Gafas A", "Gafas B", "Carteras A", "Carteras B", "Gorritos niño", "Sombreros"]
        demandas_medias = [200, 200, 100, 100, 400, 480] #dato de la empresa
        desviaciones_demanda = [25, 25, 15, 15, 35, 45]
        costos_pedido = [17195.95, 17195.95, 8597.97, 8597.97, 34391.89, 41270.27] #k
        costos_almacenamiento = [5, 5, 10, 10, 7, 10] #h
        cantidades_iniciales = [random.randint(50, 200) for _ in range(len(nombres))]
        demandas_generadas = [max(round(random.normalvariate(demanda_media, desviacion)), 0) for demanda_media, desviacion in zip(demandas_medias, desviaciones_demanda)]

        for i in range(len(nombres)):
            producto = Producto(
                self.env, nombres[i], demandas_generadas[i], desviaciones_demanda[i],
                costos_pedido[i], costos_almacenamiento[i], cantidades_iniciales[i]
            )
            self.productos.append(producto)
            yield self.env.timeout(1)

def ejecutar_simulacion():
    env = simpy.Environment()
    inventario = Inventario(env)
    env.run(until=50)  # Detenemos la simulación en el tiempo 50 (puedes ajustarlo)

ejecutar_simulacion()
