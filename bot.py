import pyautogui
from dotenv import load_dotenv
import socket
from collections import namedtuple
import pyautogui as keyboard
from time import sleep as s
import os
import database as db

pyautogui.FAILSAFE = False

NAVY = (32, 42, 68)

Message = namedtuple(
    'Message',
    'prefix user channel irc_command irc_args text text_command text_args'
)

class Bot:
    def __init__(self):
        load_dotenv()

        self.db = db.Database()
    
        self.irc_server = 'irc.twitch.tv'
        self.irc_port = 6667
        self.oauth_token = os.getenv('OAUTH_TOKEN')
        self.username = 'CresentBot'
        self.channels = ['cresents']

        self.seeLogs = False
        self.valCommandsOn = True

        self.jumpPoints, self.dropAllPoints, self.wKeyPoints, self.twerkPoints = 20, 20, 20, 20

    def send_privmsg(self, channel: str, text: str) -> None:
        """Send a message into the Twitch chat
        Args:   
            channel (str): The id of the channel the message will go into
            text (str): The content of the message
        """
        self.send_command(f'PRIVMSG #{channel} :{text}')

    def send_command(self, command):
        if 'PASS' not in command:
            if self.seeLogs:
                print(f'< {command}')
        self.irc.send((command + '\r\n').encode())

    def connect(self):
        """Connecting the bot to the twitch channel
        """
        self.irc = socket.socket()
        self.irc.connect((self.irc_server, self.irc_port))
        self.send_command(f'PASS {self.oauth_token}')
        self.send_command(f'NICK {self.username}')
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
        self.loop_for_messages()

    def get_user_from_prefix(self, prefix) -> str:
        """Gets the username of the person who sends the message
        Args:
            prefix (str): Prefix of the user
        Returns:
            str: Returns either the user or None if the user couldn't be found
        """
        domain = prefix.split('!')[0]
        if domain.endswith('.tmi.twitch.tv'):
            #This then removes that part of the message from the
            return domain.replace('.tmi.twitch.tv', '')
        if 'tmi.twitch.tv' not in domain:
            return domain

        return None

    def parse_message(self, received_msg):
        parts = received_msg.split(" ")

        prefix = None
        user = None
        channel = None
        text = None
        text_command = None
        text_args = None
        irc_command = None
        irc_args = None

        if parts[0].startswith(':'):
            prefix=parts[0][1:]
            user = self.get_user_from_prefix(prefix)
            parts = parts[1:]

        #This will go through every element looking for one which starts with a colon
        text_start = next(
            (idx for idx, part in enumerate(parts) if part.startswith(':')),
            None
        )

        if text_start is not None:
            text_parts = parts[text_start:]

            #This is setting the first part of the text to not be a colon
            text_parts[0] = text_parts[0][1:]

            #This gives us the full message
            text = ' '.join(text_parts)

            #This gives us what we want out of the text we had (parse text will know hot to split it)
            text_command = text_parts[0]
            text_args = text_parts[1:]

            #This puts all the message parts to where the message starts so they are all together
            parts = parts[:text_start]

        irc_command = parts[0] #This will be PRIVMSG
        irc_args = parts[1:] #This will be #channel

        # This will go through every element looking for one which starts with a colon
        hash_start = next(
            (idx for idx, part in enumerate(irc_args) if part.startswith('#')),
            None
        )

        if hash_start is not None:
            channel = irc_args[hash_start][1:]

        message = Message(
            prefix=prefix,
            user=user,
            channel=channel,
            text=text,
            text_command=text_command,
            text_args=text_args,
            irc_command=irc_command,
            irc_args=irc_args,
        )

        return message

    def handle_commands(self, msg, text_command):
        # Dealing with user in database
        if not self.db.user_exists(msg.user):
            self.db.insert_user(msg.user)

        #Main commands that will always be running
        if text_command == "!help":
            self.send_privmsg(msg.channel, "!points - See total chat points \n")

        if text_command == "!hello":
            self.send_privmsg(msg.channel, "Hello " + msg.user + "! Hope you have a wonderful day!")

        if text_command == "!valcommands":
            self.send_privmsg(msg.channel, "!jump (" + str(self.jumpPoints) + " points), !wkey (" + str(self.wKeyPoints) + " points), !dropall (" + str(self.dropAllPoints) + " points), !twerk (" + str(self.jumpPoints) + " points)")

        if text_command == "!points":
            self.send_privmsg(msg.channel, f"@{msg.user}, you have {self.db.get_points(msg.user)} points! Chat to gain more points!")


        if '!jump' in text_command:
            if self.db.deduct_points(msg.user, self.jumpPoints):

                pyautogui.keyDown('space')
                s(0.5)
                pyautogui.keyUp('space')

                self.send_privmsg(msg.channel, f"@{msg.user}, you now have {self.db.get_points(msg.user)} points after using 'jump'!")
                self.db.add_transaction({ 
                    "username": msg.user,
                    "action": "Jump",
                    "points": self.jumpPoints,
                })
            else:
                self.send_privmsg(msg.channel, f"@{msg.user}, you don't have enough points to do that!")
        if '!wkey' in text_command:
            if self.db.deduct_points(msg.user, self.wKeyPoints):

                pyautogui.keyDown(']')
                s(5)
                pyautogui.keyUp(']')

                self.send_privmsg(msg.channel, f"@{msg.user}, you now have {self.db.get_points(msg.user)} points after using 'w key'!")
                self.db.add_transaction({ 
                    "username": msg.user,
                    "action": "wkey",
                    "points": self.wKeyPoints,
                })
            else:
                self.send_privmsg(msg.channel, f"@{msg.user}, you don't have enough points to do that!")
        if '!dropall' in msg.text:
            if self.db.deduct_points(msg.user, self.wKeyPoints):

                keyboard.keyDown('1')
                keyboard.keyUp('1')
                keyboard.keyDown('g')
                keyboard.keyUp('g')
                keyboard.keyDown('2')
                keyboard.keyUp('2')
                keyboard.keyDown('g')
                keyboard.keyUp('g')

                self.send_privmsg(msg.channel, f"@{msg.user}, you now have {self.db.get_points(msg.user)} points after using 'drop all'!")
                self.db.add_transaction({ 
                    "username": msg.user,
                    "action": "Drop All",
                    "points": self.dropAllPoints,
                })
            else:
                self.send_privmsg(msg.channel, f"@{msg.user}, you don't have enough points to do that!")

        # Adding 10 points to the user after their command
        self.db.add_points(msg.user, 10)

    def handle_message(self, received_msg):
        if len(received_msg) == 0:
            return

        msg = self.parse_message(received_msg)
        if self.seeLogs:
            print(f'> {msg}')

        #This is used to keep the connection alive between the bot and twitch
        if msg.irc_command == 'PING':
            self.send_command('PONG :tmi.twitch.tv')

        if msg.irc_command == 'PRIVMSG':
            self.handle_commands(
                msg, #Full message
                msg.text_command, #This wil be the command said
            )

    def loop_for_messages(self):
        while True:
            received_msgs = self.irc.recv(2048).decode()
            for msg in received_msgs.split('\r\n'):
                self.handle_message(msg)


def main():
    bot = Bot()
    bot.connect()


if __name__ == "__main__":
    main()