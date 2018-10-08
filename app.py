from flask import Flask, render_template, request, redirect, url_for
from phue import Bridge
import fruit_machine

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
@app.route('/start', methods=['POST', 'GET'])
def start():
    # If we don't have a name, redirect back to index
    if not 'name' in request.form:
        return redirect(url_for('index'))
    import random, sys
    user_id = (request.form['id'] if 'id' in request.form else random.randint(1, sys.maxsize))
    return render_template('start.html', user_name=request.form['name'], user_id=user_id)

# Question route
@app.route('/question/<question_id>', methods=['POST', 'GET'])
def question(question_id):
    # if the question number is not numeric then hax!
    if not fruit_machine.is_int(question_id):
        return redirect(url_for('index'))
    if not 'id' in request.form:
        return redirect(url_for('index'))
    # Get the user ID and create a user object
    user = fruit_machine.load_user(request.form['id'])
    # Add form data into user object
    for key in request.form:
        user[key] = request.form[key]
    # save pickle
    fruit_machine.save_user(user)
    # If we don't have a selfie, forward to the photo page
    if not 'portrait' in user:
        return start()
    # Now let's load the question object
    question, qdata = fruit_machine.get_question(question_id)
    # Render page
    if question:
        return render_template('question.html', user=user, question=question, qdata=qdata, next=int(question_id)+1)
    else:
        return redirect('/verdict/' + user['id'])

@app.route('/verdict/<user_id>')
def verdict(user_id):
    user = fruit_machine.load_user(user_id)
    user = fruit_machine.evaluate_user(user)
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

# Test route for colours
@app.route('/colour/<colour>')
def colour(colour):
    if colour in xy:
        # Here we want to turn the lights a particular colour
        b.set_light('Gayness Lamp', 'xy', xy[colour])
    return render_template('colour.html', colour=colour, xy=xy)

# When we run this script directly, start a server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

