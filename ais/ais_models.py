from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Full_Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    mmsi = models.CharField(max_length=100, blank=True, null=True)  # maritime mobile service identity identifies vessel's transmitter station
    imo = models.CharField(max_length=100, blank=True, null=True)  # international maritime organisation number uniquely identifies vessels
    ship_id = models.CharField(max_length=100, blank=True, null=True)  # id assigned by marine traffic for the subject vessel
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)  # vessel bow position (vessel orientation)
    status = models.CharField(max_length=100, blank=True, null=True)  # navigational status input by vessel's crew (value range from 0-15)
    course = models.FloatField(blank=True, null=True)  # vessel navigation or movement in water
    timestamp = models.DateTimeField(blank=True, null=True)  # time position/event recorded by marine traffic
    dsrc = models.CharField(max_length=100, blank=True, null=True)  # data source: terrestrial or satellite
    utc_seconds = models.FloatField(blank=True, null=True)  # time taken by vessel to transmit information
    ship_name = models.CharField(max_length=100, blank=True, null=True)
    ship_type = models.CharField(max_length=100, blank=True, null=True)
    call_sign = models.CharField(max_length=100, blank=True, null=True)  # uniquely designated identifier for the vessel's transmitter station
    flag = models.CharField(max_length=100, blank=True, null=True)
    length = models.FloatField(blank=True, null=True)  # in meters
    width = models.FloatField(blank=True, null=True)  # in meters
    grt = models.FloatField(blank=True, null=True)  # gross tonnage: internal volume of ship (assess size and capacity of ship)
    dwt = models.FloatField(blank=True, null=True)  # Deadweight (in metric tons): weight a vessel can safely carry (excluding its own)
    draught = models.FloatField(blank=True, null=True)  # critical measurement for determining a ship's immersion in the water
    year_built = models.IntegerField(blank=True, null=True)
    rot = models.FloatField(blank=True, null=True)  # rate of turn indicates how quickly a vessel is changing its direction of movement.
    type_name = models.CharField(max_length=100, blank=True, null=True)
    ais_type_summary = models.CharField(max_length=100, blank=True, null=True)  # Further explanation of the SHIPTYPE ID
    destination = models.CharField(max_length=100, blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)  # Estimated Time of Arrival to Destination
    current_port = models.CharField(max_length=100, blank=True, null=True)
    last_port = models.CharField(max_length=100, blank=True, null=True)
    last_port_time = models.DateTimeField(blank=True, null=True)
    current_port_id = models.CharField(max_length=100, blank=True, null=True)
    current_port_unlocode = models.CharField(max_length=100, blank=True, null=True)
    current_port_country = models.CharField(max_length=100, blank=True, null=True)
    last_port_id = models.CharField(max_length=100, blank=True, null=True)
    last_port_unlocode = models.CharField(max_length=100, blank=True, null=True)
    last_port_country = models.CharField(max_length=100, blank=True, null=True)
    next_port_id = models.CharField(max_length=100, blank=True, null=True)
    next_port_unlocode = models.CharField(max_length=100, blank=True, null=True)
    next_port_name = models.CharField(max_length=100, blank=True, null=True)
    next_port_country = models.CharField(max_length=100, blank=True, null=True)
    eta_calc = models.DateTimeField(blank=True, null=True)
    eta_updated = models.DateTimeField(blank=True, null=True)
    distance_to_go = models.FloatField(blank=True, null=True)
    distance_travelled = models.FloatField(blank=True, null=True)
    awg_speed = models.FloatField(blank=True, null=True)
    max_speed = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fulldata'


