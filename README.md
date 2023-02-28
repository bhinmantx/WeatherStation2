# WeatherStation
A wind direction, speed, weather conditions server with a camera stream
## Docker, Microservices, Reverse Proxy
The system is based on a raspberry pi inside of a weatherproof dome. Attached via i2c are enviromental sensors
Because the Pi lacks a simple ADC and some sensor code isn't as well supported in Python, an arduino nano is attached via USB in order to take lightning strike and windspeed readings

The pi's camera can be turned via a stepper motor.

The camera stream and sensor data are made available via a simple http endpoint which is behind a reverse proxy (dockerized nginx) in order to provide SSL termination with the possibility of caching information to limit requests of the PI

The user facing side is served via a containerized web server running Golang which is again behind the nginx proxy 

```mermaid
flowchart RL

    subgraph Arduino
        direction TB 
        Nano{Nano}
        An[fa:fa-wind Anemometer] -->|Voltage| Nano
        Compass[fa:fa-compass Wind Direction] -->|i2c| Nano
        Nano --> NP((fa:fa-traffic-light NeoPixel))
    end
    subgraph WeatherDome
        Pi{RaspberryPi python}
        Nano -->|Serial| Pi
        Camera -->|CamStream.py| Pi
        Temp[Temperature] -->|i2c| Hum[Humidity] -->|i2c| Pi
        Pi -->|TB6612| D[PanMotor]
       

    end
    subgraph WebServices
        Ngnix[ReverseProxy]
        Pi <-->|CamStream| Ngnix
        Pi <-->|Web Controls| Ngnix
    end


linkStyle default stroke:white
classDef subGraf stroke:#333,stroke-width:4px;
class Arduino,WeatherDome subGraf;

linkStyle 0 stroke-width:4px,stroke:green
linkStyle 1 stroke-width:4px,stroke:yellow
linkStyle 2 stroke-width:4px,stroke:yellow
linkStyle 3 stroke-width:4px,stroke:white
linkStyle 4 stroke-width:4px,stroke:orange
linkStyle 5 stroke-width:4px,stroke:yellow
linkStyle 6 stroke-width:4px,stroke:yellow
linkStyle 7 stroke-width:4px,stroke:orange
linkStyle 8 stroke-width:4px,stroke:blue
```
#Docker containers provide the user facing web server as well the nginx reverse proxy for SSL termination
```mermaid
graph TD
subgraph Docker Containers
    
    nginx(nginx SSL)
    Golang[Golang Webserver Front End] --> nginx

end
subgraph From Pi
    Camera[Camera Feed] --> nginx
    Sensor[Sensor Data] --> nginx
end

U(User)
nginx ---> U
```
