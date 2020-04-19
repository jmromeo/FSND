from app import db, Artist, Show, Genre, Venue

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

#GenerateDBData()
#@    "id": 4,
#@    "name": "Guns N Petals",
#@    "genres": ["Rock n Roll"],
#@    "city": "San Francisco",
#@    "state": "CA",
#@    "phone": "326-123-5000",
#@    "website": "https://www.gunsnpetalsband.com",
#@    "facebook_link": "https://www.facebook.com/GunsNPetals",
#@    "seeking_venue": True,
#@    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#@    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#@    "past_shows": [{
#@      "venue_id": 1,
#@      "venue_name": "The Musical Hop",
#@      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#@      "start_time": "2019-05-21T21:30:00.000Z"
#@    }],
#@    "upcoming_shows": [],
#@    "past_shows_count": 1,
#@    "upcoming_shows_count": 0,
#@)
#@  # shows the venue page with the given venue_id
#@  # TODO: replace with real venue data from the venues table, using venue_id
#@  data1={
#@  }
#@  data2={
#@    "id": 5,
#@    "name": "Matt Quevedo",
#@    "genres": ["Jazz"],
#@    "city": "New York",
#@    "state": "NY",
#@    "phone": "300-400-5000",
#@    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#@    "seeking_venue": False,
#@    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#@    "past_shows": [{
#@      "venue_id": 3,
#@      "venue_name": "Park Square Live Music & Coffee",
#@      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#@      "start_time": "2019-06-15T23:00:00.000Z"
#@    }],
#@    "upcoming_shows": [],
#@    "past_shows_count": 1,
#@    "upcoming_shows_count": 0,
#@  }
#@  data3={
#@    "id": 6,
#@    "name": "The Wild Sax Band",
#@    "genres": ["Jazz", "Classical"],
#@    "city": "San Francisco",
#@    "state": "CA",
#@    "phone": "432-325-5432",
#@    "seeking_venue": False,
#@    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#@    "past_shows": [],
#@    "upcoming_shows": [{
#@      "venue_id": 3,
#@      "venue_name": "Park Square Live Music & Coffee",
#@      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#@      "start_time": "2035-04-01T20:00:00.000Z"
#@    }, {
#@      "venue_id": 3,
#@      "venue_name": "Park Square Live Music & Coffee",
#@      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#@      "start_time": "2035-04-08T20:00:00.000Z"
#@    }, {
#@      "venue_id": 3,
#@      "venue_name": "Park Square Live Music & Coffee",
#@      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#@      "start_time": "2035-04-15T20:00:00.000Z"
#@    }],
#@    "past_shows_count": 0,
#@    "upcoming_shows_count": 3,
#@  }
