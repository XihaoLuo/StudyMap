from flask import render_template, flash, redirect, url_for, request, jsonify, json
from app import app, db
from app.models import Building, StudySpace, User, Post
from app.forms import LoginForm, RegistrationForm, CheckinForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime, timedelta


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('map')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# helper takes array of User objects and sees if user with user_id is in it
def contains_user(users_array, user_id):
    for user in users_array:
        if user.id == user_id:
            return True
    return False

@app.route('/')
@app.route('/map')
@login_required
def map():
    # empty dictionary to be jsonified
    space_list = {"Spaces" : []}

    # populate dictionary with info for each study space
    study_spaces = StudySpace.query.all()
    for study_space in study_spaces:
        # list of posts recently made here
        recent_posts = Post.query.filter_by(studySpace_id = study_space.id). \
                filter(Post.timestamp <= datetime.utcnow()). \
                filter(Post.timestamp >= (datetime.utcnow() - timedelta(minutes=60))).all()

        #see which users posted (i.e. get unique # of posters & who they are)
        users_here = []
        for post in recent_posts:
            if not contains_user(users_here, post.user_id):
                users_here.append(post.author)

        tempDict = {
            "coordinates" : [study_space.lat, study_space.long],
            "room" : study_space.name,
            "building" : study_space.building.name,
            "id" : study_space.id,
            "num_occupants" : len(users_here)
        }
        space_list["Spaces"].append(tempDict)
    return render_template('map.html', title = "Map", spaces = json.dumps(space_list), num = 3)

@app.route('/feed')
@login_required
def feed():
    posts = Post.query.order_by(Post.timestamp.desc()).all() #order by timestamp later
    users = User.query.all() # users ordered by id
    spaces = StudySpace.query.all()
    return render_template('feed.html', title = "Feed", posts=posts, users=users, spaces=spaces)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/buildings')
@login_required
def buildings():
    buildings  = Building.query.all()
    return render_template('buildings.html', title = "List of Buildings and Spaces", buildings = buildings)


@app.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    form = CheckinForm()
    if form.validate_on_submit():
        space = StudySpace.query.filter_by(id = form.space_id.data).first()
        newPost = Post(body = form.post_body.data, building = space.building.name, \
            user_id = current_user.get_id(), studySpace_id = form.space_id.data)
        print(newPost.studySpace_id)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('feed'))
    return render_template('checkin.html', title='Check In', form=form)

@app.route('/makepost/')
@app.route('/makepost/<int:id>/')
@app.route('/makepost/<int:id>/<string:status>/')
@login_required
def makepost(id, status=''):
    space = StudySpace.query.filter_by(id = id).first_or_404()
    newPost = Post(body = status, building = space.building.name, user_id = current_user.get_id(),
            studySpace_id = id)
    db.session.add(newPost)
    db.session.commit()
    flash("Checked into " + space.name)
    return redirect(url_for('feed'))


@app.route('/profile/<name>')
@login_required
def profile(name):
    user = User.query.filter_by(username=name).first_or_404()
    users = User.query.all()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    spaces = StudySpace.query.all()
    last_seen = "User has no posts yet"
    last_session = None
    if(len(posts) != 0):
        last_seen_id = posts[0].studySpace_id
        last_seen = StudySpace.query.get(last_seen_id).name
        last_session = posts[0].timestamp

    num_posts = len(posts)
    return render_template('profile.html', user=user, users=users, posts=posts,
    spaces=spaces, last_seen=last_seen, last_session=last_session, num_posts=num_posts)
