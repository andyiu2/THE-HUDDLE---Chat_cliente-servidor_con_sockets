
# 💬 Chat Cliente-Servidor con Sockets y Hilos en Python

Este proyecto implementa un **chat cliente-servidor** usando **sockets TCP** y **hilos (threading)** en Python.  

Permite que múltiples clientes se conecten simultáneamente a un servidor, se identifiquen con un nombre y envíen mensajes en tiempo real.

Incluye **reconexión automática del cliente** y manejo básico de errores usando `Exception`.

---

## 📌 Funcionalidades principales

### Servidor

- Escucha conexiones TCP en una IP y puerto definidos

- Acepta múltiples clientes simultáneamente

- Usa **un hilo por cliente**

- Solicita un nombre al conectarse

- Reenvía mensajes a todos los clientes conectados (broadcast)

- Detecta desconexiones y limpia recursos correctamente

### Cliente

- Se conecta al servidor mediante TCP

- Permite reconexión automática si el servidor no está disponible

- Mantiene el nombre del usuario entre reconexiones

- Usa un hilo separado para recibir mensajes

- Permite cerrar la conexión escribiendo `close`

---

## 🛠 Tecnologías utilizadas

- Python 3

- Librerías estándar:

  - `socket`

  - `threading`

  - `time`

  - `sys`

No se utilizan librerías externas.

---

## 📂 Estructura del proyecto

chat-sockets/

│\
├── server.py # Servidor de chat con hilos\
├── client.py # Cliente con reconexión automática\
└── README.md # Documentación

---

## ▶️ Cómo ejecutar el proyecto

### 1️⃣ Iniciar el servidor


  python server.py

### servidor quedará escuchando en:

127.0.0.1 : 8000

### 2️⃣ Iniciar uno o más clientes

### En otra terminal:

python client.py

Podés ejecutar el cliente varias veces para simular múltiples usuarios.

### 🧪 Uso del chat

- El servidor solicita un nombre al conectarse
- Los mensajes enviados por un cliente se reenvían a los demás

### Para salir del chat, escribir:

close

## 🧠 Conceptos aplicados

- Programación cliente-servidor
- Sockets TCP
- Comunicación bidireccional
- Concurrencia con hilos
- Manejo de errores con try / except / finally
- Reconexión automática
- Uso de diccionarios para manejar clientes activos

## 🎯 Objetivo académico

### Este proyecto fue desarrollado con fines educativos para practicar:

- Redes y comunicación en Python
- Manejo de múltiples clientes
- Diseño de servidores concurrentes
- Separación de responsabilidades cliente / servidor

## 🚀 Posibles mejoras futuras

- Autenticación de usuarios
- Historial de mensajes
- Comandos especiales (ej: /users)
- Uso de selectors en lugar de hilos
- Manejo más fino de errores
