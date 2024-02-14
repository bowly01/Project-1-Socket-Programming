import socket
import random


WORDS = ["BANANA", "ORANGE", "MANGO", "GRAPES", "STRAWBERRY", "WATERMELON", "GUAVA"]

def choose_word():
    return random.choice(WORDS)

def display_word(word, guessed_letters):
    return "".join([letter if letter in guessed_letters else "_" for letter in word])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.37"  # localhost
port = 12345
server_socket.bind((host, port))
server_socket.listen(1)

print("Server is listening on port", port)

word = choose_word()
guessed_letters = set()

while True:
    client_socket, addr = server_socket.accept()
    print("Connection from", addr)

    initial_message = f"Word length: {len(word)}\nHint: It's a fruits."
    client_socket.send(initial_message.encode())

    while True:
        current_display = display_word(word, guessed_letters)
        client_socket.send(f"Current word: {current_display}\nGuess a letter: ".encode())

        guess = client_socket.recv(1024).decode().strip().upper()

        if len(guess) != 1 or not guess.isalpha():
            client_socket.send("ERROR Invalid guess. Please guess a single letter.".encode())
            continue

        if guess in guessed_letters:
            client_socket.send("ERROR You've already guessed that letter.".encode())
            continue

        guessed_letters.add(guess)

        if guess in word:
            client_socket.send("CORRECT Your guess is correct!".encode())
        else:
            client_socket.send("WRONG Your guess is incorrect.".encode())

        if all(letter in guessed_letters for letter in word):
            client_socket.send("WIN Congratulations! You've guessed the word correctly!".encode())
            break

    client_socket.close()

server_socket.close()
