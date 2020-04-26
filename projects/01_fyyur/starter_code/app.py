#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jmromeo@localhost:5432/fyurr'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class VenueGenre(db.Model):
    __tablename__ = 'Venue_Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
      return f'<Genre id={self.id}, name={self.name}, venue={self.venue_id}>'

#come back and add zip code so its easier to search for venues in the same city
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genre = db.relationship('VenueGenre', backref='venue', cascade="all, delete-orphan")
    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable = False)
    seeking_talent_desc = db.Column(db.String, nullable = True)
    show = db.relationship('Show', backref='venue', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
      return f'<Venue id={self.id}, name={self.name}>'


    # return query that can be used to get past shows
    def q_past_shows(self, compare_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')):
      return self.show.filter(Show.start_time < compare_time)

    # return query that can be used to get upcoming shows
    def q_upcoming_shows(self, compare_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')):
      return self.show.filter(Show.start_time >= compare_time)

    # return upcoming shows count
    def upcoming_shows_count(self):
      return self.q_upcoming_shows().count()

    # return object with upcoming shows and past shows
    def shows(self):
      timenow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
      shows = {}
      shows['upcoming_shows'] = self.q_upcoming_shows(timenow).all()
      shows['past_shows'] = self.q_past_shows(timenow).all()

      return shows

class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    def __repr__(self):
      return f'<Genre id={self.id}, name={self.name}, artist={self.artist_id}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genre = db.relationship('Genre', backref='artist', cascade="all, delete-orphan")
    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=True) # only necessary if seeking venue is false
    show = db.relationship('Show', backref='artist', lazy='dynamic')

    def __repr__(self):
        return f'<Artist id={self.id}, name={self.name}>'

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
      return f'<Show id={self.id}, start_time={self.start_time}, venue={self.venue}, artist={self.artist}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  previousVenue = Venue()
  venues = Venue.query.order_by(Venue.state, Venue.city).all()

  for venue in venues:
    if previousVenue.city != venue.city or previousVenue.state != venue.state:
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [],
      })

    data[-1]['venues'].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_shows_count(),
    })

    previousVenue = venue

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_query = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

  venues = search_query.all()
  venue_count = search_query.count()

  data = []
  for venue in venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_shows_count(),
    })

  response = {
    "count": venue_count,
    "data": data,
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)

  # dynamic loading, grabbing queries for past and upcoming shows
  timenow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
  q_past_shows = venue.show.filter(Show.start_time < timenow)
  q_upcoming_shows = venue.show.filter(Show.start_time >= timenow)

  past_shows = []
  for show in q_past_shows.order_by(Show.start_time).all():
    past_shows.append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    })

  upcoming_shows = []
  for show in q_upcoming_shows.order_by(Show.start_time).all():
    upcoming_shows.append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    })
 
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": [genre.name for genre in venue.genre],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_talent_desc,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": q_past_shows.count(),
    "upcoming_shows_count": q_upcoming_shows.count(),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  newVenue = Venue()
  newVenue.name = request.form['name']
  newVenue.city = request.form['city']
  newVenue.state = request.form['state']
  newVenue.address = request.form['address']
  newVenue.phone = request.form['phone']
  newVenue.seeking_talent = False
  genres = request.form.getlist('genres')
  for genre in genres:
    newVenue.genre.append(VenueGenre(name=genre))

  error = False
  try:
    db.session.add(newVenue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Venue ' + newVenue.name + ' could not be listed.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.get(venue_id)
  venuename = venue.name

  error = False
  try:
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Venue ' + venuename + ' could not be deleted.')
  else:
    flash('Venue ' + venuename + ' was successfully deleted!')

  return jsonify(url=url_for('index'))
 
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_query = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  timenow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

  artists = search_query.all()
  artist_count = search_query.count()

  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.show.filter(Show.start_time > timenow)
    })

  results = {
    "count": artist_count,
    "data": data
  }

  return render_template('pages/search_artists.html', results=results, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  timenow = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

  data = []
  q_past_shows = artist.show.filter(Show.start_time < timenow)
  q_upcoming_shows = artist.show.filter(Show.start_time >= timenow)

  past_shows = []
  for show in q_past_shows.all():
    past_shows.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    })

  upcoming_shows = []
  for show in q_upcoming_shows.all():
    upcoming_shows.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S')
    })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": [genre.name for genre in artist.genre],
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": q_past_shows.count(),
    "upcoming_shows_count": q_upcoming_shows.count(),
  }

  return render_template('pages/show_artist.html', artist=data)
#  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(name = artist.name,
                    city = artist.city,
                    state = artist.state,
                    phone = artist.phone,
                    image_link = artist.image_link,
                    genres = [genre.name for genre in artist.genre],
                    facebook_link = artist.facebook_link,
                    )

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get(artist_id)

  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  genres = request.form.getlist('genres')
  artist.seeking_venue = False
  artist.genre = []
  for genre in genres:
    artist.genre.append(Genre(name=genre))

  error = False
  try:
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Artist ' + artist.name + ' could not be edited.')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully edited!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.get(venue_id)
  form = VenueForm(
                   name = venue.name,
                   city = venue.city,
                   state = venue.state,
                   address = venue.address,
                   phone = venue.phone,
                   image_link = venue.image_link,
                   genres = [genre.name for genre in venue.genre],
                   facebook_link = venue.facebook_link,
                  )

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)

  venue.name = request.form['name']
  venue.city = request.form['city']
  venue.state = request.form['state']
  venue.phone = request.form['phone']
  genres = request.form.getlist('genres')
  venue.seeking_venue = False
  venue.genre = []
  for genre in genres:
    venue.genre.append(VenueGenre(name=genre))

  error = False
  try:
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Venue ' + venue.name + ' could not be edited.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully edited!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  artist = Artist()
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.phone = request.form['phone']
  genres = request.form.getlist('genres')
  artist.seeking_venue = False
  for genre in genres:
    artist.genre.append(Genre(name=genre))

  error = False
  try:
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # probably need to fix to only show upcoming shows
  shows = Show.query.order_by(Show.start_time).all()

  data = []
  for show in shows:
    t = show.start_time
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": f'{t:%Y-%m-%dT%H:%M}:00.000Z'
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show = Show()
  show.venue_id = request.form['venue_id']
  show.artist_id = request.form['artist_id']
  show.start_time = datetime.fromisoformat(request.form['start_time'])

  error = False
  try:
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if error:
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Show could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

 


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
