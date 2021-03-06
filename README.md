# At the moment this Script is pretty stable and reliable, but use it at your own risk!

# Shelly
Stuff based around the beautifull small electronic devices from Allterco

### [Secure](Scripts/secure.py)
This Script queries trough a given number of ips or mdns names and restricts the http login with a given username and password

##### Installation
###### Following installations are possible:
1. automatically via pip:
```
pip install shelly-restrict
```
2. manually via git clone
Clone or download this repository first and run:
```
(python3 -m) pip install -r ./requirements.txt
```

##### Usage
1. When it was installed auomatically:

Please enter your ips seperated with a comma as the fourth parameter
```
shelly-restrict [mode] [username] [password] [ip1,ip2,..]
  mode      enable/disable
  username  the username you want to use
  password  the password you want to use
  ips       the ip(s) of the shelly device(s), seperated by a comma
```

2. When it was installed manually:

**Don't** forget to change the ip/mdns range in line **[12](Scripts/secure.py#L12)**
```
ips = ['192.168.xxx.xxx'] #add ips or mdns names of devices
```
Then:
```
python3 secure.py [mode] [username] [password]
  mode  enable/disable
  username  the username you want to use
  password  the password you want to use
```

##### Error-Codes
  - 0: Failed to load Shelly.json, check the directory and path. (The script cant find the [Credentials-File](https://github.com/Floplosion05/Shelly/blob/main/README.md#credentials-file))
  - 1: Wrong password entered. (The provided password doesnt match with the saved hash)
  - 2: Right hash found but wrong password provided. (The entered password matches the saved hash, but not the actual password on the login page)
  - 3: Found Shelly.json, but didnt find entry for this device. (The script found the [Credentials-File](https://github.com/Floplosion05/Shelly/blob/main/README.md#credentials-file), but the restricted login was never enabled with this script)
  - 4: Found Shelly.json, but its empty. (The [Credentials-File](https://github.com/Floplosion05/Shelly/blob/main/README.md#credentials-file) is empty, if you did not do this manually please open an [issue](https://github.com/Floplosion05/Shelly/issues/new))
  - 5: Fatal error! (The provided command lead to a script crash wich results in a fatal error)

##### Credentials-File
The Credentials-File (Shellys.json) is generated and then located in the same directory as the script.
The structure is:
```
{"devices": [{"ip": "192.168.xxx.xxx", "username": "test", "password": "$pbkdf2-sha256$30000$yZnzPqc0Rqi1NibEeM.5Fw$QZ0sk1Z6K4LMt3UM3AGrrKLk9jBOjwrXsY1psfAPY4Q"}, {"ip": "192.168.xxx.xxx", "username": "test", "password": "$pbkdf2-sha256$30000$yZnzPqc0Rqi1NibEeM.5Fw$QZ0sk1Z6K4LMt3UM3AGrrKLk9jBOjwrXsY1psfAPY4Q"}]}
```
