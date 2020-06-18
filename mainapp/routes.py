from mainapp.models import *
from flask import escape, render_template, request, url_for, flash, redirect, abort, jsonify
from mainapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import re
from geopy.geocoders import Nominatim
from geopy import distance
import geocoder
import secrets
import os
from PIL import Image
import time
import schedule
from collections import Counter
from nltk.corpus import wordnet
from sqlalchemy import and_, or_
import math
import random

### Routes ###

# Landing Page for login and Register aswell as feed
@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if current_user.business and not current_user.store:
            return redirect('store')
        else:
            location = current_user.location
            n = current_user.max_dist
            lat = float(location.split(',')[0])
            lng = float(location.split(',')[1])
            lng_n = n/(69*math.cos(float(lat)*(3.141/180)))
            lat_n = n/69
            items = Item.query.filter(Item.lat_dist(lat,lat_n) , Item.lng_dist(lng,lng_n)).all()
            random.shuffle(items)
            mystores = Follow.query.filter_by(user=current_user.id).all()
            lastids = {}
            for follow in mystores:
                diff = Store.query.get(follow.store).items[-1].id - follow.last_seen
                lastids.update({follow.store : diff})


            return render_template('feed.html', page='feed', items=items, mystores=mystores, lastids=lastids)
    else:
        return render_template('home.html', page='home')


# Post only ajax page for registering account
@app.route('/register_account', methods=['POST'])
def register_account():
    business = request.form['business']=='true'
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if User.query.filter_by(email=request.form['email']).all():
        return jsonify({'result' : 'failure', 'failure' : 'email'})
    elif User.query.filter_by(username=request.form['username']).all():
        return jsonify({'result' : 'faulure', 'failure' : 'username'})
    else:
        hashed_password = bcrypt.generate_password_hash(request.form['password'])

        location = request.form['loc']
        u = User(username=request.form['username'], email=request.form['email'], password=hashed_password, business=business, location=location)
        db.session.add(u)
        db.session.commit()


        login_user(u, remember=request.form['remember'])
        return redirect(url_for('home'))
    return redirect(url_for('home'))


# Logout
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Login ajax req
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



# Redirects to your store  -- also where store setup occurs
@login_required
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
            return redirect(url_for('global_store', store_url=u.store[0].url))


# For store setup, checks if given url exists already and spits one out for user based on store name
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

# Checks if the url already exists on store submit
@app.route('/url_exists', methods=['POST'])
def url_exists():
    if Store.query.filter_by(url=request.form['name'].lower()).first():
        return jsonify({'result': 'true'})
    else:
        return jsonify({'result': ''})

# For geolocating
# @app.route('/get_location', methods=['POST'])
# def get_location():
#     try:
#         geolocator = Nominatim()
#         ip = request.form['ip']
#         g = geocoder.ip(ip).latlng
#         location = geolocator.reverse(g).address
#     except:
#         return jsonify({'result' : 'failure'})
#     if location:
#         location = location.split(',')
#         location = ','.join([location[-3], location[-2]])
#         return jsonify({'location': location, 'coords' : g})

@app.route('/get_loc', methods=['POST'])
def get_loc():
    try:
        geolocator = Nominatim()
        lat = request.form['lat']
        lng = request.form['lng']
        location = geolocator.reverse(str(lat) +',' + str(lng))
        location = location.address
    except:
        return jsonify({'result' : 'failure'})
    if location:
        location = location.split(',')
        location = ','.join([location[-3], location[-2]])
        return jsonify({'location': location})



# Settings
@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    g = geocoder.ip('me').latlng
    geolocator = Nominatim()
    location = False
    try:
        location = geolocator.reverse(g).address
    except:
        return redirect(url_for('settings'))
    location = location.split(',')
    location = {
        'State' : location[-3],
        'Zip'   : location[-2]
    }

    return render_template('settings.html', page='settings', location=location)


# Follow / unfollow a store
@app.route('/check_following', methods=['POST'])
def check_following():
    following = Follow.query.filter_by(user=current_user.id, store=request.form['id']).first()
    if following:
        db.session.delete(following)
        db.session.commit()
        return jsonify({'result' : 'Follow'})
    else:
        s = Store.query.get(request.form['id']).name
        f = Follow(user=current_user.id, store=int(request.form['id']), storeName=s, last_seen=0)
        db.session.add(f)
        db.session.commit()
        return jsonify({'result' : 'Unfollow'})


# Create store account
@login_required
@app.route('/submit_store', methods=['POST'])
def submit_store():
    geolocator = Nominatim()
    name = request.form['name']
    description = request.form['description']
    url = request.form['url'].lower()
    address = request.form['address']

    location = geolocator.geocode(address)

    if not location:
        location = '0,0'
    else:
        location = str(location.latitude) + ', ' + str(location.longitude)
    owner = current_user.id
    tags = request.form['tags']
    s = Store(name=name, description=description, url=url, address=address, owner=owner, tags=tags, location=location)
    db.session.add(s)
    db.session.commit()
    return jsonify({'result':'success'})


# Page for stores
@login_required
@app.route('/store/<store_url>', methods=['GET','POST'])
def global_store(store_url):
    store = Store.query.filter_by(url=store_url).first()
    if not store:
        return render_template('404.html', page='404')
    else:
        following = Follow.query.filter_by(user=current_user.id, store=store.id).first()
        store = Store.query.filter_by(url=store_url).first()
        f = Follow.query.filter_by(store=store.id).all()
        f = len(f)
        return render_template('store.html', store=store, page='store', followers=f, following=following)

