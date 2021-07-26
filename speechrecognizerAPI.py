from fastapi import FastAPI
import speech_recognition as sr
import uvicorn
import requests
from fastapi.templating import Jinja2Templates

r1 =sr.Recognizer()

templates = Jinja2Templates(directory="templates")

app = FastAPI(title="Speech Recog")

@app.post("/webhook")
def get_speech():
    """The above function will take in a text reply from
           speech_recognition and then send the same to dialogflow api used below
           """
    with sr.Microphone() as source:  # use the default microphone as the audio source
        r1.adjust_for_ambient_noise(source, duration=5)
        print("please go ahead")
        audio = r1.listen(source)
        try:
            get_text = r1.recognize_google(audio)
            print(get_text)
        except:
            print("error 404")

        with open('speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())

    get_text = r1.recognize_google(audio)
    access_token = "ya29.a0ARrdaM_SQUvCfWoBnla5Dt0jemtwejLDI6HVByIOZEM_NR2Sn5C_UT5-x5Uc7_BM8KbStM8IUdZ7i5uK7cyFC72eitnia-Txt1_hRUHnxq5v2sFfPd7uPVXkr9wIz5BF04ph1KsWOU72xx0MRirgU_ij2I1ZtQ"
    refresh_token = "1//04c1Yj3BQRbWlCgYIARAAGAQSNwF-L9Ir1bTcRpEpe709RYY41zLJDN86fySO55cEQlmoblQmFy8B0XRz-LOAz7v2L_Hw62nx72M"

    # Project_id = "registrar-fbjx"    used below
    try:
        if get_text != None:
            url = "https://dialogflow.googleapis.com/v2/projects/registrar-fbjx/agent/sessions/None:detectIntent"
            params = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            body = {
                "queryInput": {
                    "text": {
                        "text": get_text,
                        "languageCode": "en"
                    }
                }
            }
            response = requests.post(url, params=params, json=body)
            print(response.json())

            # Now capture only required response from dialogflow.
            new_data = {
                "text": get_text,
                "intent_id": response.json().get("queryResult").get("intent").get("name"),  # Name url of the intent
                "intent_display_name": response.json().get("queryResult").get("intent").get("displayName"),
                # to display the displayName of the intent
                "confidence": response.json().get("queryResult").get("intentDetectionConfidence"),
                # intentDetectionConfidence
                "language_code": response.json().get("queryResult").get("languageCode"),  # the language_code
                "parameters": response.json().get("queryResult").get("parameters")
            }
            print(new_data)
            print("Process completed")
            return new_data

        else:
            return "Nothing is passed"
    except:
        return "Error"


