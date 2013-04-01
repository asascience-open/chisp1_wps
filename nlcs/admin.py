from django.contrib import admin
from nlcs.models import Lake, Tributary, WaterQuality, StreamGauge

#class LakeAdmin(admin.ModelAdmin):
#    list_display = ('name', )
#    list_filter = ()
    
class TributaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'lake', 'country', 'has_nitrogen', 'has_phosphorus', 'has_stream')
    list_filter = ('lake', 'country', 'has_nitrogen', 'has_phosphorus', 'has_stream')

class WqAdmin(admin.ModelAdmin):
    list_display = ('name', 'station', 'tributary', 'has_nitrogen', 'has_phosphorus', 'startdate', 'enddate')
    list_filter = ('has_nitrogen', 'has_phosphorus', 'tributary')
    
class GaugeAdmin(admin.ModelAdmin):
    list_display = ('name', 'station', 'tributary', 'startdate', 'enddate')
    list_filter = ('tributary',)
    
admin.site.register(Lake)
admin.site.register(Tributary, TributaryAdmin)
admin.site.register(WaterQuality, WqAdmin)
admin.site.register(StreamGauge, GaugeAdmin)

