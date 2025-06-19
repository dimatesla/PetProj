"""
Простой TCP Echo-сервер
Автор: Dmitry
Описание:
  Принимает TCP-соединение, читает сообщение от клиента и отправляет его обратно с префиксом "Echo:".
"""

import socket

HOST = "0.0.0.0"  # Принимать соединения на всех интерфейсах
PORT = 9999       # Порт для прослушивания

#Создание TCP сокета
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

print ("Server started on port", PORT, flush=True)
print("Wait for connect...",flush=True)
conn, addr = s.accept()
print("Connected: " , addr,flush=True)


conn.settimeout(10.0)  # максимум 10 секунд на ожидание данных

#Обработка входящих данных
try:
    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            print("Client is silent too long. Timeout.", flush=True)
            break

        if not data:
            print("Client disconnected.", flush=True)
            break

        message = data.decode().strip()
        print("Received:", message, flush=True)
        response = f"Echo: {message}"
        conn.sendall(response.encode())

except KeyboardInterrupt:
    print("Server interrupted by user", flush=True)
finally:
    try:
        conn.close()
    except:
        pass
    s.close()
    print("Server stopped.", flush=True)
