from app import db, Artist, Show, Genre, Venue, VenueGenre
from sqlalchemy import func
from datetime import datetime

artist0 = Artist()
artist0.name="Guns N Petals"
artist0.genre.append(Genre(name="Rock N Roll"))
artist0.city="San Francisco"
artist0.state="CA"
artist0.phone="326-123-5000"
artist0.website="https://www.gunspetalsband.com"
artist0.facebook_link="https://www.facebook.com/GunsNPetals"
artist0.seeking_venue=True
artist0.seeking_description="Looking for shows to perform at in the San Francisco Bay Area!"
artist0.image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"

artist1 = Artist()
artist1.name = "Matt Quevedo"
artist1.genre.append(Genre(name="Jazz"))
artist1.city = "New York"
artist1.state = "NY"
artist1.phone = "300-400-5000"
artist1.facebook_link = "https://www.facebook.com/mattquevedo923251523"
artist1.seeking_venue = False
artist1.image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"

artist2 = Artist()
artist2.name = "The Wild Sax Band"
artist2.genre.append(Genre(name="Jazz"))
artist2.genre.append(Genre(name="Classical"))
artist2.city = "San Francisco"
artist2.state = "CA"
artist2.phone = "432-325-5432"
artist2.seeking_venue = False
artist2.image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"

artist3 = Artist()
artist3.name="Mo Jo Yo Jo"
artist3.genre.append(Genre(name="Hip Hop Anonymous"))
artist3.city="Cool Cats"
artist3.state="CA"
artist3.phone="555-555-5000"
artist3.website="https://www.hoptothetop.com"
artist3.facebook_link="https://www.facebook.com/mojoyojo"
artist3.seeking_venue=True
artist3.seeking_description="Looking for shows to perform at in Cool Cats California!"
artist3.image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"


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
venue0.genre.append(VenueGenre("Rock N Roll"))
venue0.genre.append(VenueGenre("Jazz"))
venue0.genre.append(VenueGenre("Classical"))
venue0.address = "1015 Folsom Street"
venue0.seeking_talent = True
venue0.seeking_talent_desc = "We don't need talent, we need legends"

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

venue2 = Venue()
venue2.city = "New York"
venue2.state = "NY"
venue2.phone = "914-003-1132"
venue2.name = "The Dueling Pianos Bar"
venue2.genre.append(VenueGenre(name="Soul"))
venue2.address = "335 Delancey Street"
venue2.seeking_talent = True
venue2.seeking_talent_desc = "Yo we need some talent in this hizouse"

venue3 = Venue()
venue3.city = "Oakland"
venue3.state = "CA"
venue3.phone = "415-555-5555"
venue3.name = "Oakland Convention Center",
venue3.genre.append(VenueGenre(name="Alternative"))
venue3.address = "6824 Main St"
venue3.seeking_talent = False

db.session.add(venue0)
db.session.add(venue1)
db.session.add(venue2)
db.session.add(venue3)
db.session.commit()


show0 = Show()
show0.artist_id = Artist.query.first().id
show0.venue_id = Venue.query.first().id
show0.start_time = datetime.fromisoformat('2020-04-05T21:30:00.000')

db.session.add(show0)
db.session.commit()