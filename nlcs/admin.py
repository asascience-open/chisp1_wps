from django.contrib import admin
from nlcs.models import Lake, Tributary, WaterQuality, StreamGauge

admin.site.register(Lake)
admin.site.register(Tributary)
admin.site.register(WaterQuality)
admin.site.register(StreamGauge)

