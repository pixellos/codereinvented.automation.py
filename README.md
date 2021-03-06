# codereinvented.automation.py
Home Automation

## How to run

### Docker
- Install docker
- In `docker-compose` `environment` section add missing variables
- `docker-compose up` 
- 

### Sofar Solar HYD

Some envs are required:
-  "logger__ip"
-  "logger__port"
-  "logger__serial"
-  "inverter__slaveid"
-  "verbose"

Optional:

#### PVMonitor

- "pvmonitor__login"
- "pvmonitor__password"
- "pvmonitor__lp"

#### MQTT
- "mqtt__address"
- "mqtt__port"
- "mqtt__prefix" - prefix for mqtt topic.


> PowerShell


```powershell
[Environment]::SetEnvironmentVariable(
  "logger__ip",
  "192.168.1.xxx",
  [EnvironmentVariableTarget]::Machine)
[Environment]::SetEnvironmentVariable(
 "logger__port",
 "8899",
 [EnvironmentVariableTarget]::Machine)
[Environment]::SetEnvironmentVariable(
 "logger__serial",
 "175xxxxxxx",
 [EnvironmentVariableTarget]::Machine)
[Environment]::SetEnvironmentVariable(
 "inverter__slaveid",
 "3",
 [EnvironmentVariableTarget]::Machine)
 [Environment]::SetEnvironmentVariable(
 "verbose",
 "0",
 [EnvironmentVariableTarget]::Machine)
```

## Application

To get continious stream of json files run 
- pip3 install -r requirements.txt
- python3 ./main.py


# Description

Application is scraping excel, building meta-table with addresses and descriptions, then it bucket it to not read more than 50 bytes from modbus at once, later on files are available for further processing

# TODO
- package it into pip package
- better pvmonitor integration
- read values as soon as possible, upload to pvmonitor each 5 min
- mqtt
- make use of disabled features information to fetch less data


# Thanks
- https://github.com/MichaluxPL/Sofar_LSW3
- https://github.com/jmccrohan/pysolarmanv5
- https://github.com/AdvancedClimateSystems/uModbus


## ChangeLog
- 0.0.1

Added DockerFile to setup homeassistant quickly
Added MQTT send

