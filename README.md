# Mood Tracker

## About the Project

This app has been created to track a user's mental health. Explore the moods you've tracked to uncover trends, spot recurring feelings, and gain insights into how your emotions shift throughout your days and weeks.

### Built With

* [![Anaconda][anaconda]][anaconda-url]
* [![Streamlit][streamlit]][streamlit-url]

## Getting Started

Here's how you can get the app running on your machine.

### Installation

1. Clone the repo
    ```sh
    https://github.com/bethschoen/Mood_Tracker.git
    ```
2. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```
3. Create a new virtual environment
    ```
    conda create --name mt_venv
    ```
4. Install packages using `requirements.txt`
    ```
    conda install --yes --file requirements.txt
    ```
5. Create a new journal.json file in the data folder.

6. Run the app
    ```
    streamlit run app/app.py
    ```

### Project Repo

The following describes the repo structure, detailing where you can find specific files. 

```
Mood_Tracker
|
├── assets
|   └── styles.css - Mood button styles
|
├── data
|   ├── journal.json - User data, gitignored
|   └── moods.csv - Data storing moods, sentiments, and colours. Add custom moods here.
|
├── utils - Helper functions
|   ├── form_layout.py - Create a journal form, used in data edit and entry
|   ├── styles_creation.py - Automate the creation of the styles.css
|   ├── tags.py - Create and displaying rows of buttons/spans containing moods
|   └── word_frequency.py - Analyse word frequency in journal entries
|
├── app
|   ├── pages
|   |   ├── data_analysis.py - Calendar and plot view
|   |   ├── data_edit.py - Edit an existing journal entry (navigate here through journal.py)
|   |   ├── data_entry.py - Create a new journal entry
|   |   └── journal.py - View and filter journal entries
|   |   
|   └── app.py - Page navigation
|
└── variables.py - Constants used throughout files
```

## Usage

The Home page provides a calendar view of moods over the current month. This can be filtered using the mood buttons in the side bar.

![Home page][home-page]

Alternatively, the calendar can be switched to display anxiety level using the dropdown. 

![Anxiety calendar][anxiety-calendar]

Previous journal entries can be accessed via the "Journal View" navigation button in the sidebar. This will display all recorded information. There are buttons underneath each entry, allowing you to edit or delete them. 

![Journal][journal]

A new entry can be created by clicking "New Entry".

![New entry][new-entry]

[streamlit]: https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white
[streamlit-url]: https://streamlit.io/
[anaconda]: https://img.shields.io/badge/Anaconda-44A833?logo=Anaconda&logoColor=white
[anaconda-url]: https://anaconda.org/anaconda/python
[home-page]: assets/250813_home.png
[anxiety-calendar]: assets/250813_second_diary.png
[journal]: assets/250813_journal_view.png
[new-entry]: assets/250823_new_entry.png
