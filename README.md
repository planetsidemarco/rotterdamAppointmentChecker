# Rotterdam Municipality Appointment Checker

Small codebase to help me scrape the https://www.rotterdam.nl/eerste-inschrijving-in-nederland/start-eerste-inschrijving-in-nederland website for available appointment dates and times.

## Script

Uses Selenium to scrape and explore a webform from the above URL to find the next available appointment date and times for the Rotterdam municipality.

Outputs a text file of next earliest appointment time, screenshot of that option, and screenshot of calendar availability.

## Docker

Building docker container with command: ```docker build -t rotterdam .```

Running interactive docker container with command: ```docker run -it -v $(pwd):/usr/src/app -e DISPLAY=:99 rotterdam```
