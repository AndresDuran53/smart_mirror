[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)

<img  width="480" src="media/iot_banner_smartmirror.png">

# Zarus Smart Mirror
A custom version of a Smart Mirror

## Quick Start

### Prerequisites

- Raspberry Pi con Raspberry Pi OS (Debian-based)
- Python 3.9+
- Conexión a internet

### 1. Install system dependencies

```bash
# Tkinter (interfaz gráfica) y fuentes
sudo apt-get update
sudo apt-get install -y python3-tk python3-venv fonts-roboto
```

### 2. Clone the repository

```bash
git clone https://github.com/<tu-usuario>/smart_mirror.git
cd smart_mirror
```

### 3. Create virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure

Copy the configuration template and edit it with your credentials:

```bash
cp configuration_template.json configuration.json
nano configuration.json
```

Fill in:
- **mqtt**: Your MQTT broker address, user, and password
- **homeAssistant**: Your Home Assistant URL and long-lived access token
- **openWeather**: Your coordinates and [OpenWeatherMap API key](https://openweathermap.org/api)

### 5. Run

```bash
source .venv/bin/activate
python3 smartmirror.py
```

### Run as a service (optional)

To auto-start on boot, see the service files in `services/`:

```bash
# Edit the service file paths as needed, then:
sudo cp services/checkTv.service /etc/systemd/system/
sudo systemctl enable checkTv.service
sudo systemctl start checkTv.service
```

### Python dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP requests (weather, Home Assistant) |
| `paho-mqtt` | MQTT communication |
| `pytz` | Timezone handling |
| `ephem` | Astronomical calculations (moon, sun) |
| `psutil` | System resource monitoring |
| `Pillow` | Image processing (PIL) |
| `opencv-python-headless` | Camera and face detection |
| `RPi.GPIO` | Raspberry Pi GPIO pins |

> **Note:** `tkinter` is required but is a system package — installed via `python3-tk` in step 1.

### Image Example

[<img src="media/Screenshot_example.png" alt="Example Image 1">](media/Screenshot_example.png)

----

## Implementations
- [x] Datetime
- [x] Forecast
- [x] Events
- [x] Moon Phase
- [x] Sunset / Sunrise
- [x] Picture Slide
- [x] Face recognition
- [x] Home Assistant Connection
- [x] Mqtt Connection

## License
Zarus Smart Mirror is an open source code. All files are licenced under Creative Commons [Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)