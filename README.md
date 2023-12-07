# radio
Radio

Installation
    Raspbian bullseye - not bookworm (as yet)

username: 
    station

install package list:
    gh (github cli) mpd mpc python3 python3-pip

python modules:
    pip install raspberrypi-tm1637

installing gh if not in repo:

    type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && sudo apt update \
    && sudo apt install gh -y

login to gh
    gh auth login
clone radio
    gh clone radio

adafruit audio hat:
    info at https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage

    curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash

    follow this:https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/i2s-tweaks (may not be needed)

mpd config:
    sudo nano /etc/mpd.conf

    amend playlist dir to radio github location
    add line:mixer_type                      "software"




enable gpio and i2c in raspi-config