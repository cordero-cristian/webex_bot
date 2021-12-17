import random
import time
import sys
print(sys.path)
from webex_bot.webex_bot_functions import webex_bot_functions
from bot_commands.bot_commands import bot_commands
from message_parser.message_parser import webex_message_parser
import yaml
with open('./config.yml') as file:
    configDict = yaml.load(file, Loader=yaml.FullLoader)
roomId = configDict['roomId']
roomName = configDict['roomName']

botFuncs = webex_bot_functions()
botCommands = bot_commands()

#cs Network team room id
#roomID = 'Y2lzY29zcGFyazovL3VzL1JPT00vOWY4MGVjYjEtZTRhNy0xMWViLTk3ZWQtOTE5NmRjM2EzYmYy'
listOfCommand = [
    '!details <hostname> : get ip, os_type',
    '!em7 <hostname> : get sl1/em7 details',
    '!snmp <hostname> : get snmp details',
    '!interface <hostname> <interface> : get interface details',
    '!interface <hostname> : list interfaces of hostname',
    '!vlan <hostname> <vlan_name>: get id of vlan',
    '!vlan <hostname>: get a list of vlans of hostname',
    '!help: send this help message'
]
listOfAnimalSounds = [
    'meow',
    'woof',
    'neigh',
    'baa',
    'oink',
    'moo',
    'hee-haw',
    'cluck',
    'cock-a-doodle-do',
    'chirp',
    'hoot',
    'quack',
    'gobble gobble',
    'ribbit',
    'rawr'
]
messageParser = webex_message_parser()
while True:
    commands = botFuncs.get_latest_commands(roomID)
    if commands is not None:
        for commandTup in commands:
            command = commandTup[0]
            personId = commandTup[1]
            commandDict = messageParser.parse_webex_message(command)
            command = commandDict['command'][1:]
            print(command)
            try:
                param1 = commandDict['param1']
            except KeyError:
                param1 = None
            if command == 'ood':
                string = random.choice(listOfAnimalSounds)
                botFuncs.send_message(string, groupTitle=roomName)
            if command == 'details':
                html = botCommands.details(param1)
                messageStr = f"``` \n{html}\n ```"
                botFuncs.send_message(messageStr, personid= personId, markdown=True)
            if command == 'em7':
                html = botCommands.em7(param1)
                messageStr = f"``` \n{html}\n ```"
                botFuncs.send_message(messageStr, personid = personId, markdown=True)
            if command == 'interface':
                try:
                    param2 = commandDict['param2']
                except KeyError:
                    param2 = None
                html = botCommands.interface(param1, param2)
                messageStr = f"``` \n{html}\n ```"
                botFuncs.send_message(messageStr, personid = personId, markdown=True)
            if command == 'snmp':
                html = botCommands.snmp(param1)
                messageStr = f"``` \n{html}\n ```"
                botFuncs.send_message(messageStr, personid = personId, markdown=True)
            
            if command == 'vlan':
                try:
                    param2 = commandDict['param2']
                except KeyError:
                    param2 = None
                html = botCommands.vlan(param1, param2)
                messageStr = f"``` \n{html}\n ```"
                botFuncs.send_message(messageStr, personid = personId, markdown=True)
                if param2 is None:
                    messageStr = 'please pass an vlan_name from the last message'
                    botFuncs.send_message(messageStr, personid = personId)
            if command == 'help':
                messageStr = '``` \n'
                for strCommand in listOfCommand:
                    messageStr += f'{strCommand} \n'
                messageStr += '```'
                botFuncs.send_message(messageStr, groupTitle=roomName, markdown=True)
            # running config is too big to send over teams
            # if command == 'run_config':
            #     runConfigList = botCommands.running_connfig(param1)
            #     hostname = runConfigList[0][0]
            #     runConfig = runConfigList[0][1]
            #     lastSeen = runConfigList[0][2]
            #     messageStr = f'``` {hostname} {lastSeen} \n {runConfig} ```'
            #     botFuncs.send_message(messageStr, groupTitle='BOT TEST - BETA Testing', markdown=True)
    time.sleep(6)
