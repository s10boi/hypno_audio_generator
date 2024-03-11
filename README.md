# Hypno Audio Generator

## Description
### What is it?
This Python script generates a single text-to-speech audio file from multiple text files, for use in reinforcement/hypnosis audio files.

### Why would I want it?
It can be hard to find a hypnosis/reinforcement audio file that suits your specific tastes. This script allows you to create your own audio file by using text phrases you provide it, and you can loop and shuffle the lines as much as you like.

### What options does it have?
- **Repeat**: You can choose to repeat each text file any number of times.
- **Randomise**: You can choose to randomise the line order for each repeat.
- **Progress markers**: You can choose to insert audible "progress markers" every X% of the way through a section of the audio file (for example "Programming at 25%"), so that the subject knows how far through their programming scene they are.
- **Intro and Outro**: You can choose to add a "Beginning Program" and "Program Complete" phrase to the start and end of the completed script.
- **Join Multiple Files**: You can choose to join multiple text files into a single audio file, or generate separate audio files for each text file. For example, you could have an "intro" file that doesn't repeat and isnt suffled, and then a "main" file that repeats and is shuffled, which can export as a single mp3 file.
- **Your Language**: Since it uses your Operating System's text-to-speech engine, you can use any language or accent that your OS's text to speech engine supports - just write your text files in the appropriate language, and set your OS's default text-to-speech voice to the desired language/accent.

## Requirements
- Python 3.12 or later
- Pip or Poetry to install 3rd party packages

## Installation
1. Install the required Python packages: `pip install -r requirements.txt`, or `poetry install`, if you have Poetry installed.
2. Run the program, in order to set up the data import and export directories: `python main.py`.

## Usage
1. Set your OS's default text-to-speech voice to the desired voice. For Windows, you'll need to install language packs for any new languages/accents you wish to use - ensure you choose to install the text-to-speech packages.
2. Place .txt files in the `data/import` directory. Each file should have 1 phrase per line.
3. Run the program: `python main.py`.
4. Follow the prompts to choose each file in the order you want them to appear in the audio file. Additional prompts will ask for the number of times to repeat each file, and whether to randomise the line order for each repeat.
5. Enter the name of the export file when prompted, and a .mp3 file will be generated in the `data/export` directory.
6. Note that this is a **raw** audio file with just the text to speech voice speaking your script - you'll have to edit the .mp3 file in audio editing software (such as Audacity) to add any effects to make the file sound more suitable for hypnosis/reinforcement audio. More details on what I do can be found on my [blog](https://s10boi.blogspot.com/2024/03/how-i-make-hypno-programs.html)
