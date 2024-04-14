import machine
from machine import Timer
import network
import socket
import utime
import ntptime  
from temp_class import Tmp36Sensor
from time import sleep
import time

ssid ='INALAN_2.4G_iunyeg'
password = 'InalanAek1924!@'
# Global variable
page = ""
current_day=""
sensor_type='TMP36'
day_counter=0

def getNow(UTC_OFFSET=2):
    return time.gmtime(time.time() + UTC_OFFSET * 3600)

def connect() :
    # this function is used to connect to the WLAN network
    wlan =network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)
    start_time = utime.time()
    while not wlan.isconnected():
        if utime.time() - start_time > 30:
            raise TimeoutError("Connection timed out")
        print('Waiting for connection...')
        sleep(1)
    ip= wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip, port=8080, backlog=1):
    address = (ip, port)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(backlog)
    return connection

def webpage(temp, current_moment, sensor_type, average_temp, last_ten_temps,times, max_temp):
    # Convert last_ten_temps list into a formatted HTML table
    last_ten_table = "<table>"
    size=len(last_ten_temps)
    last_ten_table += f"<tr><th>Last {size} Temperatures</th></tr>"
    for measurement, time_measurement in zip(last_ten_temps, times):
        last_ten_table += f"<tr><td>Temperature:{measurement}&deg;C, Time: {time_measurement}</td></tr>"
    last_ten_table += "</table>"
    #last ten table contains the html neccesary to create a table
    # button to download temperature log file
    download_button = "<form action=\"/download\" method=\"get\"><button type=\"submit\">Download Temperature Log</button></form>"
    # HTML content with CSS styling
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f2f2f2;
            }}
            .container {{
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Temperature Monitoring System</h2>
            <p>Current temperature: {temp}&deg;C</p>
            <p>Current date: {current_moment}</p>
            <p>Sensor type: {sensor_type}</p>
            <p>Average temperature for today: {average_temp}&deg;C</p>
            <p>Max temp for today: {max_temp}&deg;C</p>
            <h3>Last Ten Temperature Measurements</h3>
            {last_ten_table}
            {download_button}
        </div>
    </body>
    </html>
    """
    return str(html)

def GetValues(tmp36):
    global current_day, page  # Declare global variables
    if getNow()[2] != current_day:  # Using utime instead of datetime
        current_day = getNow()[2]  # Update current_day using utime
        day_counter+=1
        tmp36.FlashMeas()
        if day_counter==10:
            tmp36.FlashMeasFile()
    temp = tmp36.ReadTemp()
    average_temp = tmp36.GetAvgTemp()
    last_ten_temps, times = tmp36.GetLastTenTemp()
    max_temp = tmp36.GetMaxTemp()
    current_time = getNow()
    current_moment = "{:02d}:{:02d} {} on {} {}, {}".format(
        current_time[3],  
        current_time[4],  
        "AM" if current_time[3] < 12 else "PM",  
        "January" if current_time[1] == 1 else "February" if current_time[1] == 2 else "March" if current_time[1] == 3 else "April" if current_time[1] == 4 else "May" if current_time[1] == 5 else "June" if current_time[1] == 6 else "July" if current_time[1] == 7 else "August" if current_time[1] == 8 else "September" if current_time[1] == 9 else "October" if current_time[1] == 10 else "November" if current_time[1] == 11 else "December", 
        current_time[2],  
        current_time[0], 
    )
    page = webpage(temp, current_moment, sensor_type, average_temp, last_ten_temps, times, max_temp)

def serve(connection):
    #Start a web server
    tmp36 = Tmp36Sensor(26)
    GetValues(tmp36)
    tim = Timer(-1)  # create a virtual timer
    tim.init(period=500000, mode=Timer.PERIODIC, callback=lambda t: GetValues(tmp36))
    while True:
        client = connection.accept()[0]
        request = client.recv(1024).decode('utf-8')
        print(request)
        if "/download" in request:
            with open("temperature_log.txt", "r") as file:
                data = file.read()
            response = "HTTP/1.1 200 OK\n"
            response += "Content-Type: text/plain\n"
            response += f"Content-Length: {len(data)}\n"
            response += "Content-Disposition: attachment; filename=temperature_log.txt\n\n"
            response += data
            client.sendall(response.encode('utf-8'))
        else:
            response = "HTTP/1.1 200 OK\n"
            response += "Content-Type: text/html\n"
            response += f"Content-Length: {len(page)}\n\n"
            response += page
            client.sendall(response.encode('utf-8'))
        client.close()

try:
    ip= connect()
    connection = open_socket(ip)
    ntptime.settime()
    current_day=getNow()[2]
    serve(connection)
except Exception as e:
    print(f"An exception occurred: {e}")
    machine.reset()




    

