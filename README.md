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
4. Open your web browser to http://localhost:5000/

## Adding/editing questions:

Edit the `questions.json` file. Its format is fairly simple, which means that you can't really do anything too complicated with the questions.
