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
with_hue = True
# IP address of the Hue bridge
bridge_ip = '192.168.1.2'
lamp_name = 'Gayness Lamp'
try:
    b = Bridge(bridge_ip) if with_hue else None
except ConnectionRefusedError:
    with_hue = False

'''
    "run-once" connect command.
'''
def connect_hue():
    if not with_hue:
        return
    #if os.path.isfile(home_directory + "/.python_hue"):
    #    return
    b.connect()

'''
change the colour of our bulb
'''
def set_light(xyb):
    if not with_hue: 
        return
    b.set_light(lamp_name, {'on': True, 'xy': xyb[0:2], 'effect': 'none', 'bri': int(xyb[2]*255)})

'''
Trigger the "colorloop" effect of the light
'''
def colorloop():
    if not with_hue:
        return
    b.set_light(lamp_name, {'on': True, 'effect': 'colorloop'})

'''
Turn light off
'''
def light_off():
    if not with_hue:
        return
    b.set_light(lamp_name, {'on': False})

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
    # Hack a different colour:
    user['colour_xyb'] = colour.hack_xyb(hexr, hexg, hexb)
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

# Given a user, return a question object they haven't yet answered
def get_question(user):
    import json, random
    question_file = open(app_directory + '/questions.json')
    question_data = json.loads(question_file.read())
    question = False
    question_keys = list(question_data.keys())
    random.shuffle(question_keys)
    for key in question_keys:
        if is_int(key) and key not in user:
            question = question_data[key]
            question['id'] = key
            break
    # TODO remove question_data from the return
    return question, question_data

# Helper methods

# Return boolean indicating whether the given value is an int
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

