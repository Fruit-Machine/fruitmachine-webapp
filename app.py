from flask import Flask, render_template, request, redirect, url_for
from phue import Bridge

'''
    Set up Hue bridge. We have here settings for the bridge, as well as a 
    "run-once" connect command.
'''
# IP address of the Hue bridge
bridgeip = '192.168.1.2'
# Connect to the bridge
b = Bridge(bridgeip)
# If the connection file doesn't exist, run the connect command
import os
if not os.path.isfile('/home/pi/.python_hue'):
    # Connect
    b.connect()
'''
    Finished Hue bridge setup
'''

'''
    Begin app setup
'''
app_directory = os.path.dirname(os.path.abspath(__file__))
pickle_directory = app_directory + '/pickles'
'''
    End app setup
'''

app = Flask(__name__)

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# Cake route
@app.route('/cake')
def cake():
    return 'Cake is a sweetie!'

# Start route
@app.route('/start', methods=['POST', 'GET'])
def start():
    # 
    if not 'name' in request.form:
        return redirect(url_for('index'))
    import random, sys
    user_id = (request.form['id'] if 'id' in request.form else random.randint(1, sys.maxsize))
    return render_template('start.html', user_name=request.form['name'], user_id=user_id)

# Question route
@app.route('/question/<question_id>', methods=['POST', 'GET'])
def question(question_id):
    # if the question number is not numeric then hax!
    if not is_int(question_id):
        return redirect(url_for('index'))
    if not 'id' in request.form:
        return redirect(url_for('index'))
    # Get the user ID and create a user object
    user = load_user(request.form['id'])
    # Add form data into user object
    for key in request.form:
        user[key] = request.form[key]
    # save pickle
    save_user(user)
    # Now let's load the question object
    question, qdata = get_question(question_id)
    # Render page
    if question:
        return render_template('question.html', user=user, question=question, qdata=qdata, next=int(question_id)+1)
    else:
        return redirect('/verdict/' + user['id'])

@app.route('/verdict/<user_id>')
def verdict(user_id):
    import hashlib
    m=hashlib.md5()
    user = load_user(user_id)
    for key in sorted(user.keys()):
        if is_int(key):
            m.update(user[key].encode("utf-8"))
    user['hash'] = m.hexdigest()
    user['gender'] = genders[user['hash'][0]]
    user['sexuality'] = sexualities[user['hash'][1]]
    return user.__str__()

'''
    Set up some colour constants
'''
xy = {
        'red': (0.675, 0.322),
        'green': (0.4091, 0.518),
        'blue': (0.167, 0.04),
        'yellow': (0.4325035269415173, 0.5007488105282536),
        'violet': (0.2451169740627056, 0.09787810393609737),
        'orange': (0.6007303214398861, 0.3767456073628519),
        'white': (0.32272672086556803, 0.3290229095590793)
}
'''
    End colour constants
'''

'''
    Set up our gender/sexuality categories
'''
genders = {
        '0': 'trans male',
        '1': 'trans female',
        '2': 'cis female',
        '3': 'cis male',
        '4': 'demigender male',
        '5': 'demigender female',
        '6': 'ambigender',
        '7': 'gender fluid',
        '8': 'agender',
        '9': 'bigender',
        'a': 'gender variant',
        'b': 'intersex',
        'c': 'two-spirit',
        'd': 'transmasculine',
        'e': 'transfeminine',
        'f': 'non-binary'
}
sexualities = {
        '0': 'homosexual',
        '1': 'ambisexual',
        '2': 'protosexual',
        '3': 'bisexual',
        '4': 'asexual',
        '5': 'demisexual',
        '6': 'pansexual',
        '7': 'heterosexual',
        '8': 'cryptosexual',
        '9': 'grey asexual',
        'a': 'bicurious',
        'b': 'autosexual',
        'c': 'perisexual',
        'd': 'xenosexual',
        'e': 'queer',
        'f': 'questioning'
}

# Test route for colours
@app.route('/colour/<colour>')
def colour(colour):
    if colour in xy:
        # Here we want to turn the lights a particular colour
        b.set_light('Gayness Lamp', 'xy', xy[colour])
    return render_template('colour.html', colour=colour, xy=xy)

# Helper methods

import pickle

# Return a user object corresponding to the given ID
def load_user(user_id):
    pickle_file = user_file(user_id)
    user = {}
    if os.path.isfile(pickle_file):
        # Read pickle file into user object
        pickle_in = open(pickle_file, 'rb')
        user = pickle.load(pickle_in)
        pickle_in.close()
    else:
        # Initialize user object
        user = {'id': user_id}
    return user

def save_user(user):
    pickle_out = open(user_file(user['id']), 'wb')
    pickle.dump(user, pickle_out)
    pickle_out.close()

# Given an ID, return a string path for the corresponding pickle file
def user_file(user_id):
    return pickle_directory + '/' + user_id.__str__() + '.pickle'

# Given a question number, return the corresponding question object
def get_question(number):
    import json
    question_file = open('questions.json')
    question_data = json.loads(question_file.read())
    question = False
    if number in question_data:
        question = question_data[number]
        question['id'] = number
    return question, question_data

# Return boolean indicating whether the given value is an int
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

