import simpy
import random
import math

class Producto:
    def __init__(self, env, nombre, demanda, demanda_anual, desviacion_demanda, costo_pedido, costo_almacenamiento, cantidad_inicial):
        self.env = env
        self.nombre = nombre
        self.demanda = demanda
        self.demanda_anual = demanda_anual
        self.desviacion_demanda = desviacion_demanda
        self.costo_pedido = costo_pedido
        self.costo_almacenamiento = costo_almacenamiento
        self.stock = cantidad_inicial
        self.orden_pendiente = False
        self.env.process(self.gestion_inventario())

    def gestion_inventario(self):
        print("-----------------------------------------------")
        print(f"Inicia simulación para {self.nombre}")
        while True:
            if self.stock <= self.calcular_punto_reorden() and not self.orden_pendiente:
                cantidad_pedido = self.calcular_cantidad_pedido()
                print(f"EOQ de {self.nombre}:  {cantidad_pedido}")
                if cantidad_pedido > 0:
                    self.orden_pendiente = True
                    self.env.process(self.realizar_pedido(cantidad_pedido))
                    print(f"Realizando pedido para {self.nombre} con demanda actual {self.demanda}, con demanda anual {self.demanda_anual} y stock {self.stock} (Tiempo: {self.env.now:.2f})")
                else:
                    print(f"No es recomendable pedir {self.nombre}")
            else:
                print(f"Se tiene un pedido pendiente de {self.nombre}")

            yield self.env.timeout(1)

    def calcular_punto_reorden(self):
        # Cálculo del punto de reorden (Reorder Point)
        tiempo_entrega = 2
        punto_reorden = (self.demanda_anual/12 )* tiempo_entrega 
        return punto_reorden
    
    def realizar_pedido(self, cantidad_pedido):
        yield self.env.timeout(2)  # Tiempo que tarda en llegar el pedido
        self.stock += cantidad_pedido
        self.orden_pendiente = False
        print(f"Pedido recibido para {self.nombre}. Stock actual: {self.stock} (Tiempo: {self.env.now:.2f})")

    def calcular_cantidad_pedido(self):
        # Cálculo del tamaño óptimo de pedido (EOQ)
        cantidad_pedido = math.sqrt((2 * self.demanda_anual * self.costo_pedido) / self.costo_almacenamiento)
        return round(cantidad_pedido)

class Inventario:
    def __init__(self, env):
        self.env = env
        self.productos = []
        self.env.process(self.iniciar_simulacion())

    def iniciar_simulacion(self):
        nombres = ["Gafas A", "Gafas B", "Carteras A", "Carteras B", "Gorritos niño", "Sombreros"]
        demandas_medias = [200, 200, 100, 100, 400, 480] #dato de la empresa
        desviaciones_demanda = [25, 25, 15, 15, 35, 45] #esto lo cambiamos
        costos_pedido = [17195.95, 17195.95, 8597.97, 8597.97, 34391.89, 41270.27] #k
        costos_almacenamiento = [5, 5, 10, 10, 7, 10] #h
        cantidades_iniciales = [random.randint(10, 20) for _ in range(len(nombres))]#randomizamos cantidades iniciales
        demandas_generadas = [max(round(random.normalvariate(demandas_medias[i], desviaciones_demanda[i])), 0) for i in range(len(nombres))]#generamos demandas siguiente dist normal

        for i in range(len(nombres)):
            producto = Producto(
                self.env, nombres[i], demandas_generadas[i], demandas_medias[i], desviaciones_demanda[i],
                costos_pedido[i], costos_almacenamiento[i], cantidades_iniciales[i]
            )
            self.productos.append(producto)
            yield self.env.timeout(1)

def ejecutar_simulacion():
    env = simpy.Environment()
    inventario = Inventario(env)
    env.run(until=50)  # Detenemos la simulación en el tiempo 50 

ejecutar_simulacion()
