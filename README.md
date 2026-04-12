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

> **Important:** This is a GUI app (tkinter). It **must** run from a desktop session with a display.
> It will NOT work over SSH unless you forward the display (see below).

#### Option A: Run directly on the Pi's desktop

Open a terminal on the Pi (physically or via VNC) and run:

```bash
cd ~/smart_mirror
source .venv/bin/activate
python3 smartmirror.py
```

#### Option B: Run over SSH (testing only)

```bash
# From the Pi's SSH session, set DISPLAY to the local screen:
export DISPLAY=:0
cd ~/smart_mirror
source .venv/bin/activate
python3 smartmirror.py
```

### 6. Auto-start on boot (recommended)

The mirror should start automatically when the Pi boots into the desktop.

#### Enable auto-login to desktop

```bash
sudo raspi-config
# Navigate to: System Options → Boot / Auto Login → Desktop Autologin
```

#### Install autostart entry

```bash
mkdir -p ~/.config/autostart
cp services/smartmirror.desktop ~/.config/autostart/
# Edit the Exec path in the .desktop file if your install path differs from ~/smart_mirror
```

The mirror will launch fullscreen after the desktop loads on every reboot.

### Helper services (optional)

These systemd services run background scripts for TV control and temperature monitoring:

```bash
# Edit the paths in the .service files to match your install location and username
sudo cp services/checkTv.service /etc/systemd/system/
sudo cp services/tempChecker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable checkTv.service tempChecker.service
sudo systemctl start checkTv.service tempChecker.service
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