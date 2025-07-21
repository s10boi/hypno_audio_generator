# Hypno Audio Generator
🔞 **This program is only intended for use by those aged 18+**

This Python script generates a single text-to-speech audio file from multiple text files, for use in reinforcement/hypnosis audio files.

It can be hard to find a hypnosis/reinforcement audio file that suits your specific tastes. This script allows you to create your own audio file by using text phrases you provide it, and you can loop and shuffle the lines as much as you like.

**Note**: This script only produces the **raw** audio file, which you will probably want to edit in an audio editor to make it sound good in a hypnosis session. I have a [blog post](https://s10boi.blogspot.com/2024/03/how-i-make-hypno-programs.html) that details how I edit the raw audio file to make it sound good.

> **Looking for real-time audio generation?**
> If you want to generate hypnosis in real time, complete with all the audio effects, my other project [Dynamic Hypnosis Audio Generator](https://github.com/s10boi/dynamic_hypno_generator) is what you want instead.

## Features
- **Repeat**: You can choose to repeat each text file any number of times.
- **Randomise**: You can choose to randomise the line order for each repeat.
- **Progress markers**: You can choose to insert audible "progress markers" every X% of the way through a section of the audio file (for example "Programming at 25%"), so that the subject knows how far through their programming scene they are.
- **Intro and Outro**: You can choose to add a "Beginning Program" and "Program Complete" phrase to the start and end of the completed script.
- **Join Multiple Files**: You can choose to join multiple text files into a single audio file, or generate separate audio files for each text file. For example, you could have an "intro" file that doesn't repeat and isnt suffled, and then a "main" file that repeats and is shuffled, which can export as a single mp3 file.
- **Your Language**: Since it uses your Operating System's text-to-speech engine, you can use any language or accent that your OS's text to speech engine supports - just write your text files in the appropriate language, and set your OS's default text-to-speech voice to the desired language/accent.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Program](#running-the-program)
- [Editing the Raw Audio File](#editing-the-raw-audio-file)

## Requirements
- [Python 3.13](https://www.python.org/downloads/release/python-313/) or higher.
- **Optional**: [uv](https://docs.astral.sh/uv/) - to simplify dependency management and running the program, or pip if you prefer (see [installation notes](#installation) below).

## Installation
I strongly recommend using [uv](https://docs.astral.sh/uv/), which will simplify installing Python if you don't have it, as well as setting up dependencies and running the program, though you can also use `pip` if you prefer.

### Using `uv`
1. Clone or download the respository
2. Open a terminal in the project directory
3. Run the following command to install dependencies (this will also automatically install Python 3.13 if you don't have it):
    ```bash
    uv sync
    ```

### Using `pip`
1. Clone or download the repository
2. Open a terminal in the project directory
3. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv .venv
    ```
    **Note**: On Windows, you may need to use `python` or `py` instead of `python3`, depending on your setup.
4. Activate the virtual environment:
    - On MacOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
5. Run the following command to install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Choosing a Text to Speech Voice
The audio generated will automatically use your **system's default text-to-speech voice**.

#### MacOS
1. Go to **System Settings** > **Accessibility** > **Spoken Content**.
2. Under **System Voice**, select your preferred voice. You can press the ℹ️ icon to hear a sample of the voice or choose a different one from the list.

#### Windows 11
1. Search for "Text to Speech" in the Start menu - you want the option that opens in the old Control Panel.
2. Under **Voice Selection**, choose your preferred voice from the dropdown menu. You can click the **Preview Voice** button to hear a sample.

To install a new voice:
1. Go to **Settings** > **Time & Language** > **Speech**.
2. Under **Manage voices**, click **Add voices**.
3. Select the voice you want to install and click **Add**.
4. You may need to restart your computer for the new voice to be available, then follow the steps above to select it as your default voice.

#### Linux
I have not tested this on Linux, but the text to speech functionality uses espeak, which should be available on most distributions. You can install it using your package manager (e.g., `sudo apt install espeak` on Debian-based systems).

## Running the Program
The basic steps to generate an audio file are:
1. Create a text file containing the phrases you want to use.
2. Run the program to generate an audio file from the text file.
3. Follow the prompts from the program to choose your text file and set other options.
4. Take your outputted audio file and edit it in your preferred audio program.

### Setting Up Your Text File
1. Create a `.txt` file in the `data/import` directory.
2. Write your phrases in the file, with one phrase per line.

### Starting the Program
As with installation, I recommend using [uv](https://docs.astral.sh/uv/) to run the program, but you can also use `pip` if you prefer.

#### Using `uv`
1. Open a terminal in the project directory.
2. Run the following command to start the program:
    ```bash
    uv run main.py
    ```

#### Using `pip`
1. Open a terminal in the project directory.
2. Activate your virtual environment if you created one:
    - On MacOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
3. Run the following command to start the program:
    ```bash
    python3 main.py
    ```

### Using the Program
1. Follow the prompts to choose each file in the order you want them to appear in the audio file. Additional prompts will ask for the number of times to repeat each file, and whether to randomise the line order for each repeat.
2. Enter the name of the export file when prompted, and a .wav file will be generated in the `data/export` directory.

### Editing the Raw Audio File
This program will output a raw audio file that you will probably want to edit to make it sound good in a hypnosis session.

More details on what I do can be found on my [blog](https://s10boi.blogspot.com/2024/03/how-i-make-hypno-programs.html)
