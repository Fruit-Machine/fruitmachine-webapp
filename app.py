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
@app.route('/question/<question>', methods=['POST', 'GET'])
def start(question):
    # if the question number is not numeric then hax!
    if not is_int(question):
        return redirect(url_for('index'))
    # If we don't have an ID then we generate one
    import random, sys
    user_id = (request.form['id'] if 'id' in request.form else random.randint(1, sys.maxsize))
    # We've got an ID; let's see if we've got a pickle file yet
    import pickle
    pickle_file = '/home/pi/fruitmachine-webapp/pickles/' + user_id.__str__() + '.pickle'
    user = {}
    if os.path.isfile(pickle_file):
        # Read pickle file into user object
        pickle_in = open(pickle_file, 'rb')
        user = pickle.load(pickle_in)
        pickle_in.close()
    else:
        # Initialize user object
        user = {'id': user_id}
    # Add form data into user object
    for key in request.form:
        user[key] = request.form[key]
    # save pickle
    pickle_out = open(pickle_file, 'wb')
    pickle.dump(user, pickle_out)
    pickle_out.close()
    # Render page
    return render_template('start.html', user=user)

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

# Test route for colours
@app.route('/colour/<colour>')
def colour(colour):
    if colour in xy:
        # Here we want to turn the lights a particular colour
        b.set_light('Gayness Lamp', 'xy', xy[colour])
    return render_template('colour.html', colour=colour, xy=xy)

# Helper methods

# Return boolean indicating whether the given value is an int
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

