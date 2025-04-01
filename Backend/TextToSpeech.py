import pygame 
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

#Asynchronous function to convert text file to audio file.
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"  #Define the path where the audio file will be saved.

    if os.path.exists(file_path): #Check if the file already exists.
        os.remove(file_path)  #If the file exists, remove it to avoid overwriting errors.

    #create the communicate object to generate speech.
    communicate = edge_tts.Communicate(text,AssistantVoice,pitch='+4Hz',rate='+10%')
    await communicate.save(r'Data\speech.mp3') #Save the generated speech as an mp3 file.

# Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))
            
            # Initialize pygame mixer for audio playback
            pygame.mixer.init()
           
            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play() # Play the audio

            #Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:   #check if the external function stops.
                    break
                pygame.time.Clock().tick(10) #limit the loop to 10 ticks per second.

            return True #return True if the audio is played successfully.
        
        except Exception as e: #handle any exceptions.
            print(f"Error in TTS: {e}")

        finally:
            try:
                #call the priovided function with False to signal the end of TTS
                func(False)
                pygame.mixer.music.stop() #stop the audio playback.
                pygame.mixer.quit() #quit the pygame mixer.

            except Exception as e: #handle any exceptions during cleanup.
                print("Error in the finally block: {e}")

#function to manage text-to-speech with additional responses for long text.
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".") #Split the text by periods into a list of sentences.

    #list of perdefined responses for cases where the text is too long.
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    #if the text is very long (more than 10 sentences and 500 characters), add a responses message that says something like rest of the info. is on the chatscreen.
    if len(Data) > 10 and len(Text) >= 500:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)

    #otherwise , just play the whole text.
    else:
        TTS(Text, func)

#main execution loop
if __name__ == "__main__":
    while True:
        #prompt the user for input text and pass it to TextToSpeech function.
        TextToSpeech(input("Enter the text: "))
        
