import requests
import secrets_keys
import wordfilter as fltr
import settingsfile
import tts

model = settingsfile.GPT_MODEL
game_name = settingsfile.GAME_NAME
user_name = settingsfile.TWITCH_CHANNEL
apikey = secrets_keys.GPT_API_KEY
api_requests = 0
conversation_start = [{"role": "system",  "content": "You are responding to twitch chat messages. Respond as a tsundere named Mineva. If told to speak, just make small talk, say somthin about the game, or something random and asume you already introduced yourself. Only respond to the last message received. You are playing " + game_name + " Pretend you know everything about whatever game people ask about. Dont talk about being an AI language model. Keep your response to no more then 50 chatgpt api tokens. While you may talk to anyone, only take orders from " + user_name + ". Occationaly you can add your emotion for the response in the following one word format, *emotion* to show things such as *anger*, or *blushing* ect, but dont do it every time. If you get an inappropriate question, respond with {filtered}."}]
conversation_history = []
conversation_history = conversation_history + conversation_start
last_message = "No message"

def send_input(prompt):
    global conversation_history
    global api_requests
    global model
    global game_name
    global apikey
    global conversation_start
    global last_message

    if api_requests >= 20:
            conversation_history.clear()
            conversation_history = conversation_history + conversation_start
            api_requests = 0


    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + apikey
        }
        conversation_history.append({"role": "user", "content": prompt})
        data = {
            "model": model,
            "messages": conversation_history,
            "temperature": 0.7,
            "max_tokens": 80,
            "user": "twitch1"
        }
        api_requests += 1
        response = requests.post(url, headers=headers, json=data, timeout=35)
        response.raise_for_status()
        output = response.json()
        msg = output['choices'][0]['message']['content']
        msg = fltr.replace_text(msg)
        last_message = msg
        if response.status_code >= 200 and response.status_code < 300:
            conversation_history.append({"role": "assistant", "content": msg})
            return msg
        else:
            print("HTTP request failed with status code:" + response.status_code)
            return "gpt error, your code is fucked up sir"
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
        print(e)
        return "gpt servers are unreachable, ... Sadge"
    
def get_output():
    return last_message

def loop_prompt():
    user_input = input("Enter Text: ")
    if(user_input != ""):
        gpt_response = send_input(user_input)
        print(gpt_response)
        tts.play_test(gpt_response)
        loop_prompt()

if __name__ == "__main__":
     loop_prompt()