class Merchant_Vessel(models.Model):
    mv_key = models.BigAutoField(primary_key=True)
    mv_mmsi = models.CharField(max_length=100, blank=True, null=True)
    mv_imo = models.CharField(max_length=100, blank=True, null=True)
    mv_ship_id = models.CharField(max_length=100, blank=True, null=True)
    mv_ship_name = models.CharField(max_length=100, blank=True, null=True)
    mv_ship_type = models.CharField(max_length=100, blank=True, null=True)
    mv_call_sign = models.CharField(max_length=100, blank=True, null=True)
    mv_flag = models.CharField(max_length=100, blank=True, null=True)
    mv_length = models.FloatField(blank=True, null=True)
    mv_width = models.FloatField(blank=True, null=True)
    mv_grt = models.FloatField(blank=True, null=True)
    mv_dwt = models.FloatField(blank=True, null=True)
    mv_year_built = models.IntegerField(blank=True, null=True)
    mv_type_name = models.CharField(max_length=100, blank=True, null=True)
    mv_ais_type_summary = models.CharField(max_length=100, blank=True, null=True)
    mv_data_source = models.CharField(max_length=50, default="ais")

    class Meta:
        managed = False
        db_table = 'mer_vessel'


class MVDetails(models.Model):
    mvd_key = models.BigAutoField(primary_key=True)
    mvd_mv_key = models.ForeignKey(Merchant_Vessel, models.DO_NOTHING, db_column='mvd_mv_key', related_name='mvessel_details')
    mvd_position = models.TextField(blank=True, null=True)
    mvd_speed = models.FloatField(blank=True, null=True)
    mvd_heading = models.FloatField(blank=True, null=True)
    mvd_status = models.CharField(max_length=100, blank=True, null=True)
    mvd_course = models.FloatField(blank=True, null=True)
    mvd_timestamp = models.DateTimeField(blank=True, null=True)
    mvd_dsrc = models.CharField(max_length=100, blank=True, null=True)
    mvd_utc_seconds = models.FloatField(blank=True, null=True)
    mvd_draught = models.FloatField(blank=True, null=True)
    mvd_rot = models.FloatField(blank=True, null=True)
    mvd_destination = models.CharField(max_length=100, blank=True, null=True)
    mvd_eta = models.DateTimeField(blank=True, null=True)
    mvd_current_port = models.CharField(max_length=100, blank=True, null=True)
    mvd_last_port = models.CharField(max_length=100, blank=True, null=True)
    mvd_last_port_time = models.DateTimeField(blank=True, null=True)
    mvd_current_port_id = models.CharField(max_length=100, blank=True, null=True)
    mvd_current_port_unlocode = models.CharField(max_length=100, blank=True, null=True)
    mvd_current_port_country = models.CharField(max_length=100, blank=True, null=True)
    mvd_last_port_id = models.CharField(max_length=100, blank=True, null=True)
    mvd_last_port_unlocode = models.CharField(max_length=100, blank=True, null=True)
    mvd_last_port_country = models.CharField(max_length=100, blank=True, null=True)
    mvd_next_port_id = models.CharField(max_length=100, blank=True, null=True)
    mvd_next_port_unlocode = models.CharField(max_length=100, blank=True, null=True)
    mvd_next_port_name = models.CharField(max_length=100, blank=True, null=True)
    mvd_next_port_country = models.CharField(max_length=100, blank=True, null=True)
    mvd_eta_calc = models.DateTimeField(blank=True, null=True)
    mvd_eta_updated = models.DateTimeField(blank=True, null=True)
    mvd_distance_to_go = models.FloatField(blank=True, null=True)
    mvd_distance_travelled = models.FloatField(blank=True, null=True)
    mvd_awg_speed = models.FloatField(blank=True, null=True)
    mvd_max_speed = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mv_details'


class Merchant_Trip(models.Model):
    mt_key = models.BigAutoField(primary_key=True)
    mt_mv_key = models.ForeignKey(Merchant_Vessel, models.DO_NOTHING, db_column='mt_mv_key', related_name='trips')
    mt_dsrc = models.CharField(max_length=100, blank=True, null=True)
    mt_destination = models.CharField(max_length=100, blank=True, null=True)
    mt_eta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mer_trip'

    # @property
    # def tripdetails(self):
    #     return self.tripdetails.all()


