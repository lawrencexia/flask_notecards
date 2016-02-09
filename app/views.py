from datetime import datetime

from flask import render_template, jsonify, redirect, url_for

from app import app
from app.forms import NoteForm


notes = [
        {
            'date': datetime.utcnow(),
            'title': 'Title 1',
            'message': 'test message 1'
        },
        {
            'date': datetime.utcnow(),
            'title': 'Title 2',
            'message': 'test mesage 2'
        }
    ]


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'nickname': 'Lawrence'}

    form = NoteForm()
    if form.validate_on_submit():
        notes.append({
            'date': datetime.utcnow(),
            'title': form.title.data,
            'message': form.message.data
            })
        return redirect(url_for('index'))
    else:
        print("No valid form")


    return render_template('index.html',
                            title='Home',
                            user=user,
                            form=form)

@app.route('/notes')
def all_notes():
    return render_template('notes.html',
                            title='Notes',
                            notes=notes)


@app.route('/api/v1/notes', methods=['GET'])
def api_notes():
    return jsonify({ 'notes': notes })