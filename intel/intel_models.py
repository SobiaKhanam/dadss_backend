from django.db import models
from django.utils import timezone


class IntelReport(models.Model):
    ir_key = models.BigAutoField(primary_key=True)
    ir_reporter_name = models.CharField(max_length=255, blank=True, null=True)
    ir_reporting_time = models.DateTimeField(blank=True, null=True)
    ir_jetty = models.CharField(max_length=255, blank=True, null=True)
    ir_total_boats = models.IntegerField(blank=True, null=True)
    ir_pf_id = models.CharField(max_length=100, blank=True, null=True)
    ir_rdt = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'intel_report'

    @property
    def irdetails(self):
        return self.irdetails.all()


class IntelReportDetails(models.Model):
    ird_key = models.BigAutoField(primary_key=True)
    ird_ir_key = models.ForeignKey(IntelReport, on_delete=models.CASCADE, db_column='ird_ir_key', related_name='irdetails')
    ird_boat_types = models.CharField(max_length=255, blank=True, null=True)
    ird_total_boats = models.IntegerField(blank=True, null=True)
    ird_detected_from = models.DateTimeField(blank=True, null=True)
    ird_detected_to = models.DateTimeField(blank=True, null=True)
    ird_act_observed = models.TextField(blank=True, null=True)
    ird_transferring_loc = models.CharField(max_length=255, blank=True, null=True)
    ird_probability = models.FloatField(blank=True, null=True)
    ird_boat_picture = models.ImageField(upload_to='boat_images/', blank=True, null=True)
    ird_nakwa_name = models.CharField(max_length=255, blank=True, null=True)
    ird_number_of_crew = models.IntegerField(blank=True, null=True)
    ird_owner_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intel_report_details'
