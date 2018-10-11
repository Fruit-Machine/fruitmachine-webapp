'''
    Begin app setup
'''
import os
app_directory = os.path.dirname(os.path.abspath(__file__))
home_directory = '~'
'''
    End app setup
'''

'''
Functions dealing with connecting to and communicating with the Hue bridge
'''
from phue import Bridge
# Set this to False to run the app without Hue support
with_hue = False
# IP address of the Hue bridge
bridge_ip = '192.168.1.2'
lamp_name = 'Gayness Lamp'
b = Bridge(bridge_ip) if with_hue else None

'''
    "run-once" connect command.
'''
def connect_hue():
    if not with_hue:
        return
    if os.path.isfile(home_directory + "/.python_hue"):
        return
    b.connect()

'''
change the colour of our bulb
'''
def set_light(xyb):
    if not with_hue: 
        return
    b.set_light(lamp_name, {'xy': xyb[0:2], 'bri': xyb[2]})

'''
Trigger the "colorloop" effect of the light
'''
def colorloop():
    if not with_hue:
        return
    b.get_light(lamp_name).effect('colorloop')

'''
Functions dealing with user objects: defining, updating, storing, loading
'''

import pickle
pickle_directory = app_directory + '/pickles'

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

def evaluate_user(user):
    import hashlib, colour
    # Create a hash of the user
    m=hashlib.md5()
    for key in sorted(user.keys()):
        if is_int(key):
            m.update(user[key].encode("utf-8"))
    user['hash'] = m.hexdigest()
    # Use the hash to generate gender and sexuality
    user['gender'] = genders[user['hash'][0]]
    user['sexuality'] = sexualities[user['hash'][1]]
    # Use the hash to generate a hex colour
    user['colour_hex'] = user['hash'][2:8]
    # Use the same section of the hash to generate an xy colour
    hexr = user['hash'][2:4]
    hexg = user['hash'][4:6]
    hexb = user['hash'][6:8]
    user['colour_xyb'] = colour.rgb_to_xyb(hexr, hexg, hexb)
    return user

# Given an ID, return a string path for the corresponding pickle file
def user_file(user_id):
    return pickle_directory + '/' + user_id.__str__() + '.pickle'

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

'''
Functions for dealing with the questions.json file: turning its entries
into question objects
'''

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

# Helper methods

# Return boolean indicating whether the given value is an int
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

