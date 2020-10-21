# At the moment this Script is nowhere near working/being complete, use at your own risk

# Shelly
Stuff based around the beautifull small electronic devices from Allterco

### [Auto-Restrict-Login](Scripts/secure.py)
This Script queries trough a given number of ips or mdns names and restricts the http login with a given username and password

##### Usage
To use the script:
1. **Don't** forget to change the ip/mdns range in line **[12](https://github.com/Floplosion05/Shelly/blob/ced516583ffa67cf5629a8e12d20497b73b1f771/Scripts/secure.py#L12)**
```
python3 secure.py [mode] [username] [password]
  mode  enable/disable
```
2. Error(Codes)
  - 1:
  - 2:

##### Installation
To use the Script(s) run:
```
(python3 -m) pip install requests
(python3 -m) pip install passlib
```
Then clone or download this repository and run the script(s)
