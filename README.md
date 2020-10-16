# Shelly
Stuff based around the beautifull small electronic devices from Allterco

### [Auto-Restrict-Login](Shelly/Secure.py)
This Script queries trough a given number of ips or mdns names and restricts the http login with a given username and password

##### Usage
To use the script:
1. ***Don't*** forget to change the ip/mdns range in line 9
```
python3 secure.py [username] [password]
