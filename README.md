# Simulación de Gestión de Inventario en Python

Este proyecto ofrece una simulación de gestión de inventario utilizando **Python** y **SimPy** para modelar y evaluar estrategias de inventario. La simulación está diseñada para entender y optimizar los niveles de inventario en un entorno empresarial.

## Descripción

La simulación se centra en modelar el comportamiento de productos en un inventario a lo largo del tiempo. Se simulan factores como la demanda, tiempos de reorden, costos de almacenamiento y pedido, permitiendo evaluar diversas estrategias para optimizar la gestión del inventario.

## Características
- **Clase Producto:** Modela artículos individuales en el inventario, simulando su comportamiento a lo largo del tiempo.
- **Clase Inventario:** Representa la colección de productos a gestionar.
- **Gestión de Inventario:** Simula el ciclo de vida de los productos, calculando el Punto de Reorden, realizando pedidos cuando es necesario y ajustando el stock según la demanda.

La demanda de los productos se simula utilizando una distribución normal. Esto permite introducir variabilidad en la demanda, reflejando las fluctuaciones naturales que ocurren en entornos empresariales debido a factores como cambios estacionales, preferencias del consumidor y comportamiento del mercado.


