import socket

# Configura il server
HOST = '127.0.0.1'  # Indirizzo IP locale
PORT = 65432        # Porta per la connessione

# Crea il socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server in ascolto su {HOST}:{PORT}")

    while True:  # Mantieni il server in ascolto
        conn, addr = s.accept()
        with conn:
            print(f"Connessione stabilita con {addr}")
            while True:
                data = conn.recv(1024)  # Riceve i dati
                if not data:
                    break  # Interrompi se non ci sono dati
                print(f"Dati ricevuti: {data.decode('utf-8')}")  # Stampa i dati ricevuti

