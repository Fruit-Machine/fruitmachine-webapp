# fruitmachine-webapp
Web application driving the Fruit Machine

This is a Python web application that performs the following functions:

1. Present a web interface asking the user various questions
2. Synthesize the answers into a 3-byte colour
3. ???
4. Profit

## Running this project:

0. Make sure you have Python installed. https://www.python.org/
1. Get the code:
```
  $ git clone https://github.com/Fruit-Machine/fruitmachine-webapp.git
  $ cd fruitmachine-webapp
```
2. Install Python dependencies "Flask" and "Phue"
```
  $ pip install flask phue
```
3. Run web app
```
  $ python3 app.py
```
4. Open your web browser to http://localhost:8080/

## Adding/editing questions:

Edit the `questions.json` file. Its format is fairly simple, which means that you can't really do anything too complicated with the questions. Each question entry is indexed by a number starting at 1, and contains the question text and a list of responses. It is recommended that there not be more than about 6 answers to any given question, because otherwise the interface will get crowded. This is not a hard and fast rule though -- the app won't break if a question has lots of answers.

### Hard and fast rules for editing `questions.json`:

1. Each question entry is composed of an index and a content.
2. The entries' indices must be sequential positive integers, starting at one, each surrounded by double quotes and followed by a colon. After the colon is a pair of curly braces containing the question content.
3. The question content must include a question string. This is composed of the word `"question"` (including double quotes), then a colon, then the question text surrounded by double quotes.
4. The question content must include a response list. This is composed of the word `"responses"` (including double quotes), then a colon, then a pair of square brackets. Inside the square brackets are the possible responses to the question, each surrounded by double quotes and all separated by commas.
5. The question string and response list must be separated from each other with a comma.
6. Entries must be separated by commas, placed after the closing curly brace.
7. The full set of entries must be surrounded by curly braces. There must be no text outside these braces.
8. For clarity and readability, whitespace (spaces, tabs, line breaks) may be placed anywhere in the file without changing the outcome of the file parsing, except inside double quotes.

The following is a sample questions.json file:
```
{
        "1": {
                "question": "On a scale from zero to five, how gay are you?",
                "responses": ["0", "1", "2", "3", "4", "5"]
        },
        "2": {
                "question": "Do you like to look at flowers?",
                "responses": ["Yes, very much", "Somewhat", "Meh", "Hate it"]
        }
}
```