class Trip_Details(models.Model):
    td_id = models.BigAutoField(primary_key=True)
    td_mt_id = models.ForeignKey(Merchant_Trip, models.DO_NOTHING, db_column='td_mt_id', related_name='tripdetails')
    longitude = models.FloatField()
    latitude = models.FloatField()
    speed = models.FloatField()
    heading = models.FloatField()
    status = models.CharField(max_length=100)
    course = models.FloatField()
    timestamp = models.DateTimeField()
    utc_seconds = models.FloatField()
    draught = models.FloatField()
    rot = models.FloatField()
    current_port = models.CharField(max_length=100)
    last_port = models.CharField(max_length=100)
    last_port_time = models.DateTimeField()
    current_port_id = models.CharField(max_length=100)
    current_port_unlocode = models.CharField(max_length=100)
    current_port_country = models.CharField(max_length=100)
    last_port_id = models.CharField(max_length=100)
    last_port_unlocode = models.CharField(max_length=100)
    last_port_country = models.CharField(max_length=100)
    next_port_id = models.CharField(max_length=100)
    next_port_unlocode = models.CharField(max_length=100)
    next_port_name = models.CharField(max_length=100)
    next_port_country = models.CharField(max_length=100)
    eta_calc = models.DateTimeField()
    eta_updated = models.DateTimeField()
    distance_to_go = models.FloatField()
    distance_travelled = models.FloatField()
    awg_speed = models.FloatField()
    max_speed = models.FloatField()

    class Meta:
        managed = False
        db_table = 'mer_trip_detail'


class Location_Details(models.Model):
    ld_id = models.BigAutoField(primary_key=True)
    ld_mt_id = models.ForeignKey(Merchant_Trip, models.DO_NOTHING, db_column='ld_mt_id', related_name='locationdetails')
    longitude = models.FloatField()
    latitude = models.FloatField()
    heading = models.FloatField()
    course = models.FloatField()
    timestamp = models.DateTimeField()
    rot = models.FloatField()
    current_port = models.CharField(max_length=100)
    last_port = models.CharField(max_length=100)
    last_port_time = models.DateTimeField()
    current_port_id = models.CharField(max_length=100)
    current_port_unlocode = models.CharField(max_length=100)
    current_port_country = models.CharField(max_length=100)
    last_port_id = models.CharField(max_length=100)
    last_port_unlocode = models.CharField(max_length=100)
    last_port_country = models.CharField(max_length=100)
    next_port_id = models.CharField(max_length=100)
    next_port_unlocode = models.CharField(max_length=100)
    next_port_name = models.CharField(max_length=100)
    next_port_country = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'location_detail'


class Event_Details(models.Model):
    ed_id = models.BigAutoField(primary_key=True)
    ed_mt_id = models.ForeignKey(Merchant_Trip, models.DO_NOTHING, db_column='ed_mt_id', related_name='eventdetails')
    speed = models.FloatField()
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    draught = models.FloatField()
    eta_calc = models.DateTimeField()
    eta_updated = models.DateTimeField()
    distance_to_go = models.FloatField()
    distance_travelled = models.FloatField()
    awg_speed = models.FloatField()
    max_speed = models.FloatField()
    event = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event_detail'


class MerSreports(models.Model):
    msr_key = models.AutoField(primary_key=True)
    msr_pf_id = models.CharField(max_length=100)
    msr_dtg = models.DateTimeField(blank=True, null=True)
    msr_position = models.TextField(blank=True, null=True)
    msr_mv_key = models.IntegerField()
    msr_type = models.CharField(max_length=100, blank=True, null=True)
    msr_movement = models.CharField(max_length=100, blank=True, null=True)
    msr_action = models.CharField(max_length=100, blank=True, null=True)
    msr_info = models.CharField(max_length=100, blank=True, null=True)
    msr_rdt = models.DateTimeField(default=timezone.now)
    msr_fuelrem = models.IntegerField(blank=True, null=True)
    msr_patroltype = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mersreports'

    @property
    def merchant_trip(self):
        return self.merchant_trip

    @property
    def goods(self):
        return self.sreport_goods.all()


