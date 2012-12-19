from flask import Flask, render_template

from flask.ext import hopak

# Create custom hopak view
class MyView(hopak.BaseView):
    @hopak.expose('/')
    def index(self):
        return self.render('myadmin.html')


class AnotherView(hopak.BaseView):
    @hopak.expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @hopak.expose('/test/')
    def test(self):
        return self.render('test.html')

# Create flask app
app = Flask(__name__, template_folder='templates')

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to admin!</a>'


if __name__ == '__main__':
    # Create admin interface
    admin = hopak.Admin()
    admin.add_view(MyView(category='Test'))
    admin.add_view(AnotherView(category='Test'))
    admin.init_app(app)

    # Start app
    app.debug = True
    app.run()
