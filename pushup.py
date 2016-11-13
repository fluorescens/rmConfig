MYSQL info


        url(r'^config_done/(?P<numeric_device_id>[0-9]+)$', views.config_done, name='config_done'),
        url(r'^rec_config/(?P<numeric_device_id>[0-9]+)$', views.rec_config, name='rec_config'), 
        url(r'^getrec/(?P<numeric_device_id>[0-9]+)$', views.getrec, name='getrec'),
        url(r'^getstat/(?P<numeric_device_id>[0-9]+)$', views.getstat, name='getstat'),
        url(r'^postinst/(?P<numeric_device_id>[0-9]+)/(?P<data_package>[0-9]+)$', views.postinst, name='postinst'),



debug
net

class Reciever(models.Model):
        device_id = models.IntegerField(primary_key=True, blank=False, validators=[
                RegexValidator('^([0-9]|[1-9][0-9]|100)$', 'Device ID must be numeric.'),
        ])
        device_name = models.CharField(default="Reciever name", max_length=200)
        device_state = models.BigIntegerField(blank=False, validators=[
                RegexValidator('^[0-4294967295]$', '32-bit limit on assigning command strings.'),
        ])
        device_last_update = models.DateTimeField()

        def __str__(self):
                return str(str(self.device_id) + " " + str(self.device_name))

class Supplier(models.Model):
        device_id = models.IntegerField(primary_key=True, blank=False, validators=[
                RegexValidator('^([0-9]|[1-9][0-9]|100)$', 'Device ID must be numeric.'),
        ])
        device_name = models.CharField(blank=True, default="Supplier device", max_length=200)

        def __str__(self):
                return str(str(self.device_id) + " " + str(self.device_name))


class Instrument(models.Model):
        device_id = models.IntegerField(primary_key=True, blank=False, validators=[
                RegexValidator('^([0-9]|[1-9][0-9]|100)$', 'Device ID must be numeric.'),
        ])
	device_controller = models.ForeignKey(Supplier)
        instrument_typename = models.CharField(default="Instrument type", max_length=200)
        data = models.CharField(blank=True, default="", max_length=200)
        device_last_update = models.DateTimeField()

        def __str__(self):
                retu