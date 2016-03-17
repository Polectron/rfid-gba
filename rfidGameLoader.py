import serial
import json
import subprocess

gamesList = 'games.json'

gamesFile = open(gamesList)
games = json.loads(gamesFile.read())
gamesFile.close()

configList = 'config.json'
configFile = open(configList)
config = json.loads(configFile.read())
configFile.close()

emulator = config["emulator"]
device = '/dev/ttyUSB0'

ser = serial.Serial(device, 9600, timeout=1)

reading = False
card = ''
finishedReading = False
loadedGame = False

while True:
    character = ser.read()

    if(character == b'\x03'):
        finishedReading = True
        reading = False
        card = card.strip('\n\r')
        loadedGame = False

    if(reading):
        card += character

    if(character == b'\x02'):
        reading = True
        finishedReading = False
        card = ''

    if(finishedReading and not loadedGame):
        loadedGame = True
        subprocess.call(["killall", "-9", emulator])
        p = subprocess.Popen(["./"+emulator, games[card]], stdout=subprocess.PIPE, shell=False)


ser.close()