# On main page, - redirects to store based on store id
@login_required
@app.route('/store_redirect/<id>', methods=['GET', 'POST'])
def store_redirect(id):
    s = Store.query.get(id)
    return redirect(url_for('global_store', store_url=s.url))

# new item page
@login_required
@app.route('/new_item', methods=['GET','POST'])
def new_item():
    return render_template('newitem.html', page='newitem')

# new item upload
@login_required
@app.route('/newItemUpload', methods=['GET', 'POST'])
def newItemUpload():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            img = save_pic(image)
            width, height = img[1].size
            if width/height > 2:
                height = width/2
            if height/width > 2:
                width = height/2
            tags = [request.form['tag1'], request.form['tag2'], request.form['tag3'] ]
            metatags = []
            for i in tags:
                if i:
                    if wordnet.synsets(i):
                        metatags.extend(synonyms(i))
            tags.extend(request.form['description'].split(' '))
            metatags.extend(list(map(lambda c: c+'s', tags)))
            metatags = ', '.join(metatags)
            tags = ', '.join(tags)
            lat = current_user.store[0].location.split(',')[0]
            lon = current_user.store[0].location.split(',')[1]
            it = Item(description=request.form['description'], img=img[0], store=current_user.store[0].id, tags=tags, metatags=metatags, img_width = width, img_height=height, location=current_user.store[0].location, lat=lat, lng=lon)
            db.session.add(it)
            db.session.commit()

    return redirect('store')

@login_required
@app.route('/search', methods=['POST'])
def search():
    s = request.form['search']
    return redirect(url_for('search_query', query=s))

@login_required
@app.route('/search/<query>', methods=['GET','POST'])
def search_query(query):
    s = query.split()
    syns = map(lambda c : synonyms(c) if wordnet.synsets(c) else c, s)
    syns = list(syns)
    syns.extend(s)
    items = []
    for i in syns:
        if isinstance(i, list):
            for j in i:
                item = Item.query.filter(Item.metatags.contains(j)).all()
                items.extend(item)
        else:
            item = Item.query.filter(Item.metatags.contains(i)).all()
            items.extend(item)

    items = sorted(items, key = items.count,  reverse = True)
    items = list(dict.fromkeys(items))

    mystores = Follow.query.filter_by(user=current_user.id).all()
    for follow in mystores:
        diff = Store.query.get(follow.store).items[-1].id - follow.last_seen
        lastids.update({follow.store : diff})

    stores = Store.query.filter(Store.name.contains(query)).all()

    return render_template('feed.html', page='search', items=items, mystores=mystores, stores=stores, lastids=lastids)


@app.route('/delete_item', methods=['POST'])
def delete_item():
    i = Item.query.get(request.form['id'])
    os.remove('mainapp/' + url_for('static', filename='items/'+i.img))
    db.session.delete(i)
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/changebackground', methods=['POST'])
def changebackground():
    if request.method == 'POST':
        img = request.files['image']
        img = save_background_pic(img)
        s = Store.query.get(current_user.store[0].id)
        if s.img != 'store.jpg':
            os.remove('mainapp' + url_for('static', filename='store/'+s.img))
        s.img = img[0]
        db.session.commit()
    return redirect(url_for('store'))


@app.route('/update_max', methods=['POST'])
def update_max():
    newmax = request.form['newmax']
    current_user.max_dist = newmax
    db.session.commit()
    return jsonify({'result' : 'success'})


@app.route('/add_view_store', methods=['POST'])
def add_view_store():
    store = int(request.form['store'])
    s = Store.query.get(store)
    s.views +=1
    db.session.commit()
    return jsonify({'result' : 'success'})

@app.route('/add_item_view', methods=['POST'])
def add_view_item():
    item = int(request.form['item'])
    i = Item.query.get(item)
    i.views +=1
    db.session.commit()
    return jsonify({'result': 'success'})


@app.route('/clickthrough', methods=['POST'])
def clickthrough():
    item = int(request.form['item'])
    item = Item.query.get(item)
    item.clickthroughs +=1
    Store.query.get(item.store).clickthroughs += 1
    db.session.commit()
    return jsonify({'result' : 'success'})

@app.route('/update_last_seen', methods=['POST'])
def update_last_seen():
    id = int(request.form['storeid'])
    store = request.form['store']
    f = Follow.query.filter_by(user=current_user.id , store=store).first()
    f.last_seen = id
    db.session.commit()
    return jsonify({'result' : 'success'})



### Functions ###

def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\\items', picture_fn)
    output_size = (500,500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return [picture_fn , i]

def save_background_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\\store', picture_fn)
    #output_size = (1500,1500)
    i = Image.open(form_picture)
    #i.thumbnail(output_size)
    i.save(picture_path)
    return [picture_fn , i]


def synonyms(term):
    synset = wordnet.synsets(term)
    syns = map(lambda c: c.name() , synset[0].lemmas())
    return list(syns)

# def synonyms(term):
#     response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
#     soup = BeautifulSoup(response.text, 'html.parser')
#     soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
#     return [span.text for span in soup.findAll('a', {'class': 'css-r5sw71-ItemAnchor etbu2a31'})]
