'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''

import azure.cognitiveservices.speech as speechsdk
import secrets_keys
# Creates an instance of a speech config with specified subscription key and service region.
speech_key = ""
service_region = "centralus"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name = "en-AU-TinaNeural"

text = "Test of the TTS file, i'm just talking a bunch to see how it sounds"

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

ssml_string = f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">\n <voice name="en-AU-TinaNeural">\n <prosody pitch="5%">\n <mstts:express-as style="unfriendly"> <break strength="medium" /> {text}\n  </mstts:express-as>\n </prosody>\n </voice>\n</speak>'


#result = speech_synthesizer.speak_text_async(text).get()
result = speech_synthesizer.speak_ssml_async(ssml_string).get()
# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
    stream = speechsdk.AudioDataStream(result)
    #stream.save_to_wav_file("path/to/write/file.wav")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

