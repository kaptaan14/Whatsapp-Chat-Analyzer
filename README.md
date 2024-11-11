# Social Media Chat Analyzer

This project is a social media chat analyzer built with Python and Streamlit. The application provides various analyses on a chat log, including top statistics, activity timelines, activity maps, word cloud, most common words, emoji analysis, and sentiment analysis. The analysis can be done for a specific user or for the overall chat.

## Features

1. **Top Statistics**: Displays the total number of messages, total words, media shared, and links shared.

![image](https://github.com/Gaur2526/Images/raw/main/Top%20Statistics.png?raw=true)

2. **Activity Timelines**: Shows the monthly and daily activity timelines.
![image](https://github.com/Gaur2526/Images/raw/main/Monthly%20Activity%20Timeline.png)
![image](https://github.com/Gaur2526/Images/raw/main/Daily%20Activity%20Timeline.png)

3. **Activity Maps**: Visualizes the most busy day and month.
![image](https://github.com/Gaur2526/Images/raw/main/Activity%20Map.png)
![image](https://github.com/Gaur2526/Images/raw/main/Most%20Busy%20Users.png)
![image](https://github.com/Gaur2526/Images/raw/main/Weekly%20Activity%20Map.png)

4. **Word Cloud**: Generates a word cloud for frequent words.
![image](https://github.com/Gaur2526/Images/raw/main/Word%20Cloud%20for%20Frequent%20Words.png)

5. **Most Common Words**: Lists the most common words used in the chat.
![image](https://github.com/Gaur2526/Images/raw/main/Most%20Common%20Words.png)

6. **Emoji Analysis**: Analyzes the usage of emojis in the chat.
![image](https://github.com/Gaur2526/Images/raw/main/Emoji%20Analysis.png)

7. **Sentiment Analysis**: Performs sentiment analysis based on the text and emojis used in the messages.
![image](https://github.com/Gaur2526/Images/raw/main/Sentiment%20Analysis.png)

## Installation

1. Clone the repository:
```
gh repo clone Gaur2526/Whatsapp-Chat-Analyzer
```

2. Navigate to the project directory:
```
cd Whatsapp-Chat-Analyzer
```

3. Install the required Python packages:
```
pip/pip3 install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```
streamlit run app.py
```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload a chat log file using the file uploader in the sidebar.

![image](https://github.com/Gaur2526/Images/raw/main/DropBox.png)


4. Select a user from the dropdown menu in the sidebar.

5. Click the "Show Analysis" button in the sidebar to display the analysis.

## Project Structure

- `app.py`: The main Streamlit application.

- `preprocessor.py`: Contains the `preprocess` function for preprocessing the chat log.

- `helper.py`: Contains various helper functions for the analyses.

- `stopwords.txt`: A text file containing common stopwords to be excluded from the word cloud and most common words analysis.


