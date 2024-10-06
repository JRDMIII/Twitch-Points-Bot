import pyautogui as kbm
from time import sleep
import random

def createCommand(message, cost, function):
    return (
        { 
            'message': message,
            'cost': cost,
            'function': function
        }
    )

# These are all the function which will be available
def holdKeyCommand(key:str, time:int=0.5):
    """Holds down a key for a certain amount of time

    Args:
        key (str): Key to be pressed
        time (int, optional): Time the key will be pressed for. Defaults to 0.5.
    """
    kbm.keyDown(key)
    sleep(time)
    kbm.keyUp(key)

def pressKeyCommand(key:str):
    """Presses a key

    Args:
        key (str): Key to be pressed
    """
    kbm.keyDown(key)
    kbm.keyUp(key)

def pressSeqCommand(seq:str, time:int=0.25):
    """Presses a sequence of keys that are passed in

    Args:
        seq (str): The sequence of keys to be pressed
        time (int, optional): The time to wait between key presses. Defaults to 0.25.
    """
    for key in seq:
        pressKeyCommand(key)
        sleep(time)

def randomPresses(key:str, freq:int=3, min_interval:float=1, max_interval:float=1):
    """Presses a specified key a certain number of times with a random interval
    Args:
        key (str): The key to be pressed
        freq (int, optional): Number of times the key will be pressed. Defaults to 3.
        min_interval (float, optional): Lowest time interval between key presses. Defaults to 1.
        max_interval (float, optional): Highest time interval between key presses. Defaults to 1.
    """
    for _ in range(freq):
        pressKeyCommand(key)
        sleep(random.randint(min_interval, max_interval))

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