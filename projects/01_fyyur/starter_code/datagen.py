from app import db, Artist, ArtistGenre, Show, Venue, VenueGenre
from sqlalchemy import func
import datetime
import random

def seed_database():
    # custom data.. too painful to make many for testing 
    gen_specific_data()

    # generating artists in a few cities
    gen_many_artists(4, "sfartist")
    gen_many_artists(2, "dallasartist", city="Dallas", state="TX")
    gen_many_artists(8, "laartist", city="Los Angeles", state="CA")

    # generating venues in a few cities
    gen_many_venues(5, "sfvenue")
    gen_many_venues(3, "detroitvenue", city="Detroit", state="MI")
    gen_many_venues(6, "nashvillevenue", city="Nashville", state="TN")

    # generating some shows in past and future
    gen_many_shows(8, datetime.datetime.utcnow() - datetime.timedelta(days=10)) # making shows 10 days ago
    gen_many_shows(6, datetime.datetime.utcnow() - datetime.timedelta(days=1)) # making shows 1 day ago
    gen_many_shows(6, datetime.datetime.utcnow() + datetime.timedelta(days=5)) # making shows 5 day in future
    gen_many_shows(6, datetime.datetime.utcnow() + datetime.timedelta(days=1)) # making shows 1 day in future


# number of shows should be less than number of artists and venues
# to avoid duplicate shows
def gen_many_shows(num_shows, start_time):
    artists = Artist.query.all()
    venues = Venue.query.all()
    artists_iter = iter(artists)
    venues_iter = iter(venues)

    shows = []
    for i in range (1, num_shows):
        new_show = Show()
        new_show.artist_id = next(artists_iter).id
        new_show.venue_id = next(venues_iter).id
        new_show.start_time = start_time
        shows.append(new_show)

    db.session.add_all(shows)
    db.session.commit()

def gen_many_venues(num_venues=10, name_prefix="venue_", city="San Francisco", state="CA", genre="Other"):
    venues=[]
    for i in range (1, num_venues):
        new_venue = Venue()
        new_venue.name = f'{name_prefix}{i}'
        new_venue.genre.append(VenueGenre(name=genre))
        new_venue.city = city
        new_venue.state = state
        new_venue.address = f"{i} {name_prefix}"
        new_venue.phone = "555-555-5555"
        new_venue.website_link = f"https://www.{name_prefix}{i}.com"
        new_venue.facebook_link = f"https://www.facebook.com/{name_prefix}{i}"
        new_venue.seeking_talent = False
        new_venue.image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        new_venue.listed_time = datetime.datetime.utcnow()
        venues.append(new_venue)
    
    db.session.add_all(venues)
    db.session.commit()


def gen_many_artists(num_artists=10, name_prefix="artist_", city="San Francisco", state="CA", genre="Other"):
    artists=[]
    for i in range (1, num_artists):
        new_artist = Artist()
        new_artist.name = f'{name_prefix}{i}'
        new_artist.genre.append(ArtistGenre(name=genre))
        new_artist.city = city
        new_artist.state = state
        new_artist.phone = "555-555-5555"
        new_artist.website="https://www.{name_prefix}{i}.com"
        new_artist.facebook_link="https://www.facebook.com/{name_prefix}{i}"
        new_artist.seeking_venue=False
        new_artist.image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        new_artist.listed_time = datetime.datetime.utcnow()
        artists.append(new_artist)
    
    db.session.add_all(artists)
    db.session.commit()


