import pyautogui as kbm
from time import sleep

def createCommand(message, cost, function):
    return (
        { 
            'message': message,
            'cost': cost,
            'function': function
        }
    )

# These are all the function which will be available
def pressKeyCommand(key:str, time:int=0.5):
    kbm.keyDown(key)
    sleep(time)
    kbm.keyUp(key)

def dropSequence(sequence:str):
    # List of characters - print each characters
    return

def jumpCommand():
    pressKeyCommand('space')

def wKeyCommand():
    pressKeyCommand('key', 10)

def dropAllCommand():
    kbm.keyDown('1')
    kbm.keyUp('1')
    kbm.keyDown('g')
    kbm.keyUp('g')
    kbm.keyDown('2')
    kbm.keyUp('2')
    kbm.keyDown('g')
    kbm.keyUp('g')

commands = {
    'jump': createCommand(None, 100, jumpCommand),
    'wkey': createCommand(None, 100, wKeyCommand),
    'dropall': createCommand(None, 100, dropAllCommand),
}


# if '!twerk' in msg.text:
#     if self.points > 4:
#         for i in range(0, 5):
#             pyautogui.keyDown('ctrl')
#             s(1)
#             pyautogui.keyUp('ctrl')
# if '!usec' in msg.text:
#     if self.points > 0:
#         pyautogui.keyDown('j')
#         s(2)
#         pyautogui.leftClick()
#         pyautogui.keyUp('j')
# if '!useq' in msg.text:
#     if self.points > 0:
#         pyautogui.keyDown('u')
#         s(2)
#         pyautogui.leftClick()
#         pyautogui.keyUp('u')
# if '!useult' in msg.text:
#     if self.points > 0:
#         s(2)
#         pyautogui.keyDown('/')
#         pyautogui.leftClick()
#         pyautogui.keyUp('/')
# if '!spray' in msg.text:
#     if self.points > 0:
#         s(1)
#         pyautogui.keyDown('=')
#         s(7)
#         pyautogui.keyUp('=')