# Python Space Shooter
A fast‑paced Python 3 space shooter: steer your spaceship through dangerous obstacles and partial walls, destroy incoming asteroids, and collect power‑ups like extra life and double fire. Includes adjustable graphics settings (Very Low, Low, High) for different performance levels.

![Png](https://i.ibb.co/GQjJTFQ7/Immagine-2025-08-12-000139.png)

---

## 💻 Requirements Installation

### Microsoft Windows 11/10  
Install Python 3.13 by executing "python-3.13.0-amd64.exe" in Microsoft Windows.  
  
Library for creating the applications with a GUI: Pillow.  
File "pillow-11.0.0-cp313-cp313-win_amd64.whl" downloaded for Microsoft Windows from
https://pypi.org/project/pillow/#files  
  
Command to execute in the terminal to install the Pillow library:
```
pip install pillow-11.0.0-cp313-cp313-win_amd64.whl
```

Open the terminal (PowerShell or CMD) in the project folder and run:

```
pip install -r requirements.txt
```

Make sure Python 3 is installed and `pip` is in your PATH.  
If you have multiple Python versions:

```
pip3 install -r requirements.txt
```
---

### deepin (linux, Debian)

```
sudo apt-get update
sudo apt-get upgrade

python3 --version

curl https://bootstrap.pypa.io/pip/3.7/get-pip.py -o get-pip.py

sudo python3 get-pip.py

sudo apt-get install python3-tk

sudo apt update
sudo apt upgrade

# only if necessary
sudo apt autoremove

# only if necessary
sudo apt remove python3-pil
sudo apt purge python3-pil
sudo apt autoremove

sudo apt install python3-pip

sudo pip3 install Pillow

python3 python_space_shooter.py
```
---

### Debian 12 (linux)

```
sudo apt-get update
sudo apt-get upgrade

python3 --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

sudo apt install python3-full

curl https://bootstrap.pypa.io/pip/3.7/get-pip.py -o get-pip.py

sudo apt-get install python3-tk

sudo apt update
sudo apt upgrade

# only if necessary
sudo apt autoremove
sudo apt remove python3-pil
sudo apt purge python3-pil
sudo apt autoremove

sudo apt install python3-pip

sudo pip3 install Pillow

python3 python_space_shooter.py

# if it doesn't work on Debian
sudo apt update
sudo apt install python3-pil
sudo apt install python3-pil.imagetk

python3 python_space_shooter.py
```

---------------------
