from flask import Flask, render_template

from flask.ext import gear


# Create custom gear view
class MyGearView(gear.BaseView):
    @gear.expose('/')
    def index(self):
        return self.render('myadmin.html')


class AnotherGearView(gear.BaseView):
    @gear.expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @gear.expose('/test/')
    def test(self):
        return self.render('test.html')


# Create flask app
app = Flask(__name__, template_folder='templates')


# Flask views
@app.route('/')
def index():
    return '<a href="/gear/">Click me to get to gear!</a>'


if __name__ == '__main__':
    # Create gear interface
    gear = gear.Admin()
    gear.add_view(MyGearView(category='Test'))
    gear.add_view(AnotherGearView(category='Test'))
    gear.init_app(app)

    # Start app
    app.debug = True
    app.run()