class MerSrgoods(models.Model):
    msrg_key = models.AutoField(primary_key=True)
    msrg_msr_key = models.ForeignKey(MerSreports, models.DO_NOTHING, db_column='msrg_msr_key', related_name='sreport_goods')
    msrg_item = models.CharField(max_length=100, blank=True, null=True)
    msrg_qty = models.DecimalField(max_digits=100, decimal_places=10, blank=True, null=True)
    msrg_denomination = models.CharField(max_length=100, blank=True, null=True)
    msrg_category = models.CharField(max_length=100, blank=True, null=True)
    msrg_subcategory = models.CharField(max_length=100, blank=True, null=True)
    msrg_value = models.DecimalField(max_digits=100, decimal_places=10, blank=True, null=True)
    msrg_source = models.CharField(max_length=100, blank=True, null=True)
    msrg_confiscated = models.BooleanField(blank=True, null=True)
    msrg_remarks = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mersrgoods'


class MerSreports2(models.Model):
    msr_key = models.OneToOneField(MerSreports, models.DO_NOTHING, db_column='msr2_key', primary_key=True,
                                   related_name='merchant_trip')
    msr2_lpoc = models.CharField(max_length=100, blank=True, null=True)
    msr2_lpocdtg = models.DateField(blank=True, null=True)
    msr2_npoc = models.CharField(max_length=100, blank=True, null=True)
    msr2_npoceta = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mersreports2'


class LostReport(models.Model):
    lr_key = models.BigAutoField(primary_key=True)
    lr_mv_key = models.ForeignKey(Merchant_Vessel, on_delete=models.CASCADE, db_column='lr_mv_key')
    lr_coi_number = models.CharField(max_length=100, blank=True, null=True)
    lr_subscriber_code = models.CharField(max_length=100, blank=True, null=True)
    lr_pr_number = models.CharField(max_length=100, blank=True, null=True)
    lr_action_addresses_codes = models.CharField(max_length=100, blank=True, null=True)
    lr_reporting_date = models.DateTimeField(blank=True, null=True)
    lr_remarks = models.TextField(blank=True, null=True)
    lr_position = models.TextField(blank=True, null=True)
    lr_created_on = models.DateTimeField(blank=True, null=True)
    lr_created_by = models.CharField(max_length=100, blank=True, null=True)
    lr_track_status = models.CharField(max_length=100, blank=True, null=True)
    lr_total_crew = models.IntegerField(blank=True, null=True)
    lr_rdt = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'lost_report'


class PNSCShipData(models.Model):
    ps_key = models.BigAutoField(primary_key=True)
    ps_mv_key = models.ForeignKey(Merchant_Vessel, on_delete=models.CASCADE, db_column='ps_mv_key')
    ps_country = models.CharField(max_length=100, blank=True, null=True)
    ps_status_symbol = models.CharField(max_length=100, blank=True, null=True)
    ps_status_symbol_remarks = models.CharField(max_length=100, blank=True, null=True)
    ps_status_symbol_assigned_time = models.DateTimeField(blank=True, null=True)
    ps_track_number = models.IntegerField(blank=True, null=True)
    ps_position = models.TextField(blank=True, null=True)
    ps_speed = models.FloatField(blank=True, null=True)
    ps_course = models.FloatField(blank=True, null=True)
    ps_timestamp = models.DateTimeField(blank=True, null=True)
    ps_lastport = models.CharField(max_length=100, blank=True, null=True)
    ps_next_port = models.CharField(max_length=100, blank=True, null=True)
    ps_track_type = models.CharField(max_length=100, blank=True, null=True)
    ps_track_label = models.CharField(max_length=100, blank=True, null=True)
    ps_rdt = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'pnsc_ship_data'


