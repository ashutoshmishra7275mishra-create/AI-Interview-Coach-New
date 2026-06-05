import speech_recognition as sr

def get_answer():

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            print("🎤 Speak now...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

            text = recognizer.recognize_google(audio)

            return text

    except Exception:

        print("\n❌ Voice not working.")
        print("⌨ Type your answer instead:")

        return input("Answer: ")