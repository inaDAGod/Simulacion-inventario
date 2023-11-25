import simpy
import random

class Producto:
    def __init__(self, env, demanda, costo_pedido, costo_almacenamiento):
        self.env = env
        self.demanda = demanda
        self.costo_pedido = costo_pedido
        self.costo_almacenamiento = costo_almacenamiento
        self.stock = 0
        self.orden_pendiente = False
        self.env.process(self.revisar_inventario())

    def revisar_inventario(self):
        while True:
            if self.stock < self.demanda and not self.orden_pendiente:
                self.orden_pendiente = True
                self.env.process(self.realizar_pedido())

            yield self.env.timeout(1)

    def realizar_pedido(self):
        yield self.env.timeout(3)  # Tiempo que tarda en llegar el pedido
        self.stock += self.demanda
        self.orden_pendiente = False

class Inventario:
    def __init__(self, env):
        self.env = env
        self.productos = []
        self.env.process(self.gestion_inventario())

    def gestion_inventario(self):
        # Definir los parámetros de cada producto (demanda, costos, etc.)
        demandas = [100, 150, 200, 120, 180, 90]
        costos_pedido = [50, 60, 70, 55, 65, 45]
        costos_almacenamiento = [2, 3, 4, 2.5, 3.5, 1.8]

        # Crear y agregar los productos al inventario
        for i in range(len(demandas)):
            producto = Producto(self.env, demandas[i], costos_pedido[i], costos_almacenamiento[i])
            self.productos.append(producto)

def ejecutar_simulacion():
    env = simpy.Environment()
    inventario = Inventario(env)
    env.run(until=100)  # Ejecuta la simulación durante 100 unidades de tiempo

ejecutar_simulacion()
