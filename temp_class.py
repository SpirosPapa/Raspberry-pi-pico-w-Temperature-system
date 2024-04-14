from machine import ADC
from Queue__class import Queue 
import utime
import os
import time



def getNow(UTC_OFFSET=2):
    return time.gmtime(time.time() + UTC_OFFSET * 3600)

class Tmp36Sensor:
    def __init__(self,pin):
        # this is the object of the temp sensor
        # give the pin number that the sensor gives the voltage output to
        self.tmp36= ADC(pin)
        self.max_temp=-50
        self.num_of_meas=0
        self.sum_of_temp=0
        self.temp_queue = Queue()
        self.time_queue = Queue()

        
    def MaxTempUpdate(self,temp):
        # Update max temp
        self.max_temp=max(self.max_temp,temp)
        
    def FlashMeas(self):
        current_time = getNow()
        day=f"{current_time[2]:02d}/{current_time[1]:02d}/{current_time[0]}"
        with open("temperature_log.txt", "a") as file:
            file.write(f"Average temperature: {self.GetAvgTemp()}&deg;C, Day: {day}\n")
        self.max_temp=0
        self.num_of_meas=0
        self.sum_of_temp=0
        self.temp_queue.clear()
        self.time_queue.clear() 
    
    def FlashMeasFile(self):
        # Empty the temperature log file
        try:
            os.remove("temperature_log.txt")
        except OSError:
            pass
    
    def AddToQueue(self, temp) :
        if self.temp_queue.size() >= 10:
            dummy=self.temp_queue.get()
            dummy=self.time_queue.get()
        self.temp_queue.put(temp)
        current_time = getNow()
        hour = current_time[3]
        minute = current_time[4]
        time_str = f"{hour:02d}:{minute:02d}"  
        self.time_queue.put(time_str)
    
# all the getters are here
    def ReadTemp(self):
        adc_value=self.tmp36.read_u16()
        voltage =(3.3/65535)*adc_value # based on maximum output voltage and adc steps
        degC = (100*voltage)-50 # based on voltage to temperature diagramm
        degC=round(degC,1)
        self.num_of_meas+=1
        self.sum_of_temp+=degC
        self.MaxTempUpdate(degC)
        self.AddToQueue(degC)
        current_time = getNow()
        measurement_time = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])  # Format: HH:MM:SS
        # Write temperature and time to a file
        with open("temperature_log.txt", "a") as file:
            file.write(f"Temperature: {degC}°C, Time: {measurement_time}\n")
        return degC

    def GetAvgTemp(self):
        if self.num_of_meas == 0:
            return 0
        return round(self.sum_of_temp/self.num_of_meas,2)
    
    def GetLastTenTemp(self):
        times = self.time_queue.get_all()
        temps = self.temp_queue.get_all()
        return temps,times
    
    def GetMaxTemp(self):
        return self.max_temp
    
    
        
        

