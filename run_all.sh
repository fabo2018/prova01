#!/bin/bash

# Attivazione dell'ambiente virtuale
source ~/mediapipe_env/bin/activate

# Avvio dell'applicazione Flask
echo "Avvio dell'app Flask..."
python3 ~/Desktop/prova01/app.py &

# Attendi che Flask sia attivo
sleep 3

# Avvio di Ngrok per il tunnel
echo "Avvio del tunnel Ngrok..."
ngrok http 5000
