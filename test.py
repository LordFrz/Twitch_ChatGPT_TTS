import time
import asyncio
import aioconsole

array1 = [{"role": "system",  "content": "my text"}]
array2 = []
array2.append(array1)
resetvar = 0
isactive = True

# initialize the last_call_time to 0, so the first call will always execute
last_call_time = 0

def on_message():
    global last_call_time
    elapsed_time = time.monotonic() - last_call_time
    print(f"Elapsed Time: {elapsed_time}")
    if elapsed_time > 5:
        text = "Code Ran"
        print(f'{text:#^20}')
        last_call_time = time.monotonic()    
    else:
        text = "Code NOT Ran"
        print(f'{text:*^20}')
    

def arraystuff(text):
    global resetvar
    global array2
    global array1

    array2.append({"role": "user", "content": text})

    if(resetvar >= 2):
        array2 = []
        array2.append(array1)
        resetvar = 0

    resetvar += 1
    print(array2)
    print(resetvar)

async def printTime():
    global isactive
    asyncio.get_event_loop().create_task(printInput())
    while isactive:
       await asyncio.sleep(1)
    print("Done")

async def printInput():
    global isactive
    user_input = await aioconsole.ainput("User Input: ")
    print(user_input)
    if(user_input != ""):
        asyncio.create_task(printInput())
    else:
        isactive = False

def printcase(Text):
    if not Text.startswith('!'):
        return
    args = Text[1:].split(' ')
    cmd = args[0]
    args = args[1:]
    prompt = ' '.join(args)
    match cmd:
        case "tts": 
            print("tts commands")
        case "msg":
            print("prompt return: " + prompt)
        case "close":
            print("Exiting Program")

def loop_prompt():
    user_input = input("Enter Text: ")
    if(user_input != ""):
        printcase(user_input)
        loop_prompt()

def run():
    asyncio.run(printTime())

if __name__ == "__main__":
     loop_prompt()
     #run()