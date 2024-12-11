import cv2
import numpy as np
import mediapipe as mp
import requests

# Configurazione Mediapipe per il rilevamento delle mani
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Inizializzazione webcam
cap = cv2.VideoCapture(0)  # Cambia "0" con il numero della tua webcam se necessario

# Verifica che la fotocamera sia correttamente connessa
if not cap.isOpened():
    print("Errore: non riesco a connettermi alla fotocamera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Errore nell'acquisizione del video")
        break

    # Ribalta l'immagine per avere un effetto specchio
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Rilevamento della mano
    results = hands.process(rgb_frame)

    # Disegna i landmarks della mano
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Conversione a HSV per rilevare il colore rosso
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    # Rimuovi il rumore con apertura e chiusura morfologica
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Trova i contorni
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Considera solo contorni significativi
            # Calcola il rettangolo e il centroide
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Rettangolo blu

            # Disegna il centroide
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)  # Cerchio verde al centro
                cv2.putText(frame, "Centro", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Prepara i dati da inviare al server Flask
                data = {
                    "hand_detected": results.multi_hand_landmarks is not None,
                    "color_detected": "rosso" if area > 500 else "nessuno",  # Modifica in base al rilevamento del colore
                    "centroid": {"x": cx, "y": cy}  # Centroide rilevato
                }

                # Invia i dati al server Flask
                try:
                    response = requests.post("https://d7a8-109-118-36-72.ngrok-free.app/process-data", json=data)
                    print(f"Risposta dal server: {response.status_code}, {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Errore nell'invio dei dati: {e}")

    # Mostra il video con annotazioni
    cv2.imshow("Webcam + Disegno", frame)

    # Esci premendo 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascio risorse
cap.release()
cv2.destroyAllWindows()
hands.close()