def gen_specific_data():
    artist0 = Artist()
    artist0.name="Guns N Petals"
    artist0.genre.append(ArtistGenre(name="Rock N Roll"))
    artist0.city="San Francisco"
    artist0.state="CA"
    artist0.phone="326-123-5000"
    artist0.website="https://www.gunspetalsband.com"
    artist0.facebook_link="https://www.facebook.com/GunsNPetals"
    artist0.seeking_venue=True
    artist0.seeking_description="Looking for shows to perform at in the San Francisco Bay Area!"
    artist0.image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    artist0.listed_time = datetime.datetime.utcnow()

    artist1 = Artist()
    artist1.name = "Matt Quevedo"
    artist1.genre.append(ArtistGenre(name="Jazz"))
    artist1.city = "New York"
    artist1.state = "NY"
    artist1.phone = "300-400-5000"
    artist1.facebook_link = "https://www.facebook.com/mattquevedo923251523"
    artist1.seeking_venue = False
    artist1.image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
    artist1.listed_time = datetime.datetime.utcnow()

    artist2 = Artist()
    artist2.name = "The Wild Sax Band"
    artist2.genre.append(ArtistGenre(name="Jazz"))
    artist2.genre.append(ArtistGenre(name="Classical"))
    artist2.city = "San Francisco"
    artist2.state = "CA"
    artist2.phone = "432-325-5432"
    artist2.seeking_venue = False
    artist2.image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
    artist2.listed_time = datetime.datetime.utcnow()

    artist3 = Artist()
    artist3.name="Mo Jo Yo Jo"
    artist3.genre.append(ArtistGenre(name="Hip Hop Anonymous"))
    artist3.city="Cool Cats"
    artist3.state="CA"
    artist3.phone="555-555-5000"
    artist3.website="https://www.hoptothetop.com"
    artist3.facebook_link="https://www.facebook.com/mojoyojo"
    artist3.seeking_venue=True
    artist3.seeking_description="Looking for shows to perform at in Cool Cats California!"
    artist3.image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    artist3.listed_time = datetime.datetime.utcnow()


    db.session.add(artist0)
    db.session.add(artist1)
    db.session.add(artist2)
    db.session.add(artist3)
    db.session.commit()


    venue0 = Venue()
    venue0.city = "San Francisco"
    venue0.state = "CA"
    venue0.phone = "123-123-1234"
    venue0.name = "The Musical Hop"
    venue0.genre.append(VenueGenre(name="Rock N Roll"))
    venue0.genre.append(VenueGenre(name="Jazz"))
    venue0.genre.append(VenueGenre(name="Classical"))
    venue0.address = "1015 Folsom Street"
    venue0.seeking_talent = True
    venue0.seeking_talent_desc = "We don't need talent, we need legends"
    venue0.listed_time = datetime.datetime.utcnow()

    venue1 = Venue()
    venue1.city = "San Francisco"
    venue1.state = "CA"
    venue1.phone = "415-000-1234"
    venue1.name = "Park Square Live Music & Coffee",
    venue1.genre.append(VenueGenre(name="Rap"))
    venue1.genre.append(VenueGenre(name="Rock N Roll"))
    venue1.genre.append(VenueGenre(name="Punk"))
    venue1.address = "34 Whiskey Moore Ave"
    venue1.seeking_talent = False
    venue1.listed_time = datetime.datetime.utcnow()

    venue2 = Venue()
    venue2.city = "New York"
    venue2.state = "NY"
    venue2.phone = "914-003-1132"
    venue2.name = "The Dueling Pianos Bar"
    venue2.genre.append(VenueGenre(name="Soul"))
    venue2.address = "335 Delancey Street"
    venue2.seeking_talent = True
    venue2.seeking_talent_desc = "Yo we need some talent in this hizouse"
    venue2.listed_time = datetime.datetime.utcnow()

    venue3 = Venue()
    venue3.city = "Oakland"
    venue3.state = "CA"
    venue3.phone = "415-555-5555"
    venue3.name = "Oakland Convention Center",
    venue3.genre.append(VenueGenre(name="Alternative"))
    venue3.address = "6824 Main St"
    venue3.seeking_talent = False
    venue3.listed_time = datetime.datetime.utcnow()

    db.session.add(venue0)
    db.session.add(venue1)
    db.session.add(venue2)
    db.session.add(venue3)
    db.session.commit()


    show0 = Show()
    show0.artist_id = Artist.query.first().id
    show0.venue_id = Venue.query.first().id
    show0.start_time = datetime.datetime.fromisoformat('2020-04-05T21:30:00.000')

    db.session.add(show0)
    db.session.commit()

if __name__ == "__main__":
    seed_database()
