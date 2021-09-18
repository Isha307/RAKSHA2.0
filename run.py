import sys
sys.path.append('./app')
sys.path.append('./app/backend')

from app import app1
app1.run(host='0.0.0.0', port=8080, debug = True)
