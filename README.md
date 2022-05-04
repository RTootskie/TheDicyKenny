# TheDicyKenny
The Dice Rolling project

# Required
`Python >= 3.9`  
`Debian/Ubuntu`


# Installation  
1. Initially you need all the files on your server  
*Clone the repo to your desired directory*

2. Install required python dependencies with pip  
  ```
  discord  
  pandas  
  tables2ascii  
  ```
3. Create the system service in `/etc/systemd/system/`  
```
[Unit]  
Description=dicykenny service  
After=network.target  
  
[Service]  
Type=simple  
User=root  
Environment=TOKEN=[YOUR DISCORD BOT TOKEN]  
WorkingDirectory=/home/dicykenny  
ExecStart=python3.9 /home/dicykenny/main.py  
Restart=on-abort  
  
[Install]  
WantedBy=multi-user.target  
```

4. Make sure you edit your own discord bot's token into the Environment variable.
5. Reload the daemon for system service to work `systemctl daemon-reload`
6. Enable and then restart the service `service dicykenny enable` & `service dicykenny restart`
