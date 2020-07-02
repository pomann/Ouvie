from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload_cache'
app.config['VERSIONS_FOLDER'] = 'versions'
app.config['REBUILD_FOLDER'] = 'rebuild'

from ouvieapp import routes
