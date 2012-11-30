"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import views

class WpsTests(TestCase):
    def test_describeprocess100(self):
        """
        Test of wps version 1.0.0 describe process function
        """
        response = views.describeProcess100("all").content
        assert response == "['Test Process', 'This is a test process for the sci-wps server.', ['value1', 'value2', 'value3'], 'Process outputs xml of mutiplication of input values.']"

    def test_execute100(self):
        """
        Test of wps version 1.0.0 execute function
        """
        response = views.execute100("test_process", "value1=1;value2=2;value3=1").content
        assert response == "2.0"

    def test_getcapabilities100(self):
        """
        Test of wps version 1.0.0 getcapabilities function
        """
        pass
