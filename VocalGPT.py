import openai
openai.api_key = "YOUR-KEY-HERE"

import speech_recognition as sr
import pyttsx3

#empty
x=0
gptOutput = ""
mainList=[{"role": "system", "content": "You are a helpful assistant."}]


#convert text to speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speakText(command):
    engine.say(command)    
    engine.runAndWait()
    #engine.setProperty('rate',130)

#define response in understandable language        
def decodeGPT(response):
    response = str(response).split("\n")
    global validResponse
    validResponse = response[6]
    validResponse = validResponse[20:-2].replace('\\n', '\n').replace('\\u2019', '\'').replace('\\u201c', '\"').replace('\\u201d', '\"').replace("\\u00e9","e")
    print(validResponse)

print("I'm your virtual assistant. You can speak to me whenever you hear the beep, and you can say stop whenever you would like to end our conversation. How may I help you?")
speakText("I'm your virtual assistant. You can speak to me whenever you hear the beep, and you can say stop whenever you would like to end our conversation. How may I help you?")

while (x == 0):
    #listen to input
    # Initialize the recognizer
    r = sr.Recognizer()

    
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        speakText("beep")
        try:
            audio2 = r.listen(source2, timeout=10)
        except:
            print("Audio not recognized")
            speakText('Audio not recognized')
            break
        try:
            MyText = r.recognize_google(audio2)
        except:
            print("Audio not recognized")
            speakText('Audio not recognized')
            break
        MyText = MyText.lower()
    userInput = MyText
    print(userInput)
    if userInput == "stop":
        break

    #define input in gpt language
    userList = [{"role": "user", "content": f"{userInput}"}]
    mainList += userList
    
    #get response
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = mainList)
    decodeGPT(response)
    speakText(validResponse)
    gptOutput = validResponse
    gptList = [{"role": "assistant", "content": f"{gptOutput}"}]
    mainList += gptList

    