class SituationalReport(models.Model):
    sit_key = models.BigAutoField(primary_key=True)
    sit_mv_key = models.ForeignKey(Merchant_Vessel, on_delete=models.CASCADE, db_column='sit_mv_key')
    sit_dtg = models.DateTimeField(blank=True, null=True)
    sit_mmsi = models.CharField(max_length=100, blank=True, null=True)
    sit_position = models.TextField(blank=True, null=True)
    sit_lpoc = models.CharField(max_length=100, blank=True, null=True)
    sit_last_port_country = models.CharField(max_length=100, blank=True, null=True)
    sit_npoc = models.CharField(max_length=100, blank=True, null=True)
    sit_next_port_country = models.CharField(max_length=100, blank=True, null=True)
    sit_course = models.FloatField(blank=True, null=True)
    sit_speed = models.FloatField(blank=True, null=True)
    sit_source = models.CharField(max_length=100, blank=True, null=True)
    sit_rdt = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'situational_report'


class COSPASBeacon(models.Model):
    beacon_key = models.BigAutoField(primary_key=True)
    bcnid15 = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=300, blank=True, null=True)
    cstac_number = models.CharField(max_length=300, blank=True, null=True)
    beacon_country_code = models.CharField(max_length=300, blank=True, null=True)
    beacon_reg_type = models.BigIntegerField(blank=True, null=True)
    beacon_type = models.CharField(max_length=300, blank=True, null=True)
    beacon_activation_method = models.CharField(max_length=300, blank=True, null=True)
    beacon_manufacturer = models.CharField(max_length=300, blank=True, null=True)
    beacon_model = models.CharField(max_length=300, blank=True, null=True)
    beacon_homing_device = models.CharField(max_length=300, blank=True, null=True)
    additional_beacon_data = models.CharField(max_length=300, blank=True, null=True)
    owner_name = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=300, blank=True, null=True)
    mail_code = models.BigIntegerField(blank=True, null=True)
    mail_country = models.CharField(max_length=300, blank=True, null=True)
    email_address = models.CharField(max_length=300, blank=True, null=True)
    phone1_num = models.CharField(max_length=300, blank=True, null=True)
    phone1_type = models.CharField(max_length=300, blank=True, null=True)
    phone2_num = models.CharField(max_length=300, blank=True, null=True)
    phone2_type = models.CharField(max_length=300, blank=True, null=True)
    phone3_num = models.CharField(max_length=300, blank=True, null=True)
    phone3_type = models.CharField(max_length=300, blank=True, null=True)
    phone4_num = models.CharField(max_length=300, blank=True, null=True)
    phone4_type = models.CharField(max_length=300, blank=True, null=True)
    vehicle_type = models.CharField(max_length=300, blank=True, null=True)
    usage_more_info = models.CharField(max_length=300, blank=True, null=True)
    vehicle_name = models.CharField(max_length=300, blank=True, null=True)
    vehicle_manufacturer = models.CharField(max_length=300, blank=True, null=True)
    vehicle_model = models.CharField(max_length=300, blank=True, null=True)
    call_sign = models.CharField(max_length=300, blank=True, null=True)
    vehicle_registration_number = models.CharField(max_length=300, blank=True, null=True)
    color = models.CharField(max_length=300, blank=True, null=True)
    length = models.CharField(max_length=300, blank=True, null=True)
    mmsi = models.BigIntegerField(blank=True, null=True)
    people_capacity = models.CharField(max_length=300, blank=True, null=True)
    phone_inmarsat = models.CharField(max_length=300, blank=True, null=True)
    radio_equipment = models.CharField(max_length=300, blank=True, null=True)
    primary_contact_name = models.CharField(max_length=300, blank=True, null=True)
    primary_contact_address_line1 = models.CharField(max_length=300, blank=True, null=True)
    primary_contact_address_line2 = models.CharField(max_length=300, blank=True, null=True)
    primary_phone1_num = models.CharField(max_length=300, blank=True, null=True)
    primary_phone1_type = models.CharField(max_length=300, blank=True, null=True)
    primary_phone2_num = models.CharField(max_length=300, blank=True, null=True)
    primary_phone2_type = models.CharField(max_length=300, blank=True, null=True)
    primary_phone3_num = models.CharField(max_length=300, blank=True, null=True)
    primary_phone3_type = models.CharField(max_length=100, blank=True, null=True)
    primary_phone4_num = models.CharField(max_length=100, blank=True, null=True)
    primary_phone4_type = models.CharField(max_length=100, blank=True, null=True)
    alternate_contact_name = models.CharField(max_length=100, blank=True, null=True)
    alternate_contact_address_line1 = models.CharField(max_length=100, blank=True, null=True)
    alternate_contact_address_line2 = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone1_num = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone1_type = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone2_num = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone2_type = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone3_num = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone3_type = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone4_num = models.CharField(max_length=100, blank=True, null=True)
    alternate_phone4_type = models.CharField(max_length=100, blank=True, null=True)
    initial_date = models.CharField(max_length=100, blank=True, null=True)
    last_edit_date = models.CharField(max_length=100, blank=True, null=True)
    additional_data = models.CharField(max_length=100, blank=True, null=True)
    operator_id = models.CharField(max_length=100, blank=True, null=True)
    operator_language = models.CharField(max_length=100, blank=True, null=True)
    special_status_date = models.CharField(max_length=100, blank=True, null=True)
    special_status = models.CharField(max_length=100, blank=True, null=True)
    special_status_info = models.CharField(max_length=100, blank=True, null=True)
    previous_special_status = models.CharField(max_length=100, blank=True, null=True)
    survival_type1_num = models.CharField(max_length=100, blank=True, null=True)
    survival_type2_num = models.CharField(max_length=100, blank=True, null=True)
    survival_type1_desc = models.CharField(max_length=100, blank=True, null=True)
    survival_type2_desc = models.CharField(max_length=100, blank=True, null=True)
    vehicle_cellular_num = models.CharField(max_length=100, blank=True, null=True)
    block_id = models.CharField(max_length=100, blank=True, null=True)
    challenge_question = models.CharField(max_length=100, blank=True, null=True)
    challenge_response = models.CharField(max_length=100, blank=True, null=True)
    aircraft_24bitaddress = models.CharField(max_length=100, blank=True, null=True)
    aircraft_operating_agency = models.CharField(max_length=100, blank=True, null=True)
    vehicle_nationality = models.CharField(max_length=100, blank=True, null=True)
    svdr_present = models.CharField(max_length=100, blank=True, null=True)
    carrier_key = models.CharField(max_length=100, blank=True, null=True)
    call_sign_decoded = models.CharField(max_length=100, blank=True, null=True)
    mmsi_decoded = models.BigIntegerField(blank=True, null=True)
    aircraft_24bitaddress_decoded = models.CharField(max_length=100, blank=True, null=True)
    user_confirmation_required = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cospos_beacon'


