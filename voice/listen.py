import speech_recognition as sr

recognizer = sr.Recognizer()

def listen_to_patient():

    try:

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source
            )

            audio = recognizer.listen(
                source,
                timeout=5
            )

            text = recognizer.recognize_google(
                audio
            )

            return text

    except Exception as e:

        return f"Voice Error: {str(e)}"