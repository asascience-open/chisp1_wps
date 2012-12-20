"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import views
import urllib2
from wps.models import Server

class WpsTests(TestCase):
    def test_describeProcess100(self):
        """
        Test of wps version 1.0.0 describe process function
        """
        response = views.describeProcess100("all").content
        assert response

    def test_execute100(self):
        """
        Test of wps version 1.0.0 execute function
        """
##        response = views.execute100("test_process", "value1=1;value2=2;value3=1").content
##        assert response == "<float>2.0</float>"
        pass

    def test_getCapabilities100(self):
        """
        Test of wps version 1.0.0 getcapabilities function
        """
        s = Server.objects.create(
                                  title="My Test Server Title",
                                  implementation_site="http://localhost:8000/")
        response = self.client.get('/wps/?request=GetCapabilities&Version=1.0.0')
        self.assertEqual(response.status_code, 200)

