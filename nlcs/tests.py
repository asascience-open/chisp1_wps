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

    def test_nlcs_describeProcess(self):
        s = Server.objects.create(
                                  title="My Test Server Title",
                                  implementation_site="http://localhost:8000/")
        response = self.client.get('/nlcs/?request=describeprocess&identifier=all')
        self.assertEqual(response.status_code, 200)

    def test_execute100(self):
        """
        Test of wps version 1.0.0 execute function
        """
        response = self.client.get('/nlcs/?request=execute&version=1.0.0&identifier=calc_nutrient_load&datainputs=lake=ontario%3Bdate=2013-01-01%3Bnutrient=nitrogen')
        self.assertEqual(response.status_code, 200)

    def test_execute100_callback(self):
        """
        Test of wps version 1.0.0 execute function
        """
        response = self.client.get('/nlcs/?callback=mytestfunction&request=execute&version=1.0.0&identifier=calc_nutrient_load&datainputs=lake=ontario%3Bdate=2013-01-01%3Bnutrient=nitrogen')
        self.assertEqual(response.status_code, 200)

    def test_getCapabilities100(self):
        """
        Test of wps version 1.0.0 getcapabilities function
        """
        s = Server.objects.create(
                                  title="My Test Server Title",
                                  implementation_site="http://localhost:8000/")
        response = self.client.get('/nlcs/?request=GetCapabilities&Version=1.0.0')
        self.assertEqual(response.status_code, 200)

