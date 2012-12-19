from django.db import models

# Create your models here.

class Server(models.Model):
    # Server
    title    = models.CharField(max_length=1000, help_text="Server Title", blank=False)
    abstract = models.CharField(max_length=2000, help_text="Server Abstract", blank=True)
    keywords = models.CharField(max_length=2000, help_text="Comma Separated List of Keywords", blank=True)

    # Contact
    contact_person          = models.CharField(max_length=1000, help_text="Person to Contact", blank=True)
    contact_organization    = models.CharField(max_length=1000, help_text="Contact Organization", blank=True)
    contact_position        = models.CharField(max_length=1000, help_text="Contact Position (Optional)", blank=True)
    contact_street_address  = models.CharField(max_length=1000, help_text="Street Address (Optional)", blank=True)
    contact_city_address    = models.CharField(max_length=1000, help_text="Address: City (Optional)", blank=True)
    contact_state_address   = models.CharField(max_length=1000, help_text="Address: State or Providence (Optional)", blank=True)
    contact_code_address    = models.CharField(max_length=1000, help_text="Address: Postal Code (Optional)", blank=True)
    contact_country_address = models.CharField(max_length=1000, help_text="Address: Country (Optional)", blank=True)
    contact_telephone       = models.CharField(max_length=1000, help_text="Contact Telephone Number (Optional)", blank=True)
    contact_email           = models.CharField(max_length=1000, help_text="Contact Email Address", blank=True)
    contact_site            = models.CharField(max_length=1000, help_text="Contact Web Site", blank=True)

    # This implementation
    implementation_site     = models.CharField(max_length=1000, help_text="Web Address for This Implementation", blank=False)

# Add other implementation specific classes here
class StreamGauge(models.Model):
    river_segment_id = models.CharField(max_length=1000, help_text="NHN River Segment ID for both US and Canadian River Reaches", blank=False)
    sos_endpoint = models.CharField(max_length=1000, help_text="SOS Endpoint for this Stream Gauge and ID", blank=True)
    stream_gauge_id = models.CharField(max_length=1000, help_text="Stream gauge ID that corresponds to the station in the SOS endpoint", blank=False, unique=True)
    stream_gauge_name = models.CharField(max_length=1000, help_text="Stream gauge name", blank=True)
    stream_gauge_offerings = models.CharField(max_length=10000, help_text="Comma separated list of offerings for this station through SOS endpoint", blank=True)
    stream_gauge_parameters = models.CharField(max_length=50000, help_text="Comma separated list of observedProperty parameters for this station through SOS endpoint", blank=True)
    stream_gauge_x = models.DecimalField(help_text="Longitude or X coodinate", blank=True, max_digits=20, decimal_places=8)
    stream_gauge_y = models.DecimalField(help_text="Latitude or Y coordinate", blank=True, max_digits=20, decimal_places=8)
