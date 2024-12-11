import cv2

print("Sto cercando la tua webcam...")
for i in range(5):  # Prova i primi 5 numeri
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print(f"Webcam trovata al numero {i}")
        cap.release()
        break
    else:
        print(f"Numero {i} non corrisponde a nessuna webcam.")
