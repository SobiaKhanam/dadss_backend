from django.db import models


class Fdensity(models.Model):
    fd_key = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    no_vessels = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fdensity'


class Narco(models.Model):
    n_key = models.IntegerField(primary_key=True)
    dtg = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    value = models.BigIntegerField(blank=True, null=True)
    flag = models.CharField(max_length=50, blank=True, null=True)
    item = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    vessel_name = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'narco'


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    reg_no = models.CharField(max_length=50, blank=True, null=True)
    reg_date = models.DateField(blank=True, null=True)
    boat_name = models.CharField(max_length=50, blank=True, null=True)
    boat_type = models.CharField(max_length=50, blank=True, null=True)
    boat_location = models.CharField(max_length=50, blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)
    pc_date = models.DateField(blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip'
