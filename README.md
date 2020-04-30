## Dependencies:-

1. Firmata library for Python [Pymata](https://htmlpreview.github.io/?https://raw.githubusercontent.com/MrYsLab/PyMata/master/documentation/html/pymata.m.html#header-classes)
	```
	pip install pymata
	```
2. MQTT Client Library for Python [Eclipse Paho](https://pypi.org/project/paho-mqtt/)
	```
	pip install paho-mqtt
	```
## Run on Boot:-

To make the Python script run on boot I have used [InitScripts](https://openwrt.org/docs/techref/initscripts), to creare the job follow the following commands, (Its a basic script and doesnot have error handling and all)

`vi /etc/init.d/dht12`

Paste the followinf content, 

```
#!/bin/sh /etc/rc.common

START=98

start(){
        ubus  -t 60 wait_for network.interface network.interface.loopback # Makes sure network is up
        echo "Starting the DHT12 Sensor Script"
        python /root/sensor.py &
}

```
Make the file executable and enable it,

```
chmod +x /etc/init.d/dht12
/etc/init.d/dht12 enable
```

Now you can reboot the module and can see the sensor data getting published to the provided topic. 

