A project I was working on in 2023 when ChatGPT first popped off. Its all bad spegeti code, but might be usefull as an example of API actions.

As its wildly out of date, its doubtfull this works out of the box.

You will need to create an app on twitch and get the app api key. Update the API keys inside the secrets_Keys.py
Install everything in the requiernemnt.txt

This has support for:
  - Twitch Chat reading and messaging
  - Microsoft Azure TTS
  - Chat GPT API requests
  - Elven LAbs TTS (This one was expensive, so when using it, and you ran out of credist, it would automaticaly switch to one of teh otehr TTS services)
  - Edge TTS
  - Sureal DB (I dont think I fully implemeted this, I was going to use it for longer term memory for the chatGPT bot)

Much of what was planed is only half assed. Its all spegetti code tbh. 

When I had it running it would connect to Twitch chat, and read messages. Using those messages it would then send a chatGPT message request. 
Chatgpt would parse that request and return a message with the parameter set inside the gptAPI.py Which would then be sent to whichever 
TTS server was selected in the settingfile.py That would creeat a temp.mp3 or ovwrite the one that exists. Then that would trigger to play.\

So in this way you woudl be able to talk to a chatGPT bot via twitch chat. 

Thsi worked but had its issues. Such as the mp3 playing taking focus of the mouse out of whatever game I was playing. I did solve this, but I dont remeber how, 
as it was late at night after trying a bunch of stuff, and I didnt write it down >.<

This was just a prototype to figure out how to have all the services and API talking to each other, so it was a hot mess of coding.
