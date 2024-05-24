#!/bin/bash

chromium-browser http://127.0.0.1:5000/bookshelf --kiosk --noerrdialogs --disable-infobars --no-first-run --start-maximized > /home/craig/bookshelf_pi/logs/chrome.log 2>&1
