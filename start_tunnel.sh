#!/bin/bash
# Avvia il server Flask
python3 video_feedback.py &
# Aspetta qualche secondo per assicurarsi che Flask sia attivo
sleep 5
# Avvia Ngrok per il tunneling
ngrok http 5000


