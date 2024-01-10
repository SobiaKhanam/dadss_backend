from django.db import models


class Atrips(models.Model):
    atp_key = models.BigAutoField(primary_key=True)
    atp_av_key = models.BigIntegerField()
    atp_destination = models.CharField(max_length=50)
    atp_lastport = models.CharField(max_length=50, blank=True, null=True)
    atp_lasttime = models.DateTimeField(blank=True, null=True)
    atp_nextport = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atrips'


class Avessels(models.Model):
    av_key = models.BigAutoField(primary_key=True)
    av_id = models.CharField(max_length=50, blank=True, null=True)
    av_mmsi = models.CharField(max_length=50, blank=True, null=True)
    av_imo = models.CharField(max_length=50, blank=True, null=True)
    av_name = models.CharField(max_length=50, blank=True, null=True)
    av_callsign = models.CharField(max_length=50, blank=True, null=True)
    av_flag = models.CharField(max_length=50, blank=True, null=True)
    av_length = models.SmallIntegerField(blank=True, null=True)
    av_width = models.SmallIntegerField(blank=True, null=True)
    av_draught = models.SmallIntegerField(blank=True, null=True)
    av_built = models.SmallIntegerField(blank=True, null=True)
    av_type = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avessels'


class Rtrips(models.Model):
    rtp_key = models.IntegerField()
    rtp_source = models.CharField(max_length=50)
    rtp_dtg = models.DateTimeField()
    rtp_rv_key = models.IntegerField()
    rtp_direction = models.CharField(max_length=50)
    rtp_pcnum = models.CharField(max_length=50)
    rtp_pcissuedt = models.DateField(blank=True, null=True)
    rtp_pcduration = models.SmallIntegerField(blank=True, null=True)
    rtp_remarks = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rtrips'