class COSPASData(models.Model):
    cospas_key = models.BigAutoField(primary_key=True)
    occurrence_type = models.CharField(max_length=100, blank=True, null=True)
    distress_conf = models.CharField(max_length=100, blank=True, null=True)
    beacon_operating_mode = models.CharField(max_length=100, blank=True, null=True)
    beacon_reg_no = models.CharField(max_length=100, blank=True, null=True)
    msg_ref = models.CharField(max_length=100, blank=True, null=True)
    detected_at = models.DateTimeField(blank=True, null=True)
    det_satellite = models.CharField(max_length=100, blank=True, null=True)
    det_freq_typeA = models.CharField(max_length=100, blank=True, null=True)
    det_freq_typeB = models.CharField(max_length=100, blank=True, null=True)
    det_freq_typeC = models.CharField(max_length=100, blank=True, null=True)
    user_class_std_location = models.CharField(max_length=100, blank=True, null=True)
    cospos_beacon_key = models.ForeignKey(COSPASBeacon, on_delete=models.CASCADE, db_column='cospos_beacon_key', blank=True, null=True)
    emergency_code = models.CharField(max_length=100, blank=True, null=True)
    pos_confirmed_lat = models.FloatField(blank=True, null=True)
    pos_confirmed_long = models.FloatField(blank=True, null=True)
    pos_dopplerA = models.CharField(max_length=100, blank=True, null=True)
    pos_dopplerB = models.CharField(max_length=100, blank=True, null=True)
    pos_doa_lat = models.FloatField(blank=True, null=True)
    pos_doa_long = models.FloatField(blank=True, null=True)
    pos_expected_acc = models.FloatField(blank=True, null=True)
    pos_altitude = models.FloatField(blank=True, null=True)
    pos_encoded_lat = models.FloatField(blank=True, null=True)
    pos_encoded_long = models.FloatField(blank=True, null=True)
    pos_updated_time = models.DateTimeField(blank=True, null=True)
    pos_provided_by = models.CharField(max_length=100, blank=True, null=True)
    nextpass_confirmed = models.DateTimeField(blank=True, null=True)
    nextpass_doppA = models.DateTimeField(blank=True, null=True)
    nextpass_doppB = models.DateTimeField(blank=True, null=True)
    nextpass_doa = models.DateTimeField(blank=True, null=True)
    nextpass_encoded = models.DateTimeField(blank=True, null=True)
    hex_id = models.CharField(max_length=100, blank=True, null=True)
    activation_type = models.CharField(max_length=100, blank=True, null=True)
    oei_mid = models.CharField(max_length=100, blank=True, null=True)
    oei_loc_protocol_type = models.CharField(max_length=100, blank=True, null=True)
    oei_pos_uncertainty = models.CharField(max_length=100, blank=True, null=True)
    oei_lat = models.FloatField(blank=True, null=True)
    oei_long = models.FloatField(blank=True, null=True)
    oper_info_imo = models.CharField(max_length=100, blank=True, null=True)
    oper_info_vessel_type = models.CharField(max_length=100, blank=True, null=True)
    oper_info_lpoc = models.CharField(max_length=100, blank=True, null=True)
    oper_info_npoc = models.CharField(max_length=100, blank=True, null=True)
    oper_ship_owner = models.CharField(max_length=100, blank=True, null=True)
    oper_sat_alert_time = models.DateTimeField(blank=True, null=True)
    temp_from = models.DateTimeField(blank=True, null=True)
    temp_to = models.DateTimeField(blank=True, null=True)
    temp_inc_reporting_time = models.DateTimeField(blank=True, null=True)
    temp_inc_details = models.CharField(max_length=100, blank=True, null=True)
    temp_actions_list = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cospas_data'


