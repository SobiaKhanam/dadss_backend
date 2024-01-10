# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class Grdensity(models.Model):
    grd_key = models.AutoField(primary_key=True)
    grd_gr_key = models.ForeignKey('Greports', models.DO_NOTHING, db_column='grd_gr_key', related_name='density')
    grd_position = models.TextField()
    grd_qty = models.SmallIntegerField()
    grd_type = models.CharField(max_length=100)
    grd_movement = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'grdensity'


class Greports(models.Model):
    gr_key = models.AutoField(primary_key=True)
    gr_pf_id = models.CharField(max_length=100)
    gr_dtg = models.DateTimeField()
    gr_position = models.TextField()
    gr_patroltype = models.CharField(max_length=100, blank=True, null=True)
    gr_fuelrem = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    gr_info = models.CharField(max_length=100, blank=True, null=True)
    gr_rdt = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'greports'

    @property
    def density(self):
        return self.density.all()

    def fishing(self):
        return self.fishing.all()

    def merchant(self):
        return self.merchant.all()


class Grfishing(models.Model):
    grf_key = models.AutoField(primary_key=True)
    grf_gr_key = models.ForeignKey(Greports, models.DO_NOTHING, db_column='grf_gr_key', related_name='fishing')
    grf_position = models.TextField()
    grf_name = models.CharField(max_length=100)
    grf_type = models.CharField(max_length=100)
    grf_movement = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'grfishing'


class Grmerchant(models.Model):
    grm_key = models.AutoField(primary_key=True)
    grm_gr_key = models.ForeignKey(Greports, models.DO_NOTHING, db_column='grm_gr_key', related_name='merchant')
    grm_position = models.TextField()
    grm_name = models.CharField(max_length=100)
    grm_type = models.CharField(max_length=100)
    grm_movement = models.CharField(max_length=100)
    grm_lpoc = models.CharField(max_length=100, blank=True, null=True)
    grm_npoc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grmerchant'


class Platforms(models.Model):
    pf_key = models.AutoField(primary_key=True)
    pf_id = models.CharField(max_length=100, unique=True)
    pf_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    pf_type = models.CharField(max_length=100, blank=True, null=True)
    pf_squadron = models.CharField(max_length=100, blank=True, null=True)
    pf_co = models.CharField(max_length=100, blank=True, null=True)
    pf_info = models.CharField(max_length=100, blank=True, null=True)
    pf_rdt = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'platforms'


class Rvcrews(models.Model):
    rvc_key = models.AutoField(primary_key=True)
    rvc_rv_key = models.ForeignKey('Rvessels', models.DO_NOTHING, db_column='rvc_rv_key', related_name='crews')
    rvc_name = models.CharField(max_length=100)
    rvc_id = models.CharField(max_length=100)
    rvc_idtype = models.CharField(max_length=100, blank=True, null=True)
    rvc_idexpdt = models.DateField(blank=True, null=True)
    rvc_nationality = models.CharField(max_length=100, blank=True, null=True)
    rvc_ethnicity = models.CharField(max_length=100, blank=True, null=True)
    rvc_type = models.CharField(max_length=100, blank=True, null=True)
    rvc_cell = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rvcrews'


class Rvessels(models.Model):
    rv_key = models.AutoField(primary_key=True)
    rv_id = models.CharField(max_length=100)
    rv_name = models.CharField(max_length=100)
    rv_regno = models.CharField(max_length=100)
    rv_type = models.CharField(max_length=100)
    rv_flag = models.CharField(max_length=100)
    rv_province = models.CharField(max_length=100, blank=True, null=True)
    rv_length = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rv_breadth = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rv_tonnage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    rv_crew = models.SmallIntegerField(blank=True, null=True)
    rv_pf_id = models.CharField(max_length=100, blank=True, null=True)
    rv_rdt = models.DateTimeField(blank=True, null=True, default=timezone.now)

    class Meta:
        managed = False
        db_table = 'rvessels'

    @property
    def nakwa(self):
        return self.crews.all()

    def owner(self):
        return self.owners.all()


class Rvowners(models.Model):
    rvo_key = models.AutoField(primary_key=True)
    rvo_rv_key = models.ForeignKey(Rvessels, models.DO_NOTHING, db_column='rvo_rv_key', related_name='owners')
    rvo_type = models.CharField(max_length=100)
    rvo_name = models.CharField(max_length=100)
    rvo_id = models.CharField(max_length=100, blank=True, null=True)
    rvo_idtype = models.CharField(max_length=100, blank=True, null=True)
    rvo_idexpdt = models.DateField(blank=True, null=True)
    rvo_nationality = models.CharField(max_length=100, blank=True, null=True)
    rvo_ethnicity = models.CharField(max_length=100, blank=True, null=True)
    rvo_share = models.SmallIntegerField(blank=True, null=True)
    rvo_cell = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rvowners'


