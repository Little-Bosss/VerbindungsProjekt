from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

VOTES_FILE = 'votes.json'

def load_votes():
    try:
        with open(VOTES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_votes(votes):
    with open(VOTES_FILE, 'w') as file:
        json.dump(votes, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        name = request.form['name']
        votes = load_votes()

        if option == 'keep':
            votes[name] = votes.get(name, 0)
        elif option == 'give':
            receiver = request.form['receiver']
            if receiver not in votes:
                votes[receiver] = 0

            if votes[receiver] < 1:
                votes[name] = 0
                votes[receiver] += 1
            else:
                return "Error: Receiver already has the maximum allowed votes."

        save_votes(votes)
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/results')
def results():
    votes = load_votes()
    entitled_to_vote_once = [voter for voter, count in votes.items() if count == 0]
    allowed_to_vote_twice = [voter for voter, count in votes.items() if count == 1]

    return render_template('results.html', once=entitled_to_vote_once, twice=allowed_to_vote_twice)

if __name__ == '__main__':
    app.run(debug=True)
