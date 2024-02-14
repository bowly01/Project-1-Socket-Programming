import socket
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.37"  # localhost
port = 12345

try:
    client_socket.connect((host, port))

    print(client_socket.recv(1024).decode())

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data, end="")

        guess = input()

        client_socket.send(guess.encode())

        status = client_socket.recv(1024).decode()

        print(status)

        if "WIN" in status or "ERROR" in status:
            break

except ConnectionError as e:
    print("Connection error:", e)
except Exception as e:
    print("Error:", e)

finally:
    client_socket.close()
