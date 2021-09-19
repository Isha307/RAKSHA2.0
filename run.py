import sys
sys.path.append('./app')
sys.path.append('./app/backend')

from app.apps import app
app.run(host='0.0.0.0', port=8080, debug = True)
