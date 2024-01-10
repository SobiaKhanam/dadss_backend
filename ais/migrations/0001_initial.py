# Generated by Django 4.1.2 on 2023-12-14 08:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='COSPASBeacon',
            fields=[
                ('beacon_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('bcnid15', models.CharField(blank=True, max_length=300, null=True)),
                ('password', models.CharField(blank=True, max_length=300, null=True)),
                ('cstac_number', models.CharField(blank=True, max_length=300, null=True)),
                ('beacon_country_code', models.CharField(blank=True, max_length=300, null=True)),
                ('beacon_reg_type', models.BigIntegerField(blank=True, null=True)),
                ('beacon_type', models.CharField(blank=True, max_length=300, null=True)),
                ('beacon_activation_method', models.CharField(blank=True, max_length=300, null=True)),
                ('beacon_manufacturer', models.CharField(blank=True, max_length=300, null=True)),
                ('beacon_model', models.CharField(blank=True, max_length=300, null=True)),
                ('beacon_homing_device', models.CharField(blank=True, max_length=300, null=True)),
                ('additional_beacon_data', models.CharField(blank=True, max_length=300, null=True)),
                ('owner_name', models.CharField(blank=True, max_length=300, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('city', models.CharField(blank=True, max_length=300, null=True)),
                ('province', models.CharField(blank=True, max_length=300, null=True)),
                ('mail_code', models.BigIntegerField(blank=True, null=True)),
                ('mail_country', models.CharField(blank=True, max_length=300, null=True)),
                ('email_address', models.CharField(blank=True, max_length=300, null=True)),
                ('phone1_num', models.CharField(blank=True, max_length=300, null=True)),
                ('phone1_type', models.CharField(blank=True, max_length=300, null=True)),
                ('phone2_num', models.CharField(blank=True, max_length=300, null=True)),
                ('phone2_type', models.CharField(blank=True, max_length=300, null=True)),
                ('phone3_num', models.CharField(blank=True, max_length=300, null=True)),
                ('phone3_type', models.CharField(blank=True, max_length=300, null=True)),
                ('phone4_num', models.CharField(blank=True, max_length=300, null=True)),
                ('phone4_type', models.CharField(blank=True, max_length=300, null=True)),
                ('vehicle_type', models.CharField(blank=True, max_length=300, null=True)),
                ('usage_more_info', models.CharField(blank=True, max_length=300, null=True)),
                ('vehicle_name', models.CharField(blank=True, max_length=300, null=True)),
                ('vehicle_manufacturer', models.CharField(blank=True, max_length=300, null=True)),
                ('vehicle_model', models.CharField(blank=True, max_length=300, null=True)),
                ('call_sign', models.CharField(blank=True, max_length=300, null=True)),
                ('vehicle_registration_number', models.CharField(blank=True, max_length=300, null=True)),
                ('color', models.CharField(blank=True, max_length=300, null=True)),
                ('length', models.CharField(blank=True, max_length=300, null=True)),
                ('mmsi', models.BigIntegerField(blank=True, null=True)),
                ('people_capacity', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_inmarsat', models.CharField(blank=True, max_length=300, null=True)),
                ('radio_equipment', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_contact_name', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_contact_address_line1', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_contact_address_line2', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_phone1_num', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_phone1_type', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_phone2_num', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_phone2_type', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_phone3_num', models.CharField(blank=True, max_length=300, null=True)),
                ('primary_phone3_type', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_phone4_num', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_phone4_type', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_contact_address_line1', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_contact_address_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone1_num', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone1_type', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone2_num', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone2_type', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone3_num', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone3_type', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone4_num', models.CharField(blank=True, max_length=100, null=True)),
                ('alternate_phone4_type', models.CharField(blank=True, max_length=100, null=True)),
                ('initial_date', models.CharField(blank=True, max_length=100, null=True)),
                ('last_edit_date', models.CharField(blank=True, max_length=100, null=True)),
                ('additional_data', models.CharField(blank=True, max_length=100, null=True)),
                ('operator_id', models.CharField(blank=True, max_length=100, null=True)),
                ('operator_language', models.CharField(blank=True, max_length=100, null=True)),
                ('special_status_date', models.CharField(blank=True, max_length=100, null=True)),
                ('special_status', models.CharField(blank=True, max_length=100, null=True)),
                ('special_status_info', models.CharField(blank=True, max_length=100, null=True)),
                ('previous_special_status', models.CharField(blank=True, max_length=100, null=True)),
                ('survival_type1_num', models.CharField(blank=True, max_length=100, null=True)),
                ('survival_type2_num', models.CharField(blank=True, max_length=100, null=True)),
                ('survival_type1_desc', models.CharField(blank=True, max_length=100, null=True)),
                ('survival_type2_desc', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_cellular_num', models.CharField(blank=True, max_length=100, null=True)),
                ('block_id', models.CharField(blank=True, max_length=100, null=True)),
                ('challenge_question', models.CharField(blank=True, max_length=100, null=True)),
                ('challenge_response', models.CharField(blank=True, max_length=100, null=True)),
                ('aircraft_24bitaddress', models.CharField(blank=True, max_length=100, null=True)),
                ('aircraft_operating_agency', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('svdr_present', models.CharField(blank=True, max_length=100, null=True)),
                ('carrier_key', models.CharField(blank=True, max_length=100, null=True)),
                ('call_sign_decoded', models.CharField(blank=True, max_length=100, null=True)),
                ('mmsi_decoded', models.BigIntegerField(blank=True, null=True)),
                ('aircraft_24bitaddress_decoded', models.CharField(blank=True, max_length=100, null=True)),
                ('user_confirmation_required', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'cospos_beacon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='COSPASData',
            fields=[
                ('cospas_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('occurrence_type', models.CharField(blank=True, max_length=100, null=True)),
                ('distress_conf', models.CharField(blank=True, max_length=100, null=True)),
                ('beacon_operating_mode', models.CharField(blank=True, max_length=100, null=True)),
                ('beacon_reg_no', models.CharField(blank=True, max_length=100, null=True)),
                ('msg_ref', models.CharField(blank=True, max_length=100, null=True)),
                ('detected_at', models.DateTimeField(blank=True, null=True)),
                ('det_satellite', models.CharField(blank=True, max_length=100, null=True)),
                ('det_freq_typeA', models.CharField(blank=True, max_length=100, null=True)),
                ('det_freq_typeB', models.CharField(blank=True, max_length=100, null=True)),
                ('det_freq_typeC', models.CharField(blank=True, max_length=100, null=True)),
                ('user_class_std_location', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_code', models.CharField(blank=True, max_length=100, null=True)),
                ('pos_confirmed_lat', models.FloatField(blank=True, null=True)),
                ('pos_confirmed_long', models.FloatField(blank=True, null=True)),
                ('pos_dopplerA', models.CharField(blank=True, max_length=100, null=True)),
                ('pos_dopplerB', models.CharField(blank=True, max_length=100, null=True)),
                ('pos_doa_lat', models.FloatField(blank=True, null=True)),
                ('pos_doa_long', models.FloatField(blank=True, null=True)),
                ('pos_expected_acc', models.FloatField(blank=True, null=True)),
                ('pos_altitude', models.FloatField(blank=True, null=True)),
                ('pos_encoded_lat', models.FloatField(blank=True, null=True)),
                ('pos_encoded_long', models.FloatField(blank=True, null=True)),
                ('pos_updated_time', models.DateTimeField(blank=True, null=True)),
                ('pos_provided_by', models.CharField(blank=True, max_length=100, null=True)),
                ('nextpass_confirmed', models.DateTimeField(blank=True, null=True)),
                ('nextpass_doppA', models.DateTimeField(blank=True, null=True)),
                ('nextpass_doppB', models.DateTimeField(blank=True, null=True)),
                ('nextpass_doa', models.DateTimeField(blank=True, null=True)),
                ('nextpass_encoded', models.DateTimeField(blank=True, null=True)),
                ('hex_id', models.CharField(blank=True, max_length=100, null=True)),
                ('activation_type', models.CharField(blank=True, max_length=100, null=True)),
                ('oei_mid', models.CharField(blank=True, max_length=100, null=True)),
                ('oei_loc_protocol_type', models.CharField(blank=True, max_length=100, null=True)),
                ('oei_pos_uncertainty', models.CharField(blank=True, max_length=100, null=True)),
                ('oei_lat', models.FloatField(blank=True, null=True)),
                ('oei_long', models.FloatField(blank=True, null=True)),
                ('oper_info_imo', models.CharField(blank=True, max_length=100, null=True)),
                ('oper_info_vessel_type', models.CharField(blank=True, max_length=100, null=True)),
                ('oper_info_lpoc', models.CharField(blank=True, max_length=100, null=True)),
                ('oper_info_npoc', models.CharField(blank=True, max_length=100, null=True)),
                ('oper_ship_owner', models.CharField(blank=True, max_length=100, null=True)),
                ('oper_sat_alert_time', models.DateTimeField(blank=True, null=True)),
                ('temp_from', models.DateTimeField(blank=True, null=True)),
                ('temp_to', models.DateTimeField(blank=True, null=True)),
                ('temp_inc_reporting_time', models.DateTimeField(blank=True, null=True)),
                ('temp_inc_details', models.CharField(blank=True, max_length=100, null=True)),
                ('temp_actions_list', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'cospas_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Event_Details',
            fields=[
                ('ed_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('speed', models.FloatField()),
                ('status', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('draught', models.FloatField()),
                ('eta_calc', models.DateTimeField()),
                ('eta_updated', models.DateTimeField()),
                ('distance_to_go', models.FloatField()),
                ('distance_travelled', models.FloatField()),
                ('awg_speed', models.FloatField()),
                ('max_speed', models.FloatField()),
                ('event', models.IntegerField()),
            ],
            options={
                'db_table': 'event_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Full_Data',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mmsi', models.CharField(max_length=100)),
                ('imo', models.CharField(max_length=100)),
                ('ship_id', models.CharField(max_length=100)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('speed', models.FloatField()),
                ('heading', models.FloatField()),
                ('status', models.CharField(max_length=100)),
                ('course', models.FloatField()),
                ('timestamp', models.DateTimeField()),
                ('dsrc', models.CharField(max_length=100)),
                ('utc_seconds', models.FloatField()),
                ('ship_name', models.CharField(max_length=100)),
                ('ship_type', models.CharField(max_length=100)),
                ('call_sign', models.CharField(max_length=100)),
                ('flag', models.CharField(max_length=100)),
                ('length', models.FloatField()),
                ('width', models.FloatField()),
                ('grt', models.FloatField()),
                ('dwt', models.FloatField()),
                ('draught', models.FloatField()),
                ('year_built', models.IntegerField()),
                ('rot', models.FloatField()),
                ('type_name', models.CharField(max_length=100)),
                ('ais_type_summary', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('eta', models.DateTimeField()),
                ('current_port', models.CharField(max_length=100)),
                ('last_port', models.CharField(max_length=100)),
                ('last_port_time', models.DateTimeField()),
                ('current_port_id', models.CharField(max_length=100)),
                ('current_port_unlocode', models.CharField(max_length=100)),
                ('current_port_country', models.CharField(max_length=100)),
                ('last_port_id', models.CharField(max_length=100)),
                ('last_port_unlocode', models.CharField(max_length=100)),
                ('last_port_country', models.CharField(max_length=100)),
                ('next_port_id', models.CharField(max_length=100)),
                ('next_port_unlocode', models.CharField(max_length=100)),
                ('next_port_name', models.CharField(max_length=100)),
                ('next_port_country', models.CharField(max_length=100)),
                ('eta_calc', models.DateTimeField()),
                ('eta_updated', models.DateTimeField()),
                ('distance_to_go', models.FloatField()),
                ('distance_travelled', models.FloatField()),
                ('awg_speed', models.FloatField()),
                ('max_speed', models.FloatField()),
            ],
            options={
                'db_table': 'fulldata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Location_Details',
            fields=[
                ('ld_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('heading', models.FloatField()),
                ('course', models.FloatField()),
                ('timestamp', models.DateTimeField()),
                ('rot', models.FloatField()),
                ('current_port', models.CharField(max_length=100)),
                ('last_port', models.CharField(max_length=100)),
                ('last_port_time', models.DateTimeField()),
                ('current_port_id', models.CharField(max_length=100)),
                ('current_port_unlocode', models.CharField(max_length=100)),
                ('current_port_country', models.CharField(max_length=100)),
                ('last_port_id', models.CharField(max_length=100)),
                ('last_port_unlocode', models.CharField(max_length=100)),
                ('last_port_country', models.CharField(max_length=100)),
                ('next_port_id', models.CharField(max_length=100)),
                ('next_port_unlocode', models.CharField(max_length=100)),
                ('next_port_name', models.CharField(max_length=100)),
                ('next_port_country', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'location_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LostReport',
            fields=[
                ('lr_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('lr_coi_number', models.CharField(blank=True, max_length=100, null=True)),
                ('lr_subscriber_code', models.CharField(blank=True, max_length=100, null=True)),
                ('lr_pr_number', models.CharField(blank=True, max_length=100, null=True)),
                ('lr_action_addresses_codes', models.CharField(blank=True, max_length=100, null=True)),
                ('lr_reporting_date', models.DateTimeField(blank=True, null=True)),
                ('lr_remarks', models.TextField(blank=True, null=True)),
                ('lr_position', models.TextField(blank=True, null=True)),
                ('lr_created_on', models.DateTimeField(blank=True, null=True)),
                ('lr_created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('lr_track_status', models.CharField(blank=True, max_length=100, null=True)),
                ('lr_total_crew', models.IntegerField(blank=True, null=True)),
                ('lr_rdt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'lost_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Merchant_Trip',
            fields=[
                ('mt_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dsrc', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('eta', models.DateTimeField()),
            ],
            options={
                'db_table': 'mer_trip',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Merchant_Vessel',
            fields=[
                ('mv_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('mv_mmsi', models.CharField(max_length=100)),
                ('mv_imo', models.CharField(max_length=100)),
                ('mv_ship_id', models.CharField(max_length=100)),
                ('mv_ship_name', models.CharField(max_length=100)),
                ('mv_ship_type', models.CharField(blank=True, max_length=100, null=True)),
                ('mv_call_sign', models.CharField(blank=True, max_length=100, null=True)),
                ('mv_flag', models.CharField(max_length=100)),
                ('mv_length', models.FloatField(blank=True, null=True)),
                ('mv_width', models.FloatField(blank=True, null=True)),
                ('mv_grt', models.FloatField(blank=True, null=True)),
                ('mv_dwt', models.FloatField(blank=True, null=True)),
                ('mv_year_built', models.IntegerField(blank=True, null=True)),
                ('mv_type_name', models.CharField(max_length=100)),
                ('mv_ais_type_summary', models.CharField(max_length=100)),
                ('mv_data_source', models.CharField(default='ais', max_length=50)),
            ],
            options={
                'db_table': 'mer_vessel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MerSreports',
            fields=[
                ('msr_key', models.AutoField(primary_key=True, serialize=False)),
                ('msr_pf_id', models.CharField(max_length=100)),
                ('msr_dtg', models.DateTimeField()),
                ('msr_position', models.TextField()),
                ('msr_mv_key', models.IntegerField()),
                ('msr_type', models.CharField(blank=True, max_length=100, null=True)),
                ('msr_movement', models.CharField(blank=True, max_length=100, null=True)),
                ('msr_action', models.CharField(blank=True, max_length=100, null=True)),
                ('msr_info', models.CharField(blank=True, max_length=100, null=True)),
                ('msr_rdt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('msr_fuelrem', models.IntegerField()),
                ('msr_patroltype', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'mersreports',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MerSrgoods',
            fields=[
                ('msrg_key', models.AutoField(primary_key=True, serialize=False)),
                ('msrg_item', models.CharField(blank=True, max_length=100, null=True)),
                ('msrg_qty', models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True)),
                ('msrg_denomination', models.CharField(blank=True, max_length=100, null=True)),
                ('msrg_category', models.CharField(blank=True, max_length=100, null=True)),
                ('msrg_subcategory', models.CharField(blank=True, max_length=100, null=True)),
                ('msrg_value', models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True)),
                ('msrg_source', models.CharField(blank=True, max_length=100, null=True)),
                ('msrg_confiscated', models.BooleanField()),
                ('msrg_remarks', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'mersrgoods',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MissionReport',
            fields=[
                ('mr_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('mr_pf_id', models.CharField(max_length=100)),
                ('mr_dtg', models.DateTimeField(blank=True, null=True)),
                ('mr_rdt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'misrep',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MRDetails',
            fields=[
                ('mrd_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('mrd_mmsi', models.CharField(max_length=100)),
                ('mrd_vessel_type', models.CharField(max_length=100)),
                ('mrd_vessel_name', models.CharField(max_length=100)),
                ('mrd_position', models.TextField()),
                ('mrd_course', models.FloatField()),
                ('mrd_speed', models.FloatField()),
                ('mrd_npoc', models.CharField(max_length=100)),
                ('mrd_lpoc', models.CharField(max_length=100)),
                ('mrd_act_desc', models.CharField(max_length=500)),
                ('mrd_dtg', models.DateTimeField()),
                ('mrd_ais_status', models.CharField(max_length=100)),
                ('mrd_call_details', models.CharField(max_length=100)),
                ('mrd_response', models.CharField(max_length=100)),
                ('mrd_remarks', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'misrep_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MVDetails',
            fields=[
                ('mvd_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('mvd_position', models.TextField()),
                ('mvd_speed', models.FloatField()),
                ('mvd_heading', models.FloatField()),
                ('mvd_status', models.CharField(max_length=100)),
                ('mvd_course', models.FloatField()),
                ('mvd_timestamp', models.DateTimeField()),
                ('mvd_dsrc', models.CharField(max_length=100)),
                ('mvd_utc_seconds', models.FloatField()),
                ('mvd_draught', models.FloatField()),
                ('mvd_rot', models.FloatField()),
                ('mvd_destination', models.CharField(max_length=100)),
                ('mvd_eta', models.DateTimeField()),
                ('mvd_current_port', models.CharField(max_length=100)),
                ('mvd_last_port', models.CharField(max_length=100)),
                ('mvd_last_port_time', models.DateTimeField()),
                ('mvd_current_port_id', models.CharField(max_length=100)),
                ('mvd_current_port_unlocode', models.CharField(max_length=100)),
                ('mvd_current_port_country', models.CharField(max_length=100)),
                ('mvd_last_port_id', models.CharField(max_length=100)),
                ('mvd_last_port_unlocode', models.CharField(max_length=100)),
                ('mvd_last_port_country', models.CharField(max_length=100)),
                ('mvd_next_port_id', models.CharField(max_length=100)),
                ('mvd_next_port_unlocode', models.CharField(max_length=100)),
                ('mvd_next_port_name', models.CharField(max_length=100)),
                ('mvd_next_port_country', models.CharField(max_length=100)),
                ('mvd_eta_calc', models.DateTimeField()),
                ('mvd_eta_updated', models.DateTimeField()),
                ('mvd_distance_to_go', models.FloatField()),
                ('mvd_distance_travelled', models.FloatField()),
                ('mvd_awg_speed', models.FloatField()),
                ('mvd_max_speed', models.FloatField()),
            ],
            options={
                'db_table': 'mv_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SituationalReport',
            fields=[
                ('sit_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('sit_dtg', models.DateTimeField()),
                ('sit_mmsi', models.CharField(max_length=100)),
                ('sit_position', models.TextField(blank=True, null=True)),
                ('sit_lpoc', models.CharField(max_length=100)),
                ('sit_last_port_country', models.CharField(max_length=100)),
                ('sit_npoc', models.CharField(max_length=100)),
                ('sit_next_port_country', models.CharField(max_length=100)),
                ('sit_course', models.FloatField()),
                ('sit_speed', models.FloatField()),
                ('sit_source', models.CharField(max_length=100)),
                ('sit_rdt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'situational_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trip_Details',
            fields=[
                ('td_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('speed', models.FloatField()),
                ('heading', models.FloatField()),
                ('status', models.CharField(max_length=100)),
                ('course', models.FloatField()),
                ('timestamp', models.DateTimeField()),
                ('utc_seconds', models.FloatField()),
                ('draught', models.FloatField()),
                ('rot', models.FloatField()),
                ('current_port', models.CharField(max_length=100)),
                ('last_port', models.CharField(max_length=100)),
                ('last_port_time', models.DateTimeField()),
                ('current_port_id', models.CharField(max_length=100)),
                ('current_port_unlocode', models.CharField(max_length=100)),
                ('current_port_country', models.CharField(max_length=100)),
                ('last_port_id', models.CharField(max_length=100)),
                ('last_port_unlocode', models.CharField(max_length=100)),
                ('last_port_country', models.CharField(max_length=100)),
                ('next_port_id', models.CharField(max_length=100)),
                ('next_port_unlocode', models.CharField(max_length=100)),
                ('next_port_name', models.CharField(max_length=100)),
                ('next_port_country', models.CharField(max_length=100)),
                ('eta_calc', models.DateTimeField()),
                ('eta_updated', models.DateTimeField()),
                ('distance_to_go', models.FloatField()),
                ('distance_travelled', models.FloatField()),
                ('awg_speed', models.FloatField()),
                ('max_speed', models.FloatField()),
            ],
            options={
                'db_table': 'mer_trip_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MerSreports2',
            fields=[
                ('msr_key', models.OneToOneField(db_column='msr2_key', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='merchant_trip', serialize=False, to='ais.mersreports')),
                ('msr2_lpoc', models.CharField(blank=True, max_length=100, null=True)),
                ('msr2_lpocdtg', models.DateField(blank=True, null=True)),
                ('msr2_npoc', models.CharField(blank=True, max_length=100, null=True)),
                ('msr2_npoceta', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mersreports2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PNSCShipData',
            fields=[
                ('ps_key', models.BigAutoField(primary_key=True, serialize=False)),
                ('ps_country', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_status_symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_status_symbol_remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_status_symbol_assigned_time', models.DateTimeField(blank=True, null=True)),
                ('ps_track_number', models.IntegerField(blank=True, null=True)),
                ('ps_position', models.TextField(blank=True, null=True)),
                ('ps_speed', models.FloatField(blank=True, null=True)),
                ('ps_course', models.FloatField(blank=True, null=True)),
                ('ps_timestamp', models.DateTimeField(blank=True, null=True)),
                ('ps_lastport', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_next_port', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_track_type', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_track_label', models.CharField(blank=True, max_length=100, null=True)),
                ('ps_rdt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ps_mv_key', models.ForeignKey(db_column='ps_mv_key', on_delete=django.db.models.deletion.CASCADE, to='ais.merchant_vessel')),
            ],
            options={
                'db_table': 'pnsc_ship_data',
            },
        ),
    ]