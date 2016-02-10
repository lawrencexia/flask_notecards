# Part 1 (of potentially more) of the Flask Demo

This is a simple web app where the user is able to write down notes and have them displayed

## Prerequisites

In order to follow through this tutorial, you should have Python, VirtualEnv, and Pip ready to go on this machine. I'm writing this for OSX, so some of the command lines might be slightly different for different OS.

It also helps if you know some python, or a basic understanding of object oriented progamming and/or MVC web development. You could probably infer things I don't explicitly cover though.  

## Building out a simple Flask app in 10 minutes

The goal of this part of the Flask demo is to quickly demonstrate how to get a Flask app working. Specifically, we will make an app that allows the user to write messages, which will then be shown on the page. 

Let's start by setting up your virtual environment for package management. Since I'm on OSX, I run `virtualenv venv` and then activate the virtual environment with `. venv/bin/activate`. Read more [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install some packages that we need using pip:

    pip install flask
    pip install flask-wtf

And freeze our requirements to a text file (so we can quickly set up our environment on a different machine in the future).

    pip freeze > requirements.txt

Let's set up our app directory and make some folders:

    mkdir app
    mkdir app/static
    mkdir app/templates

The main app logic lives inside the `app` folder. Static web assets live in `app/static` and html templates (we'll see these in a sec) hang out in `app/templates`.

We want to add some logic in our app package initialization, so we'll create `app/__init__.py` and populate it with: 

    from flask import Flask

    app = Flask(__name__)

    from app import views

The `views` module is imported at the bottom to avoid circular dependencies

## Let's hello world something

Let's define some web end points, aka routes. Create the `app/views.py`, where we will put our controller/routing logic. Here, we make the necessary imports and return 'Hello World' when the user hits the '/' endpoint:

    @app.route('/')
    def index():
        """ Home Page """
        return 'Hello World'

The `@app.route` decorator defines the endpoint that this method routes for. Create a simple `run.py` script in the root folder to launch the app

    from app import app
    

    app.run(debug=True)

Note: debug is set to True, meaning when we update and save our code, the app will automatically reload. We can run the app with `python -m run`. You may have to set `run.py` as an executable with `chmod a+x run.py`.

Navigate to localhost:5000 to check out your hello world app!

## Forms

In order to enter some messages to ourselves, we'll have to create a form object. Let's do this in `app/forms.py` and definte the `NoteForm` class.

    """ Contains form classes """
    from flask.ext.wtf import Form
    from wtforms import StringField, TextAreaField
    from wtforms.validators import DataRequired


    class NoteForm(Form):
        """ Form representing a note """
        title = StringField('title')
        message = TextAreaField('message', validators=[DataRequired()])

Flask's WTForms library is an extension of WTForms. Here we define the two fields that have inputs, `title` and `message`, and we set it to the desired input type. I set the optional `validators` parameter for message to require data, since we don't really want blank messages!

Next, let's modify our `index` route in the `views` module to handle the Form. Let's also import a couple more modules we'll need:

    from flask import render_template

    from app import app
    from app.forms import NoteForm

    @app.route('/', methods=['GET', 'POST'])
    def index():
        """ Home page """
        form = NoteForm()
        return render_template('index.html',
                                form=form)

A bit more is happening here! Instead of returning a 'Hello World' string, we are returning the result of render_template on 'index.html', which is the web template we are about to make. Note that we can pass in values as well that will bake into the template. In our case, this is our NoteForm object. Flask uses Jinja2 as a templating engine. Also notice how we added methods in the `@app.route` decorator, specifying GET and POST requests. Our NoteForm will be posting to this end point. 

Let's create our first html template! Create `app/templates/index.html` and write in:

    <html>
        <head>
            <title>Note Card Site</title>
        </head>
        <body>
            <h1>Super sweet notecard app</h1>
            <form action="", method="post", name="new_note">
                {{form.hidden_tag()}}
                <table>
                    <tr>
                        <td>Title</td>
                        <td>{{form.title(size=32)}}</td>
                    </tr>
                    <tr>
                        <td>Message</td>
                        <td>{{form.message(cols=32, rows=4)}}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td><input type="submit" value="Submit"></td>
                    </tr>
                </table>
            </form>
        </body>
    </html>    
    
In the index template, we are able to bake in values from our form object using `{{ }}` notation. Before we take our new code for a spin, we need to configure our flask with a secret key and enables Flask's cross-site request forgery (CSRF) prevention logic.

Create a `config.py` file in root:

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'demo_app'

Next, configure the app using these values in `app/__init__.py`

    from flask import Flask

    app = Flask(__name__)
    app.config.from_object('config')

    from app import views

Cool! Load up `locahost:5000` and check out your shiny new web form!

## Saving and displaying notecards

Final stretch! Okay. Now we have our form, let's have it do something, amirite? First, I'll have to confess. I'm not going to cover persistant storage in this part, so we'll have to cheat a little bit and store our "Note Cards" in a python list. Let's create a variable `notes=[]` as a global variable in our `views` module. Next in there, let's add a little bit more logic in the `index` method. 

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

In `index`, if the form is validated through `form.validate_on_submit()`, we append a new note dict to our global `notes` list, with the date, title, and message. Afterwards, we call Flask's `redirect` method to redirect us to the url found by the Flask `url_for` method, in which we pass the name of the method of our desired route. 

Before we pass our list of note cards to the template to render, we sort them in descending order by the date.

We can display our note cards in the template: 

    <html>
        ...
        <body>
            ...
            <hr>
            <ul>
                {% for note in notes %}
                <li>
                    <span><b>{{note.title}}</b> - {{note.date}}</span>
                    <div>{{note.message}}</div>
                </li>
                {% endfor %}
            </ul>
        </body>
    </html>

We can iterate through a list in the template using the above notation, and display the date, title, and message for each item.

## Add a basic API end point

You might have noticed that we imported `jsonify` from flask earlier. Aha! You caught me. That's because we're going to expose a basic API end point. If you're interested in building a web app with seperated client server, you can still use Flask as the backend. Let's set up a quick API endpoint in the `views` module:

    @app.route('/api/v1/notes', methods=['GET'])
    def api_notes():
        """ API end point for all notes """
        return jsonify({ 'notes': notes })

Voila! Now you can query `localhost:5000/api/v1/notes` and see json data of all the notes you entered in. 

## Conclusion

Thanks for checking this out, and I hope you learned/are interested enough in Flask to take it for a spin yourself. If there is enough interest, I will continue this demo and hook the app up to a database for persistence 

