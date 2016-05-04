import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase

# Testing with LiveServer
class MyTest(LiveServerTestCase):
  # if the create_app is not implemented NotImplementedError will be raised
  def create_app(self):
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

  def test_flask_application_is_up_and_running(self):
    response = urllib2.urlopen(self.get_server_url())
    self.assertEqual(response.code, 200)
