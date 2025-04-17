import asyncio
import subprocess
import edge_tts
import settingsfile
import requests
import secrets_keys
import aiohttp
import azure.cognitiveservices.speech as speechsdk

TEXT = "test of the tts file"
VOICE = settingsfile.VOICE_MODEL
EL_VOICE = settingsfile.EL_VOICE_ID
OUTPUT_FILE = "temp.mp3"
ELEVENLABS_API_KEY = secrets_keys.ELEVENLABS_API_KEY
USE_ELVEN_LABS = settingsfile.USE_EL
TTS_SERVER = settingsfile.TTS_SERVICE

async def play_edge(TEXT) -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    await play_mpv()
    #subprocess.run(["mpv", "--ontop=no", "--video=no", "--title=TTS VOICE", "--screen=1", "--window-minimized=yes", OUTPUT_FILE], creationflags=subprocess.CREATE_NO_WINDOW)

async def play(TEXT):
    #Used to start a subprocess when calling from outside this script]
    match TTS_SERVER:
        case 0:
            #await asyncio.get_event_loop().create_task(play_edge(TEXT))
            await play_edge(TEXT)
        case 1:
            #await asyncio.get_event_loop().create_task(play_elven(TEXT))
            await play_elven(TEXT)
        case 2:
            #await asyncio.get_event_loop().create_task(play_azure(TEXT))
            await play_azure(TEXT)

async def play_mpv() -> None:
    subprocess.Popen(["mpv", "--ontop=no", "--video=no", "--title=TTS VOICE", "--screen=1", "--window-minimized=yes", OUTPUT_FILE], creationflags=subprocess.CREATE_NO_WINDOW).wait()

async def play_elven(TEXT):
    global TTS_SERVER
    api_url = f'https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE}'

    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': ELEVENLABS_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        'text': "..." + TEXT,
        'voice_settings': {
            'stability': 0,
            'similarity_boost': 0
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload ) as response:
            # If the request was successful, save the MP3 output to a file
            if response.status == 200:
                mp3_bytes = await response.read()
                with open(OUTPUT_FILE, 'wb') as f:
                    f.write(mp3_bytes)
                await play_mpv()
            else:
                print(response.status)
                print('Error generating speech. Switching to backup.')
                TTS_SERVER = 2
                await play_azure(TEXT)

async def play_azure(TEXT):
    global TTS_SERVER
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = secrets_keys.AZURE_SPEECH_KEY
    service_region = "centralus"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=OUTPUT_FILE)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = settingsfile.AZURE_VOICE
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3)

    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    #speech_synthesizer.speak_text_async("I'm excited to try text-to-speech")
    ssml_string = f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n <voice name="en-AU-TinaNeural">\n <prosody pitch="5%">\n <mstts:express-as style="unfriendly"> <break strength="medium" /> {TEXT}\n  </mstts:express-as>\n </prosody>\n </voice>\n</speak>'

    result = speech_synthesizer.speak_ssml_async(ssml_string).get()
    #speechsdk.AudioDataStream(result)
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        await play_mpv()
    else:
        TTS_SERVER = 1
        await play_edge(TEXT)

def play_test(TEXT):
    match TTS_SERVER:
        case 0:
            asyncio.run(play_edge(TEXT))
        case 1:
            asyncio.run(play_elven(TEXT))
        case 2:
            asyncio.run(play_azure(TEXT))

async def test_mpv():
    await play_mpv()
    await play_mpv()
    await play_mpv()


if __name__ == "__main__":
    #asyncio.run(play_test("Test of the TTS file, hope this works as intended. Because I put in a lot of work."))
    asyncio.run(test_mpv())