class MissionReport(models.Model):
    mr_key = models.BigAutoField(primary_key=True)
    mr_pf_id = models.CharField(max_length=100, blank=True, null=True)
    mr_dtg = models.DateTimeField(blank=True, null=True)
    mr_rdt = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'misrep'

    @property
    def mrdetails(self):
        return self.mrdetails.all()


class MRDetails(models.Model):
    mrd_key = models.BigAutoField(primary_key=True)
    mrd_mr_key = models.ForeignKey(MissionReport, on_delete=models.CASCADE, db_column='mrd_mr_key', related_name='mrdetails')
    mrd_mv_key = models.ForeignKey(Merchant_Vessel, on_delete=models.CASCADE, db_column='mrd_mv_key')
    mrd_mmsi = models.CharField(max_length=100, blank=True, null=True)
    mrd_vessel_type = models.CharField(max_length=100, blank=True, null=True)
    mrd_vessel_name = models.CharField(max_length=100, blank=True, null=True)
    mrd_position = models.TextField(blank=True, null=True)
    mrd_course = models.FloatField(blank=True, null=True)
    mrd_speed = models.FloatField(blank=True, null=True)
    mrd_npoc = models.CharField(max_length=100, blank=True, null=True)
    mrd_lpoc = models.CharField(max_length=100, blank=True, null=True)
    mrd_act_desc = models.CharField(max_length=500, blank=True, null=True)
    mrd_dtg = models.DateTimeField(blank=True, null=True)
    mrd_ais_status = models.CharField(max_length=100, blank=True, null=True)
    mrd_call_details = models.CharField(max_length=100, blank=True, null=True)
    mrd_response = models.CharField(max_length=100, blank=True, null=True)
    mrd_remarks = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'misrep_details'


