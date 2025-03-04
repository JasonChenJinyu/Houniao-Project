# Houniao Project

## Motivation and Aspiration
Houniao Project is orginated from Moonshot 48: a Hackathon belongs to teenagers. There, 4 distinct yet aspired individual utilized their specialization to serve a unified goal: make the world a better place through AI-powered education, the ultimate theme of the hackathon.

Houniao project aims to help a overlooked group of individual: the left-behind childrens in rural or developing urban area who are not accompanied by their parents most of the time. With respect to the theme of the hackathon: AI education for good.

## Project Overview
Houniao Project's first product is Houniao ONE, an AI-powered emoji chatbot specialized for education and children communication, featuring parent access to children's mental status analyzed and reported by AI to facilitate parent-kid communication and interaction, preventing emotional and social detachment, and cultivating social responsibility. It consists a children user interactive interface, parent terminal, and a database of children's data with AI API implemented. 

### Hardware Configuration (Children's End)
On children's end, as children press the button, a 3-second audio recording starts. The audio file will be saved and transcripted to text, and then it will be sent to AI model. The AI, while responding a message, returns a emoji token representing AI's tone when speaking and send to the hardware through http request. Then, a emoji animation will be selected from a sequence and be displayed on the LED matrix.

Prototype Hardware: Esp32-C3 Supermini, WS2812 LED 8*8 matrix display, Power managing module, and Battery.

### Frontend Configuration (Parent's End)

Parent portal is designed to be available on web and ios or android app where parent can get to know the AI's recent response and analysis of children's emotions.

### Backend Configuration (AI Database)


Copyright © 2025 Wangzi Haoran, Jason Chen, Notting Xu, Yang Yanrui. All Rights Reserved.
