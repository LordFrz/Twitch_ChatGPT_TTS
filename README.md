A project I was working on in 2023 when ChatGPT first popped off. Its all bad spaghetti code, but might be useful as an example of API actions.

As its wildly out of date, its doubtful this works out of the box.

You will need to create an app on twitch and get the app api key. Update the API keys inside the secrets_Keys.py
Install everything in the requirements.txt
- pip install -r /path/to/requirements.txt

This has support for:
  - Twitch Chat reading and messaging
  - Microsoft Azure TTS
  - Chat GPT API requests
  - Elven LAbs TTS (This one was expensive, so when using it, and you ran out of credits, it would automatically switch to one of the other TTS services)
  - Edge TTS
  - Sureal DB (I dont think I fully implemented this, I was going to use it for long term memory for the chatGPT bot)

All these would be running asynchronously, which was a whole rabbit hole I went down for like a month, but it somehow all started working, lol.

Much of what was planed is only half assed. Its all spegetti code tbh. 

When I had it running, it would connect to Twitch chat, and read messages. Using those messages it would then send a chatGPT message request. 
ChatGPT would parse that request and return a message with the parameter set inside the gptAPI.py which would then be sent to whichever 
TTS server was selected in the settingfile.py That would create a temp.mp3 or overwrite the one that exists. Then that would trigger to play.\

So in this way you would be able to talk to a chatGPT bot via twitch chat. 

Thsi worked but had its issues. Such as the mp3 playing taking focus of the mouse out of whatever game I was playing. I did solve this, but I don't remember how, 
as it was late at night after trying a bunch of stuff, and I didn't write it down >.<

To run it, you would open a command line inside the folder everything is in. Then type "Python chatBot.py" This would then open you browser to have you verify
you twitch login in. Once that was done you would be connected to your twitch chat. The bot would then start listening for chat messages.

This was just a prototype to figure out how to have all the services and API talking to each other, so it was a hot mess of coding.

Here is a video of me running it and explaining some stuff. This is my buddy's abandoned youtube channel so you wont get any response there if you have question, sorry.
https://www.youtube.com/watch?v=dupNrakjm5s
