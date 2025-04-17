import time
from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import gptAPI as chat
import tts
import secrets_keys
import settingsfile
import aioconsole

APP_ID = secrets_keys.TWITCH_APP_ID
APP_SECRET = secrets_keys.TWITCH_APP_SECRET
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = settingsfile.TWITCH_CHANNEL
last_call_time = 0
last_speak_call_time = 0
isActive = True

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Joining Channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here

# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    global last_call_time
    if not (msg.text.startswith('#') or msg.text.startswith('!')):
        #elapsed_time = time.monotonic() - last_call_time
        elapsed_time = asyncio.get_event_loop().time() - last_call_time
        if elapsed_time > settingsfile.COOL_DOWN:
            promptText = (f'{msg.user.name} said: {msg.text}')
            last_call_time = asyncio.get_event_loop().time()
            await prompt_tts(promptText)
        else:
            return

async def send_prompt(prompt):
    try: 
        return chat.send_input(prompt)
    except ValueError:
        return ""

async def prompt_tts(prompt):
    #Checks that the prompt has text, then sends it to chatGPT and TTS
    if(isinstance(prompt, str)):
        await play_tts(await send_prompt(prompt))

async def play_tts(message):
    #Checks that the prompt has test, then sends it to Text To Speech Module
    #message = message.replace("*","")
    if(isinstance(message, str)):
        await tts.play(message)

# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    await play_tts("Thank you for Subscribing")
    await prompt_tts({sub.sub_message})        

async def console_input():
    global isActive
    global last_call_time
    await asyncio.sleep(5)
    user_input = await aioconsole.ainput("Console: ")
    if not user_input.startswith('!'):
        await console_input()
    args = user_input[1:].split(' ')
    cmd = args[0].lower()
    args = args[1:]
    prompt = ' '.join(args)
    match cmd:
        case "tts":
            last_call_time = asyncio.get_event_loop().time()
            await play_tts(prompt)
        case "msg":
            last_call_time = asyncio.get_event_loop().time()
            await prompt_tts(prompt)
        case "close":
            print("Exiting Program")
            isActive = False
            return
        case "help":
            print("## Commands ## \n !tts - Text to Speech with Current voice \n !msg - chatGPT message completion \n !close - exit the program" )
    if(isActive):
        await console_input()
        

# this is where we set up the bot
async def run():
    global isActive
    global last_call_time
    global last_speak_call_time
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)
    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)

    # we are done with our setup, lets start this bot up!
    chat.start()
    asyncio.get_event_loop().create_task(console_input())
    # lets run till we press enter in the console
    while isActive:
        speak_time = asyncio.get_event_loop().time() - last_speak_call_time
        if speak_time > 1800:
                last_call_time = asyncio.get_event_loop().time()
                last_speak_call_time = asyncio.get_event_loop().time()
                await prompt_tts("speak")
        await asyncio.sleep(1)

    #try:
    #    input('press ENTER to stop')
    #finally:
        # now we can close the chat bot and the twitch api client
    chat.stop()
    await twitch.close()

if __name__ == "__main__":
    # lets run our setup
    asyncio.run(run())