# InsightForge: YouTube Comment Analyzer

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Team Members](#team-members)
8. [Sprint Plan](#sprint-plan)
9. [License](#license)

## Introduction

Welcome to the YouTube Comment Analyzer project by InsightForge. Our application provides a quick and efficient way to analyze the sentiment of YouTube video comments. By inputting a YouTube video URL, users can receive a sentiment score ranging from -1 to +1, along with a detailed dashboard displaying various sentiment statistics.

## Features

- Analyze YouTube comments for sentiment and provide a score.
- Filter out URLs, hashtags, numbers, redundant whitespaces, and stop words in raw comments.
- User registration, login, and logout functionalities.
- Store and retrieve past analysis results.
- Compare statistics between two videos or a video analyzed at different times.
- Show the top most common words in a video.

## Technology Stack

- **Programming Language**: Python
- **Web Framework**: Flask
- **Database**: SQL
- **Libraries**:
  - googleapiclient.discovery
  - nltk
  - wordcloud
  - matplotlib
  - re
  - numpy
  - pillow

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**

   ```sh
   git clone https://github.com/InsightForge/YouTube-Comment-Analyzer.git
   cd YouTube-Comment-Analyzer
   ```

2. **Create a virtual environment**

   ```sh
   python3 -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```sh
   python app.py
   ```

## Usage

1. Before running the app.py file, make sure to run <manage.py> to establish the database on your system.
2. Open your web browser and navigate to `http://localhost:8008/`.
3. Register for an account or log in if you already have one.
4. Enter the YouTube video URL in the text box and submit.
5. View the sentiment analysis results on the dashboard.
6. Access past analysis results through the history section.

## Project Structure

```
YouTube-Comment-Analyzer/
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── html.py
|
├── static/
|   ├── images/
|       ├── copy-url.png
|       ├── error.png
|       ├── generate-pages.png
|       ├── InsightForge.png
|       ├── moon.png
|       ├── paste-url.png
|       └── sample.png
|       ├── select-pages.png
|   ├── basic.css
|   ├── dashboard.css
|   ├── home.css
|   └── tutorial.css
|
├── templates/
|   ├── auth/
|       ├── base.html
|       ├── login.html
|       └── signup.html
|   └── html/
|       ├── base.html
|       ├── dashboard.html
│       ├── home.html
|       └── tutorial.html
|
├── tests/
│   ├── functional/
|       ├── __init__.py
|       └── test_pages.py
|   ├── unit/
|       ├── __init__.py
|       └── test_models.py
|   └── conftest.py
|
├── analyzer.py
├── api_key.py
├── app.py
├── database.py
├── manage.py
├── models.py
├── pytest.ini
├── README.md
└── youtube_icon.png
```

## Team Members

- **Eilish Quan** - [equan9@my.bcit.ca](mailto:equan9@my.bcit.ca)
- **Ray Chu** - [rchu38@my.bcit.ca](mailto:rchu38@my.bcit.ca)
- **Hai (Peter) Wu** - [hwu138@my.bcit.ca](mailto:hwu138@my.bcit.ca)
- **Ngai-Lam (Tony) Chou** - [nchou8@my.bcit.ca](mailto:nchou8@my.bcit.ca)
- **Ashutosh (Ash) Dhatwalia** - [adhatwalia@my.bcit.ca](mailto:adhatwalia@my.bcit.ca)
- **Chu-Hsiang (Andrew) Hsu** - [chsu100@my.bcit.ca](mailto:chsu100@my.bcit.ca)

## Sprint Plan

### Week 1

- Develop backend logic for comment analysis.
- Set up initial project documentation.

### Week 2

- Implement Flask application and API routes.
- Develop basic web pages for user interaction.

### Week 3

- Enhance UI design.
- Implement user registration, login, and logout functionalities.
- Integrate database for storing analysis results.

### Week 4

- Complete database integration.
- Add features for viewing and comparing analysis results.

### Week 5

- Optimize code quality and runtime.
- Conduct thorough testing and bug fixing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
