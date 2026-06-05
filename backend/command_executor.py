import os
import webbrowser

def execute_command(command):

    command = command.lower()

    if "chrome" in command:
        os.system("start chrome")

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        webbrowser.open("https://www.google.com")

    elif "notepad" in command:
        os.system("notepad")

    elif "calculator" in command:
        os.system("calc")

    elif "vscode" in command:
        os.system("code")

    else:
        print("Command not found")