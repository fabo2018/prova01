import os
import sys
import cv2
import numpy as np
import mediapipe as mp
import socket

# Navigazione automatica nella directory del file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Controlla se l'ambiente virtuale è già attivo
if not os.environ.get("VIRTUAL_ENV"):
    # Percorso dell'ambiente virtuale
    env_activate = os.path.join(os.getcwd(), "mediapipe_env", "bin", "activate_this.py")

    # Attivazione dell'ambiente virtuale
    if os.path.exists(env_activate):
        with open(env_activate) as f:
            exec(f.read(), {'__file__': env_activate})
    else:
        print("Errore: Ambiente virtuale non trovato. Assicurati che 'mediapipe_env' sia nella directory corretta.")
        sys.exit(1)

# Importazione delle librerie necessarie
try:
    import cv2
    import numpy as np
    import mediapipe as mp
except ImportError as e:
    print(f"Errore: {e}. Assicurati che le dipendenze siano installate nell'ambiente virtuale.")
    sys.exit(1)

# Configurazione Mediapipe per il rilevamento delle mani
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Inizializzazione webcam
cap = cv2.VideoCapture(0)  # Usa 0 per la webcam predefinita
if not cap.isOpened():
    print("Errore: non riesco a connettermi alla fotocamera.")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Errore nell'acquisizione del video.")
        break

    # Ribalta l'immagine per effetto specchio
    frame = cv2.flip(frame, 1)

    # Converti il frame in RGB per Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Rilevamento delle mani
    results = hands.process(rgb_frame)

    # Disegna i landmark delle mani
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Converti in HSV per il rilevamento del colore rosso
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Unisci le due maschere
    mask = mask1 + mask2

    # Rimuovi il rumore usando operazioni morfologiche
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Trova i contorni del colore rosso
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Considera solo contorni significativi
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Rettangolo blu

            # Calcola il centroide
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)  # Cerchio verde al centro
                cv2.putText(frame, f"Centro: ({cx}, {cy})", (cx - 50, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Configura il client per inviare i dati al server
                HOST = '127.0.0.1'  # Deve corrispondere all'IP del server
                PORT = 65432        # Deve corrispondere alla porta del server

                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((HOST, PORT))
                    data_to_send = f"Centroide: ({cx}, {cy})"
                    client_socket.sendall(data_to_send.encode('utf-8'))
                    client_socket.close()
                except ConnectionRefusedError:
                    print("Errore: Impossibile connettersi al server. Assicurati che il server sia in esecuzione.")

    # Mostra il frame annotato
    cv2.imshow("Webcam + Disegno", frame)

    # Premi 'q' per uscire
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia le risorse
cap.release()
cv2.destroyAllWindows()
hands.close()
