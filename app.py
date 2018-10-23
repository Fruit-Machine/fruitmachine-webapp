from flask import Flask, render_template, request, redirect, url_for
import fruit_machine as fm

app = Flask(__name__)

# Default route
@app.route('/')
def index():
    fm.light_off()
    return render_template('index.html')

# Form submission route. This is the route used by all form 
# submissions.
@app.route('/submit/', defaults={'user_id': None}, methods=['POST', 'GET'])
@app.route('/submit/<user_id>', methods=['POST', 'GET'])
def submit(user_id):
    # If we don't yet have a user ID, create one
    if not user_id:
        import random, sys
        user_id = random.randint(1, sys.maxsize)
    # Load an existing user or create an empty one
    user = fm.load_user(user_id)
    # Add form data into user object
    for key in request.form:
        user[key] = request.form[key]
    # Save any files uploaded
    import os
    for name in request.files:
        file_obj = request.files[name]
        filename, file_extension = os.path.splitext(file_obj.filename)
        dst_url = url_for('static', filename='portraits/' + user_id.__str__() + file_extension)
        dst_path = fm.app_directory + dst_url
        file_obj.save(dst_path)
        user[file_obj.name] = dst_url
    # Begin detection of which page we should be on
    if not user.get('name'):
        # We haven't filled out the index page yet
        return redirect(url_for('index'))
    # We've at least started the form; save the user
    fm.save_user(user)
    fm.colorloop()
    # Let's see how far along we are:
    if not user.get('2d') or not user.get('4d'):
        # We haven't completed the "digits" page yet
        return redirect(url_for('digits', user_id=user_id))
    if not user.get('portrait'):
        # We haven't completed the "portrait" page yet
        return redirect(url_for('portrait', user_id=user_id))
    if not user.get('headset'):
        # We haven't clicked "OK" on the headset page yet
        return redirect(url_for('headset', user_id=user_id))
    if not user.get('cancel'):
        # We haven't clicked "Cancel" on the user questions
        return redirect(url_for('question', user_id=user_id))
    # We've finished the whole process
    return redirect(url_for('compute', user_id=user_id))

# Cake route
@app.route('/cake')
def cake():
    return 'Cake is a sweetie!'

# Route for the digits-measuring page
@app.route('/digits/<user_id>')
def digits(user_id):
    user = fm.load_user(user_id)
    return render_template('digits.html', user=user)

# Route for taking a selfie
@app.route('/portrait/<user_id>')
def portrait(user_id):
    return render_template('portrait.html', user_id=user_id)

# Route for "headset" page
@app.route('/headset/<user_id>')
def headset(user_id):
    user = fm.load_user(user_id)
    return render_template('headset.html', user_id=user_id, user_portrait=user['portrait'])

# Question route
@app.route('/question/<user_id>')
def question(user_id):
    # let's load the question object and a count of answered questions
    question, qcount = fm.get_question(user_id)
    # Render page
    if question:
        return render_template('question.html', user_id=user_id, question=question, qcount=qcount)
    else:
        # Out of questions; skip to the end
        return redirect(url_for('compute', user_id=user_id))

@app.route('/compute/<user_id>')
def compute(user_id):
    user = fm.evaluate_user(user_id)
    fm.colorloop(1)
    return render_template('compute.html', user_id=user_id)

@app.route('/verdict/<user_id>')
def verdict(user_id):
    user = fm.evaluate_user(user_id)
    fm.set_light(user['colour_xyb'])
    return render_template('verdict.html', user=user)

@app.route('/debrief')
def debrief():
    return render_template('debrief.html')

# When we run this script directly, start a server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

