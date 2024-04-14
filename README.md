# Temperature Monitoring System with Raspberry Pi Pico and TMP36 Sensor

Welcome to the Temperature Monitoring System project for Raspberry Pi Pico! This project utilizes Micropython to create a system that continuously monitors temperature using a TMP36 analogue sensor. It records temperature data, calculates daily averages and maximum temperatures, and provides a user-friendly interface via a web server hosted on the Raspberry Pi Pico.

## Features

- **Temperature Sensing**: Utilizes the TMP36 analogue temperature sensor to measure ambient temperature.
- **Data Logging**: Records temperature readings to a file, updating the daily average and maximum temperature.
- **Web Server Interface**: Hosts a web server on the Raspberry Pi Pico, allowing users to access temperature data and system information.
- **Automatic Updates**: The system updates temperature readings every 5 minutes using interrupts.
- **User Interaction**: Provides a button on the web interface to allow users to download the temperature data file.

## Installation

1. **Hardware Setup**: Connect the TMP36 sensor to the Raspberry Pi Pico according to the provided circuit diagram.
2. **Software Installation**:
   - Clone this repository to your Raspberry Pi Pico.
   - Ensure Micropython is installed on your Raspberry Pi Pico.
   - Upload the code files to the Raspberry Pi Pico.

## Usage

1. **Power On**: Power on the Raspberry Pi Pico.
2. **Access Web Interface**: Connect to the Raspberry Pi Pico's Wi-Fi network and navigate to the provided IP address in your web browser.
3. **View Data**: On the web interface, you can view:
   - Current temperature
   - Maximum daily temperature
   - Average daily temperature
   - Current time
   - List of last ten temperature readings
4. **Download Data**: Use the provided button on the web interface to download the temperature data file.

## Notes

- Ensure the Raspberry Pi Pico has a stable power supply to maintain accurate temperature readings.
- Customize the web interface or functionality according to your preferences by modifying the provided code files.


Thank you for using the Temperature Monitoring System with Raspberry Pi Pico and TMP36 Sensor. If you have any questions or feedback, please don't hesitate to reach out.