class ShipBreaking(models.Model):
    sb_key = models.BigAutoField(primary_key=True)
    sb_mv_key = models.ForeignKey(Merchant_Vessel, on_delete=models.CASCADE, db_column='sb_mv_key')
    sb_dtg = models.DateTimeField(blank=True, null=True)
    sb_flag_reg_cert = models.BooleanField(blank=True, null=True)
    sb_crew = models.IntegerField(blank=True, null=True)
    sb_imo_verified = models.BooleanField(blank=True, null=True)
    sb_agreement_memo = models.BooleanField(blank=True, null=True)
    sb_credit_let = models.BooleanField(blank=True, null=True)
    sb_lpoc = models.CharField(max_length=100, blank=True, null=True)
    sb_mast_name = models.CharField(max_length=100, blank=True, null=True)
    sb_mast_nationality = models.CharField(max_length=100, blank=True, null=True)
    sb_buyer_comp_name = models.CharField(max_length=100, blank=True, null=True)
    sb_buyer_comp_num = models.CharField(max_length=100, blank=True, null=True)
    sb_owner_name = models.CharField(max_length=100, blank=True, null=True)
    sb_owner_num = models.CharField(max_length=100, blank=True, null=True)
    sb_locshipping_comp_name = models.CharField(max_length=100, blank=True, null=True)
    sb_locshipping_agent_name = models.CharField(max_length=100, blank=True, null=True)
    sb_locshipping_agent_num = models.CharField(max_length=100, blank=True, null=True)
    sb_sec_team = models.BooleanField(blank=True, null=True)
    sb_haz_material = models.BooleanField(blank=True, null=True)
    sb_gas_free_cert = models.BooleanField(blank=True, null=True)
    sb_waste_free_cert = models.BooleanField(blank=True, null=True)
    sb_import_gen_manifest = models.BooleanField(blank=True, null=True)
    sb_comm_equip_list = ArrayField(models.CharField(max_length=200), blank=True)
    sb_goods_dec_doc = models.BooleanField(blank=True, null=True)
    sb_del_cert = models.BooleanField(blank=True, null=True)
    sb_iso_cert = models.BooleanField(blank=True, null=True)
    sb_ex_name = models.CharField(max_length=100, blank=True, null=True)
    sb_emb_name = models.CharField(max_length=100, blank=True, null=True)
    sb_rdt = models.DateTimeField(default=timezone.now)

    class Meta:
        # managed = False
        db_table = 'ship_breaking'

    @property
    def sb_crews(self):
        return self.sb_crews


class Sbcrews(models.Model):
    sbc_key = models.BigAutoField(primary_key=True)
    sbc_sb_key = models.ForeignKey(ShipBreaking, on_delete=models.CASCADE, db_column='sbc_sb_key', related_name='sb_crews')
    sbc_name = models.CharField(max_length=100, blank=True, null=True)
    sbc_nationality = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'sb_crew'
