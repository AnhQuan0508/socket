from configparser import ConfigParser

config = ConfigParser()

config["ttmq38@gmail.com"] = {
  "password": "123456"
}

config["SMTP"] = {
  "port": 2225
}

config["POP3"] = {
  "port": 3335
}

# config["AutoUpdate"] = {
#   "time": 10
# }

with open("config.ini", "w") as f:
  config.write(f)