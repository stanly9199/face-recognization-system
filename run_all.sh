#!/bin/bash
cd website-vue && npm run serve &
cd website-vue/website-backend && node server.js &
cd nginx-1.26.2 && ./nginx &
cd image && python -m http.server 8000 &
ngrok start --all &
wait
