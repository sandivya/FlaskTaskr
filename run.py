from project import app
import os

port = int(os.environ.get('PORT', 7640)
app.run(host='0.0.0.0', port=port)