class Srcrews(models.Model):
    src_key = models.AutoField(primary_key=True)
    src_sr_key = models.ForeignKey('Sreports', models.DO_NOTHING, db_column='src_sr_key', related_name='sreport_crews')
    src_srv_key = models.IntegerField()
    src_name = models.CharField(max_length=100)
    src_id = models.CharField(max_length=100, blank=True, null=True)
    src_idtype = models.CharField(max_length=100, blank=True, null=True)
    src_idexpdt = models.DateField(blank=True, null=True)
    src_nationality = models.CharField(max_length=100, blank=True, null=True)
    src_ethnicity = models.CharField(max_length=100, blank=True, null=True)
    src_type = models.CharField(max_length=100, blank=True, null=True)
    src_cell = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'srcrews'


class Sreports(models.Model):
    sr_key = models.AutoField(primary_key=True)
    sr_pf_id = models.CharField(max_length=100)
    sr_dtg = models.DateTimeField()
    sr_position = models.TextField()  # This field type is a guess.
    sr_rv_key = models.IntegerField()
    sr_type = models.CharField(max_length=100, blank=True, null=True)
    sr_movement = models.CharField(max_length=100, blank=True, null=True)
    sr_action = models.CharField(max_length=100, blank=True, null=True)
    sr_info = models.CharField(max_length=100, blank=True, null=True)
    sr_rdt = models.DateTimeField(blank=True, null=True, default=timezone.now)
    sr_fuelrem = models.IntegerField()
    sr_patroltype = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sreports'

    @property
    def nakwa(self):
        return self.sreport_crews.filter(src_type='NAKWA')

    @property
    def fishing_trip(self):
        return self.fishing_trip

    @property
    def merchant_trip(self):
        return self.merchant_trip

    @property
    def crew(self):
        return self.sreport_crews.filter(src_type='CREW')

    @property
    def srowner(self):
        return self.sreport_owners.all()

    @property
    def goods(self):
        return self.sreport_goods.all()


class Sreports1(models.Model):
    sr_key = models.OneToOneField(Sreports, models.DO_NOTHING, db_column='sr1_key', primary_key=True, related_name='fishing_trip')
    sr_depjetty = models.CharField(max_length=100, blank=True, null=True)
    sr_depdt = models.DateField(blank=True, null=True)
    sr_pc = models.CharField(max_length=100, blank=True, null=True)
    sr_pcissuedt = models.DateField(blank=True, null=True)
    sr_pcdays = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sreports1'


class Sreports2(models.Model):
    sr_key = models.OneToOneField(Sreports, models.DO_NOTHING, db_column='sr2_key', primary_key=True, related_name='merchant_trip')
    sr2_lpoc = models.CharField(max_length=100, blank=True, null=True)
    sr2_lpocdtg = models.DateField(blank=True, null=True)
    sr2_npoc = models.CharField(max_length=100, blank=True, null=True)
    sr2_npoceta = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sreports2'


class Srgoods(models.Model):
    srg_key = models.AutoField(primary_key=True)
    srg_sr_key = models.ForeignKey(Sreports, models.DO_NOTHING, db_column='srg_sr_key', related_name='sreport_goods')
    srg_item = models.CharField(max_length=100, blank=True, null=True)
    srg_qty = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    srg_denomination = models.CharField(max_length=100, blank=True, null=True)
    srg_category = models.CharField(max_length=100, blank=True, null=True)
    srg_subcategory = models.CharField(max_length=100, blank=True, null=True)
    srg_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    srg_source = models.CharField(max_length=100, blank=True, null=True)
    srg_confiscated = models.BooleanField()
    srg_remarks = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'srgoods'


class Srowners(models.Model):
    sro_key = models.AutoField(primary_key=True)
    sro_sr_key = models.ForeignKey(Sreports, models.DO_NOTHING, db_column='sro_sr_key', related_name='sreport_owners')
    sro_srv_key = models.IntegerField()
    sro_type = models.CharField(max_length=100)
    sro_name = models.CharField(max_length=100)
    sro_id = models.CharField(max_length=100, blank=True, null=True)
    sro_idtype = models.CharField(max_length=100, blank=True, null=True)
    sro_idexpdt = models.DateField(blank=True, null=True)
    sro_nationality = models.CharField(max_length=100, blank=True, null=True)
    sro_ethnicity = models.CharField(max_length=100, blank=True, null=True)
    sro_share = models.SmallIntegerField(blank=True, null=True)
    sro_cell = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'srowners'


