# Houniao Project
## Motivation and Aspiration
Houniao Project orginated from Moonshot 48, a Hackathon belongs to teenagers. There, four distinct yet aspired youth combined their expertise to pursue a shared goal: make the world a better place through AI-powered education.

Houniao project aims to support an often-overlooked group: left-behind children in rural and underdeveloped urban areas who spend most of their time without parental companionship and are subjected to educational and emotion unfulfillment.

## Key Features  
**Houniao ONE**, the initial of this project, is an AI-powered emoji chatbot designed for education and child communication. It provides parents with AI-analyzed reports on their child's mental well-being, fostering better parent-child interaction and preventing emotional and social detachment while promoting social responsibility.  

### Houniao ONE consists of:  
- **Interactive interface** for children, implemented with AI-Humanization technologies
- **Parent terminal** for checking updates on children's status
- **AI-integrated database** for processing conversation and analyzing children's data 

## Getting Started

### Hardware Setup
#### Material Required
- ESP32C3 or other model with Wi-Fi connectivity
- WS2812 8*8 LED matrix
- 5V Power supply or battery
- 3D-printed enclosure

#### Prerequisites
- Arduino IDE or Platform IO preinstalled
- API keys for AI services


#### 1. Install arduino library dependencies:
   `Adafruit_NeoPixel`
   and
   `Arduino Json`

#### 2. Change Wi-Fi Parameters
Go to `Embedded Program/src/main.cpp` line 8-9. Change the SSID and Passcode to correspond your local network.

#### Optional: Adding Custom Emojis
Using `Embedded Program/pixelizer.py`, you can easily turn a image into a 8*8 RGB matrix that can be read by `main.cpp`. You need to define the customized pattern in `main.cpp`, add a method that execute it, and modify `void loop()` to add it into the sequence.

### Software Setup
According to `Frontend` and `Backend` folder, build the webpage and database. The hardware should work in accordance with the software once set up.

## Technology Stack
- Hardware: Arduino
- Frontend: React 19, Vite 6, ESLint
- AI Sevices: Kouzi API
- Backend: Python, SQLite 

# License


Copyright © 2025 Wangzi Haoran, Jason Chen, Notting Xu, Yang Yanrui. All Rights Reserved.
