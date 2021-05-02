import psutil
import time
import collections
import wmi
from powerShellInterface import PowerShellInterface

class HardwareMonitor:
    def __init__(self):
        self.psi = PowerShellInterface()
        self.wmi = wmi.WMI(namespace="root\OpenHardwareMonitor")
        self.sensors = self.wmi.Sensor()
        self.lastUpdate = time.time()

#<------------ CPU Stats ------------->
    def getCPUPercentage(self, step = 1, byCore = False):
        cpuPercent = psutil.cpu_percent(interval=step, percpu=byCore)
        return cpuPercent

    def getCPUFrequency(self):
        res = self.psi.getCurrentClockSpeed()
        cpuFreq = []
        res = res.split(' ')
        res[0] = round(float(res[0]), 2)
        res[1] = int(res[1])
        return res

    def getCPUClockWMI(self, isSingleCore = True):
        updateSensors()
        # 1: 54, 2:41, 3:13, 4:37, 5:30, 6:77, 7:16, 8:80 
        cores = [self.sensors[54], self.sensors[41], self.sensors[13], self.sensors[37], self.sensors[30], self.sensors[77], self.sensors[16], self.sensors[80]]
        if isSingleCore:
            maximum = 0
            name = ""
            for core in cores:
                if (core.Value > maximum):
                    name = core.Name
                    maximum = core.Value
            return { name: name, frequency: maximum }
        else:
            return cores

    def getCPUTemp(self):
        updateSensors()
        return self.sensors[31].Value

    def updateSensors():
        if (time.time() - self.lastUpdate) > 3:
            self.sensors = self.wmi.Sensor()
            self.lastUpdate = time.time()

    #get cpu percent from sensors
#<------------ End Cpu Stats ---------->
#<------------ Gpu Stats -------------->
# - Get Clock speed
    def getGPUFrequency(self):
        updateSensors()
        return { gpuCore: self.sensors[7].Value }

    def getGPUMemoryUsage(self):
        updateSensors()
        return { total: self.sensors[43].Value, used: self.sensors[2].Value, free: self.sensors[59].Value}
# - Get Temp
    def getGPUTemp(self):
        updateSensors()
        return self.sensors[48].Value

# - Get Utilization %
#<------------ End Gpu Stats ---------->
#<------------ Ram Stats -------------->
# - Get Utilization % 
# - Get Utilization [Used, Total, Free]?
#<------------ End Ram Stats ---------->
#<------------ Drive Stats ------------>
# - Get Drive usage [Used, Total, Free]
# - Only get the first 2/3 drives
#<------------ End Drive Stats -------->
#<------------ Network Stats ---------->
# - Get Active connection type? 
# - Get download 
# - Get upload
#<------------ End Network Stats ------>
#<------------ Processes Stats -------->
#<------------ End Processes Stats ---->




hwm = HardwareMonitor()
print(hwm.getCPUFrequency())

import wmi 
w = wmi.WMI(namespace="root\OpenHardWareMonitor")
temperature_infos = w.Sensor()
# i = 0
# for sensor in temperature_infos:
#     if sensor.SensorType == u'Temperature':
#         print("["+str(i)+"]"+sensor.Name + ':' +  str(sensor.Value))
#     i+=1

sensors = {}
for i in range(len(temperature_infos)):
    sensor = temperature_infos[i]
    string = "[{index}] {name}: {value}".format(index=i, name=sensor.Name, value=sensor.Value)
    if (sensor.SensorType not in sensors.keys()):
        sensors[sensor.SensorType] = []
    sensors[sensor.SensorType].append(string)

for key in sensors.keys():
    print('\n'+key)
    for sensor in sensors[key]:
        print('\t' + sensor)
    
    
for i in range(5):
    time.sleep(1)
    print(hwm.getCPUTemp())
