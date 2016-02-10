""" Web end points """
from datetime import datetime

from flask import render_template, jsonify, redirect, url_for

from app import app
from app.forms import NoteForm


notes = []


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Home page """
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

    sorted_notes = sorted(notes, key=lambda k: k['date'], reverse=True)

    return render_template('index.html',
                            form=form,
                            notes=sorted_notes)


@app.route('/api/v1/notes', methods=['GET'])
def api_notes():
    """ API end point for all notes """
    return jsonify({ 'notes': notes })