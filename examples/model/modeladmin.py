from flask import Flask, render_template

from flask.ext import hopak
from flask.ext.pymongo import PyMongo

from hopak.models import Model, ModelRegistry
from hopak.utils import rel
from hopak.ds.mongo import MongoDS

class Post(Model):
    __yaml__=rel(__file__, 'post.yaml')

# Create flask app
app = Flask(__name__)
mongo = PyMongo(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/afmin/">Click me to get to admin!</a>'


if __name__ == '__main__':
    # Create gear admin interface
    admin = hopak.Admin()
    admin.add_model(Post)
    admin.init_app(app, MongoDS(mongo))

    # Start app
    app.debug = True
    app.run()
