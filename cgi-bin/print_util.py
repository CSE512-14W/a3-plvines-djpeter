import json

def print_html(records):
	print 'Content-type: text/html; charset=UTF-8\n\n'
	for r in records:
		#print r
		#print '<br><br>'
		print '<hr>'
		for key, value in r.iteritems():
			print key, ":", unicode(value).encode('UTF-8'), '<br>'

def print_json(records):
	print 'Content-type: application/json\n\n'
	print json.dumps(records)
