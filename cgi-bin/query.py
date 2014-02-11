#!/usr/bin/env python

import sqlite3 as db

# some old code
def get_stuff():
	result = []
	#con = db.connect('sqlite/artist_similarity.db')
	#con = db.connect('sqlite/artist_term.db')
	con = db.connect('sqlite/track_metadata.db')
	cur = con.cursor()   
	cur.execute('SELECT * FROM sqlite_master WHERE type = "table"')
	for row in cur.fetchall():
		result.append(row)
	return result

def get_artist_details(artist_ids):
	con = None
	result = []
	try:
		con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()
 
		# also attach artist terms
		cur.execute('ATTACH ? as artist_term_db', ('sqlite/artist_term.db',) )


		for artist_id in artist_ids:
			new_record = {'artist_id':artist_id}

			# note that artist the max familiarity may be higher here...
			cur.execute('SELECT min(year), max(year), min(artist_familiarity), max(artist_familiarity), min(artist_hotttnesss), max(artist_hotttnesss) FROM songs WHERE artist_id = ? AND year > 0 LIMIT 1', (artist_id,))
			row = cur.fetchone()
			# hack for when the artist has no years for any songs (we skip that artist)
			if row[0] is None: continue
			new_record['year_first_song'] = row[0]
			new_record['year_last_song'] = row[1]
			new_record['artist_familiarity_min'] = row[2]
			new_record['artist_familiarity_max'] = row[3]
			new_record['artist_hotttnesss_min'] = row[4]
			new_record['artist_hotttnesss_max'] = row[5]
			
			# get the best artist name as the most common
			cur.execute('SELECT artist_name, COUNT(*) as `num` FROM songs WHERE artist_id = ? GROUP BY artist_name ORDER BY num DESC', (artist_id,))
			row = cur.fetchone()
			new_record['artist_name'] = row[0]
			# also list the rest of the artist names? (could set limit to one otherwise)
			include_other_names = False
			if include_other_names:
				all_artist_names = []
				for row in cur.fetchall():
					all_artist_names.append(row[0])
				new_record['other_artist_names'] = all_artist_names

			# get a sample of songs
			top_songs_each_year = True
			if top_songs_each_year:
				year_min = new_record['year_first_song']
				year_max = new_record['year_last_song']
				song_list = []
				for year in range(year_min, year_max+1):
					songs = get_songs(artist_id, year, year, 1)
					if len(songs) == 1: song_list.append(songs[0])
				new_record['top_songs'] = song_list
			else:
				early_song = get_songs(artist_id, new_record['year_first_song'], new_record['year_first_song'] + 1, 1)
				if (len(early_song) == 1):
					early_song = early_song[0]
				else:
					early_song = None
				
				middle_song = get_songs(artist_id, new_record['year_first_song'] + 1, new_record['year_last_song'] - 1, 1)
				if (len(middle_song) == 1):
					middle_song = middle_song[0]
					if (middle_song == early_song):
							middle_song = None
				else:
					middle_song = None

				late_song = get_songs(artist_id, new_record['year_last_song'] - 1, new_record['year_last_song'], 1)
				if (len(late_song) == 1):
					late_song = late_song[0]
					if (middle_song == late_song or early_song == late_song):
							late_song = None

				else:
					late_song = None

				new_record['top_songs'] = [early_song, middle_song, late_song]

			# get terms
			cur.execute('SELECT term FROM artist_term WHERE artist_term.artist_id = ?', (artist_id,))
			terms = []
			for row in cur.fetchall():
				terms.append(row[0])
			new_record['terms'] = terms
			
			result.append(new_record)

	except db.Error, e:
		result.append("Error %s:" % e.args[0])
	finally:
		if con:
		    con.close()
	return result


def get_artists(year_min, year_max, limit, order_by = None):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		#con = db.connect('sqlite/artist_term.db')
		con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   
  
		# get the artist ids
		core_query = 'SELECT distinct artist_id FROM songs WHERE year BETWEEN ? AND ? %s LIMIT ?'
		if order_by is None or order_by == 'artist_familiarity':
			query = core_query % 'ORDER BY artist_familiarity DESC'
		elif order_by == 'artist_hotttnesss':
			query = core_query % 'ORDER BY artist_hotttnesss DESC'
		else:
			raise Exception("unexpected order_by")
		cur.execute(query, (year_min, year_max, limit))
		artist_ids = [row[0] for row in cur.fetchall()]
		return get_artist_details(artist_ids)

	except db.Error, e:
		result.append("Error %s:" % e.args[0])
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']


def get_similar_artists(artist_id, year_min, year_max, limit, order_by = None, term = None):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		#con = db.connect('sqlite/artist_term.db')
		con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   
		
		cur.execute('ATTACH ? as artist_similarity_db', ('sqlite/artist_similarity.db',) )

		if term is None:
			core_query = 'SELECT distinct similarity.similar FROM similarity, songs WHERE similarity.target = ? AND similarity.similar = songs.artist_id AND year BETWEEN ? AND ? %s LIMIT ?'
			if order_by is None or order_by == 'artist_familiarity':
				query = core_query % 'ORDER BY artist_familiarity DESC'
			elif order_by == 'artist_hotttnesss':
				query = core_query % 'ORDER BY artist_hotttnesss DESC'
			else:
				raise Exception("unexpected order_by")
			cur.execute(query, (artist_id, year_min, year_max, limit))
		else:
			cur.execute('ATTACH ? as artist_term_db', ('sqlite/artist_term.db',) )
			# This doesn't work for some reason...query runs forever
			core_query = 'SELECT distinct similarity.similar FROM similarity, songs, artist_term WHERE similarity.target = ? AND similarity.similar = songs.artist_id AND year BETWEEN ? AND ? AND similarity.similar = artist_term.artist_id AND artist_term.term = ? %s LIMIT ?'
			#core_query = 'SELECT distinct similarity.similar FROM similarity, songs, artist_term WHERE similarity.target = ? AND similarity.similar = songs.artist_id AND year BETWEEN ? AND ? %s LIMIT ?'
			if order_by is None or order_by == 'artist_familiarity':
				query = core_query % 'ORDER BY artist_familiarity DESC'
			elif order_by == 'artist_hotttnesss':
				query = core_query % 'ORDER BY artist_hotttnesss DESC'
			else:
				raise Exception("unexpected order_by")
			cur.execute(query, (artist_id, year_min, year_max, limit, term))

		# in either case:
		artist_ids = [row[0] for row in cur.fetchall()]

		return get_artist_details(artist_ids)

	except db.Error, e:
		return [("Error %s:" % e.args[0])]
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']

