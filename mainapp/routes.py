from mainapp.models import *
from flask import escape, render_template, request, url_for, flash, redirect, abort, jsonify
from mainapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import re
from haversine import haversine, Unit


@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if current_user.business and not current_user.store:
            return redirect('store')
    return render_template('home.html', page='home')


@app.route('/register_account', methods=['POST'])
def register_account():
    business = request.form['business']=='true'
    if current_user.is_authenticated:
        return redirect(url_for(home))
    if User.query.filter_by(email=request.form['email']).all():
        return jsonify({'result' : 'failure', 'failure' : 'email'})
    elif User.query.filter_by(username=request.form['username']).all():
        return jsonify({'result' : 'faulure', 'failure' : 'username'})
    else:
        hashed_password = bcrypt.generate_password_hash(request.form['password'])
        u = User(username=request.form['username'], email=request.form['email'], password=hashed_password, business=business)
        db.session.add(u)
        db.session.commit()
        print(u)

        login_user(u, remember=request.form['remember'])
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/login', methods=['POST'])
def login():
    u = User.query.filter_by(username=request.form['username']).first()
    if u and bcrypt.check_password_hash(u.password, request.form['password']):
        login_user(u, remember=(request.form['remember']=='true') )
    else:
        return jsonify({'result':'failure', 'failure': 'user'})
    if u.business:
        return redirect(url_for('store'))
    else:
        return redirect(url_for('home'))


#settings page for people who own a store

@app.route('/store', methods=['GET', 'POST'])
def store():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    u = User.query.get(current_user.id)
    if not u.business:
        return redirect(url_for('home'))
    else:
        if not u.store:
            return render_template('setup_store.html', page='setup_store')
        if u.store:
            return render_template('store.html', store=u.store[0], page='store')



@app.route('/check_url', methods=['POST'])
def check_url():
    name = request.form['name'].strip().lower()
    url = "-".join(name.split(' '))
    if Store.query.filter_by(url=url).first():
        url = url+'-1'
    while Store.query.filter_by(url=url).first():
        url = url.split('-')
        url[-1] = str(int(url[-1])+1)
        url = '-'.join(url)
    return jsonify({'url' : url})


@app.route('/url_exists', methods=['POST'])
def url_exists():
    if Store.query.filter_by(url=request.form['name'].lower()).first():
        print(Store.query.filter_by(url=request.form['name']).first())
        return jsonify({'result': 'true'})
    else:
        print('no')
        return jsonify({'result': ''})


@app.route('/submit_store', methods=['POST'])
def submit_store():
    name = request.form['name']
    description = request.form['description']
    url = request.form['url'].lower()
    address = request.form['address']
    owner = current_user.id
    tags = request.form['tags']
    s = Store(name=name, description=description, url=url, address=address, owner=owner, tags=tags)
    db.session.add(s)
    db.session.commit()
    return jsonify({'result':'success'})

@app.route('/store/<store_url>', methods=['GET','POST'])
def global_store(store_url):
    store = Store.query.filter_by(url=store_url).first()
    if not store:
        return render_template('404.html', page='404')
    else:
        return render_template('store.html', store=store, page='store')
