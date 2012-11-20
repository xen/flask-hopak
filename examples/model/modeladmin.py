from flask import Flask, render_template

from flask.ext import gear
from flask.ext.pymongo import PyMongo

from formgear.models import Model, ModelRegistry
from formgear.utils import rel
from formgear.ds.mongo import MongoDS

class Post(Model):
    __yaml__=rel(__file__, 'post.yaml')

# Create flask app
app = Flask(__name__)
mongo = PyMongo(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/gear/">Click me to get to gear!</a>'


if __name__ == '__main__':
    # Create gear admin interface
    gear = gear.Admin()
    gear.add_model(Post)
    gear.init_app(app, MongoDS(mongo))

    # Start app
    app.debug = True
    app.run()
