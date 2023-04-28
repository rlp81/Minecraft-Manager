# PLEASE NOTE!
**This program was programmed in linux. Some changes may need to be made.**

# Minecraft-Manager
A Discord bot that can control minecraft servers

# Dependancies
**py-cord v2.3**: Discord API
**mcrcon**: Minecraft Rcon commmunicator

# Installation
## Windows
**py-cord**

```py -3.10 -m pip install -U py-cord --pre```

**mcrcon**

```py -3.10 -m pip install mcrcon```

## Linux/Mac-OSX
**py-cord**

```python3.10 -m pip install -U py-cord --pre```


**mcrcon**

```python3.10 -m pip install mcrcon```

# Running

## Making a server
Make a new folder in the ~/servers directory, e.g. ~/servers/myserver

In said folder install the server.jar file, and run it e.g. ```java -jar server.jar``` 

create a start.sh file e.g.

``` #!bin/bash (new line) java -Xms1024M -Xmx1024M -jar minecraft.jar --nogui```

Then use the following command:

```chmod +x start.sh```

Make sure it works by using: ```./start.sh```

## Adding the server
Start the bot, and then use the command /add_server SERVERNAME PORT e.g. 56775 PASSWORD

The password and port are set in server.properties in your server. THESE ARE NOT FOR CONNECTING TO THE SERVER. 

Enable rcon in the server in server.properties by replacing false with true at enable-rcon=false 

Set your password and port in server.properties where it says rcon.port=PORT and rcon.password=PASSWORD

## Running the server
Now you can run your server. Use the command /start SERVERNAME and it should start. 

Note: It will take longer to start on the first start up.
