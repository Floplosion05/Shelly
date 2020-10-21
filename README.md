# At the moment this Script is nowhere near being complete, use at your own risk!

# Shelly
Stuff based around the beautifull small electronic devices from Allterco

### [Auto-Restrict-Login](Scripts/secure.py)
This Script queries trough a given number of ips or mdns names and restricts the http login with a given username and password

##### Installation
To use the Script(s) run:
```
(python3 -m) pip install requests
(python3 -m) pip install passlib
```
Then clone or download this repository and run the script(s)

##### Usage
To use the script run:
1. **Don't** forget to change the ip/mdns range in line **[12](https://github.com/Floplosion05/Shelly/blob/1bb07f124326b38dcee3988aaf8065b9076dca41/Scripts/secure.py#L12)**
2. When a login page is already restricted you will be prompted to provide the old password
3. The Script will automatically generate a file called Shelly.json in the same directory as the script, to store the last username and the hash of the last password.
```
python3 secure.py [mode] [username] [password]
  mode  enable/disable
```
##### Error(Codes)
  - 1:
  - 2:
