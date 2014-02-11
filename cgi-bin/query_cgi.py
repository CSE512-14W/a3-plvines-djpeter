#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

from query import *
from print_util import *

fields = cgi.FieldStorage()

# debugging code
if False:
	params = {}
	for key in fields.keys():
		params[key] = fields[key].value
	print_html([params])

# see which query and format
query = fields['query'].value
format = None # anything that doesn't match (including nothing) is assumed json
if 'format' in fields: format = fields['format'].value
# enough take order_by that we do it once here
order_by = None
if 'order_by' in fields: order_by = fields['order_by'].value

# obtain query results
query_result = []
if query == 'artists':
	year_min = fields['year_min'].value
	year_max = fields['year_max'].value
	limit = fields['limit'].value
	query_result = get_artists(year_min, year_max, limit, order_by)
elif query == 'similar':
	artist_id = fields['artist_id'].value
	year_min = fields['year_min'].value
	year_max = fields['year_max'].value
	limit = fields['limit'].value
	term = None
	# term breaks the query right now
	#if 'term' in fields: term = fields['term'].value
	query_result = get_similar_artists(artist_id, year_min, year_max, limit, order_by, term)
elif query == 'search':
	search = fields['search'].value
	limit = fields['limit'].value
	#query_result = get_artists_by_name_substring(search, limit)
	query_result = get_artists_by_main_name_substring(search, limit, order_by)
elif query == 'songs':
	artist_id = fields['artist_id'].value
	year_min = fields['year_min'].value
	year_max = fields['year_max'].value
	limit = fields['limit'].value
	query_result = get_songs(artist_id, year_min, year_max, limit)
elif query == 'terms':
	limit = fields['limit'].value
	query_result = get_terms(limit)
else:
	query_result = ['invalid query']

# output results
if (format == 'html'):
	print_html(query_result)
else:
	print_json(query_result)

	

