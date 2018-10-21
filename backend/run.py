import sys

try:
	from app import app
	import namespaces.user
	import namespaces.house
	app.run(debug=True)
except ImportError as e:
	print('ERROR:', e, file=sys.stderr)
	if sys.version_info < (3,6):
		print('Please update your python version')
