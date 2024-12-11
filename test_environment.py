try:
    import cv2
    import numpy as np
    import mediapipe as mp
    print("Tutte le librerie sono state importate correttamente!")
except ImportError as e:
    print(f"Errore: {e}")