# not bothering to fix this one because shouldn't be used
def get_artists_by_name_substring(search, limit):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		#con = db.connect('sqlite/artist_term.db')
		con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   
  
		
		include_details = True
		if include_details :
			# will return the most popular name, even if that name doesn't include the search term
			cur.execute('SELECT distinct artist_id FROM songs WHERE lower(artist_name) LIKE lower(?) ORDER BY artist_familiarity DESC LIMIT ?', ('%'+search+'%', limit))
			artist_ids = [row[0] for row in cur.fetchall()]
			return get_artist_details(artist_ids)
		else:
			# this gets all versions of the artist_name which contain the substring
			cur.execute('SELECT distinct artist_id, artist_name FROM songs WHERE lower(artist_name) LIKE lower(?) ORDER BY artist_familiarity DESC LIMIT ?', ('%'+search+'%', limit))
			result = []
			for row in cur.fetchall():
				new_record = {}
				new_record['artist_id'] = row[0]
				new_record['artist_name'] = row[1]
				result.append(new_record)
			return result

	except db.Error, e:
		return [("Error %s:" % e.args[0])]
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']


def get_artists_by_main_name_substring(search, limit, order_by = None):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		#con = db.connect('sqlite/artist_term.db')
		con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   

		core_query = 'SELECT distinct artist_id FROM songs X WHERE lower(artist_name) LIKE lower(?) AND lower(artist_name) in (SELECT lower(artist_name) FROM songs WHERE artist_id = X.artist_id GROUP BY artist_name ORDER BY COUNT(*) DESC LIMIT 1) %s LIMIT ?'
		if order_by is None or order_by == 'artist_familiarity':
			query = core_query % 'ORDER BY artist_familiarity DESC'
		elif order_by == 'artist_hotttnesss':
			query = core_query % 'ORDER BY artist_hotttnesss DESC'
		else:
			raise Exception("unexpected order_by")

		#cur.execute('SELECT distinct artist_id FROM songs X WHERE lower(artist_name) LIKE lower(?) AND lower(artist_name) in (SELECT lower(artist_name) FROM songs WHERE artist_id = X.artist_id GROUP BY artist_name ORDER BY COUNT(*) DESC LIMIT 1) ORDER BY artist_familiarity DESC LIMIT ?', ('%'+search+'%', limit))
		cur.execute(query, ('%'+search+'%', limit))
		artist_ids = [row[0] for row in cur.fetchall()]
		return get_artist_details(artist_ids)

	except db.Error, e:
		return [("Error %s:" % e.args[0])]
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']


def get_songs(artist_id, year_min, year_max, limit):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		#con = db.connect('sqlite/artist_term.db')
		con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   
  
		#cur.execute('SELECT artist_id, artist_name, title, year, track_7digitalid FROM songs WHERE artist_id = ? AND year BETWEEN ? AND ? ORDER BY artist_familiarity DESC LIMIT ?', (artist_id, year_min, year_max, limit))
		cur.execute('SELECT artist_id, artist_name, title, year, track_7digitalid FROM songs WHERE artist_id = ? AND year BETWEEN ? AND ? ORDER BY year ASC LIMIT ?', (artist_id, year_min, year_max, limit))
		result = []
		for row in cur.fetchall():
			new_record = {}
			new_record['artist_id'] = row[0]
			new_record['artist_name'] = row[1]
			new_record['title'] = row[2]
			new_record['year'] = row[3]
			new_record['track_7digitalid'] = row[4]
			result.append(new_record)
		return result

	except db.Error, e:
		return [("Error %s:" % e.args[0])]
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']

# terms look better, so not using this
def get_mbtags(limit):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		con = db.connect('sqlite/artist_term.db')
		#con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   
  
		cur.execute('select mbtag, count(*) from artist_mbtag group by mbtag order by count(*) desc limit ?', (limit,))
		result = []
		for row in cur.fetchall():
			new_record = {}
			new_record['mbtag'] = row[0]
			new_record['count'] = row[1]
			result.append(new_record)
		return result

	except db.Error, e:
		return [("Error %s:" % e.args[0])]
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']


def get_terms(limit):
	con = None
	try:
		#con = db.connect('sqlite/artist_similarity.db')
		con = db.connect('sqlite/artist_term.db')
		#con = db.connect('sqlite/track_metadata.db')
		cur = con.cursor()   
  
		cur.execute('select term, count(*) from artist_term group by term order by count(*) desc limit ?', (limit,))
		result = []
		for row in cur.fetchall():
			new_record = {}
			new_record['term'] = row[0]
			new_record['count'] = row[1]
			result.append(new_record)
		return result

	except db.Error, e:
		return [("Error %s:" % e.args[0])]
	finally:
		if con:
		    con.close()
	return ['unexpected end of function']


