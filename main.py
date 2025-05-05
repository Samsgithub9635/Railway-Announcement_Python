# Import necessary libraries
import os
import pandas as pd
from pydub import AudioSegment
from gtts import gTTS
import pyaudio

# Function to convert text to speech and save as an audio file
def textToSpeech(text, filename):
    myText = str(text)  # Convert text to string if it's not already
    language = 'bn'     # Bengali language code
    myobj = gTTS(text=myText, lang=language, slow=True)  # Create gTTS object
    myobj.save(filename)  # Save the speech as an audio file

# Function to merge multiple audio files into one
def mergeAudios(audios):
    '''This function returns pydubs audio segment'''
    combined = AudioSegment.empty()  # Create an empty AudioSegment
    for audio in audios:
        combined += AudioSegment.from_mp3(audio)  # Add each audio file to the combined AudioSegment
    return combined  # Return the combined AudioSegment

# Function to generate the skeleton of the announcement
def generateSkeleton():
    # 1-Generate "Anugroho Kore Sunben Gari Sankhya"
    audio = AudioSegment.from_mp3('BongRail.mp3')  # Load the base audio file
    start = 0  # Start time for the audio segment
    finish = 2000  # End time for the audio segment
    audioProcessed = audio[start:finish]  # Extract the specified segment
    audioProcessed.export("1_Beng.mp3", format='mp3')  # Save the extracted segment as a new audio file

    # 2. Train No. and Name and Platform No.
    # This part is missing in the original code, you need to add the code here

    # 3-Generate "No. Platform e asche"
    start = 7000  # Start time for the audio segment
    finish = 9000  # End time for the audio segment
    audioProcessed = audio[start:finish]  # Extract the specified segment
    audioProcessed.export("3_Beng.mp3", format="mp3")  # Save the extracted segment as a new audio file

# Function to generate announcements based on data from an Excel file
def generateAnnouncement(filename):
    df = pd.read_excel(filename)  # Read data from the Excel file into a DataFrame
    print(df)  # Print the DataFrame to inspect the data
    for index, item in df.iterrows():  # Iterate over each row in the DataFrame
        # Generate announcement text with train number, name, and platform
        announcement_text = f"{item['train_no']} {item['train_name']} {item['platform']}"
        textToSpeech(announcement_text, '2_Beng.mp3')  # Convert announcement text to speech and save as an audio file

        # Create a list of audio files to merge (assuming only 3 segments for now)
        audios = [f"{i}_Beng.mp3" for i in range(1, 4)]  # Change range if there are more segments
        
        # Merge the audio segments
        announcement = mergeAudios(audios)
        
        # Export the merged announcement as an audio file
        announcement.export(f"announcement_{item['time']}_{index+1}.mp3", format="mp3")

# Main function to execute the program
if __name__ == "__main__":
    print("Generating Skeleton...")
    generateSkeleton()  # Generate the skeleton of the announcement
    print("Now Generating Announcement...")
    generateAnnouncement("RailwayAnnouncement_Bangla.xlsx")  # Generate the announcements from the provided Excel file
