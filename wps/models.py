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
class RiverSegment(models.Model):
	title = models.CharField(max_length=1000, help_text="NHN River Segment ID for both US and Canadian River Reaches", blank=False)
	gauges_located_on_river = models.CharField(help_text="Comma Separated List of Stream Gauge IDs", blank=True)
