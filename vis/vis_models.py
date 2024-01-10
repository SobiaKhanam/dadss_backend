from django.db import models


class ActivityLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    log_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    subject_id = models.PositiveBigIntegerField(blank=True, null=True)
    subject_type = models.CharField(max_length=255, blank=True, null=True)
    event = models.CharField(max_length=150, blank=True, null=True)
    causer_id = models.PositiveBigIntegerField(blank=True, null=True)
    causer_type = models.CharField(max_length=255, blank=True, null=True)
    properties = models.JSONField(blank=True, null=True)
    batch_uuid = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_log'


class ApprehensionCrewLogs(models.Model):
    boat_apprehension_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apprehension_crew_logs'


class ApprehensionNakwaLogs(models.Model):
    boat_apprehension_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apprehension_nakwa_logs'


class BlacklistBoats(models.Model):
    boat_id = models.PositiveIntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blacklist_boats'


class BlacklistPeople(models.Model):
    person_id = models.PositiveIntegerField(blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blacklist_people'


class BoatApprehensions(models.Model):
    boat_id = models.PositiveIntegerField(blank=True, null=True)
    cap_date = models.DateField(blank=True, null=True)
    rel_date = models.DateField(blank=True, null=True)
    offence = models.CharField(max_length=1000, blank=True, null=True)
    decision = models.CharField(max_length=1000, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    personnel = models.CharField(max_length=200, blank=True, null=True)
    qty = models.CharField(max_length=100, blank=True, null=True)
    type_of_drugs = models.CharField(max_length=100, blank=True, null=True)
    dtg = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_apprehensions'


class BoatLocations(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_locations'


class BoatOwners(models.Model):
    boat_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    share = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_owners'


class BoatPeople(models.Model):
    boat_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    person_for = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_people'


class BoatPurposes(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_purposes'


class BoatRegnoPostfixes(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_regno_postfixes'


class BoatTripLogs(models.Model):
    boat_id = models.PositiveIntegerField(blank=True, null=True)
    nakwa_name = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    mole = models.CharField(max_length=10, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    crew = models.CharField(max_length=20, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    dep_date = models.DateTimeField(blank=True, null=True)
    pc_date = models.DateField(blank=True, null=True)
    pc_issue_date = models.DateField(blank=True, null=True)
    pc_days = models.IntegerField(blank=True, null=True)
    dep_jetty = models.ForeignKey('Jetty', models.DO_NOTHING, db_column='dep_jetty', blank=True, null=True)
    arrived_jetty = models.ForeignKey('Jetty', models.DO_NOTHING, db_column='arrived_jetty', blank=True, null=True, related_name='arrived_jetty')
    commodity = models.ForeignKey('Commoditys', models.DO_NOTHING, db_column='commodity', blank=True, null=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    fish_type = models.ForeignKey('FishTypes', models.DO_NOTHING, db_column='fish_type', blank=True, null=True)
    fish_weight = models.FloatField(blank=True, null=True)
    fishing_latitude = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    fishing_longitude = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    remarks = models.TextField(db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    dep_by_user_id = models.IntegerField(blank=True, null=True)
    dep_by_user_ip = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    arrived_by_user_id = models.IntegerField(blank=True, null=True)
    arrived_by_user_ip = models.CharField(max_length=50, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    user_location = models.ForeignKey('UserLocations', models.DO_NOTHING, blank=True, null=True)
    arrival_user_location = models.ForeignKey('UserLocations', models.DO_NOTHING, blank=True, null=True, related_name='arrival_user_location')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_trip_logs'


class BoatTypes(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_types'


class BoatWarnings(models.Model):
    boat_id = models.PositiveIntegerField(blank=True, null=True)
    cap_date = models.DateField(blank=True, null=True)
    offence = models.TextField(blank=True, null=True)
    rel_date = models.DateField(blank=True, null=True)
    decision = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boat_warnings'


class Boats(models.Model):
    old_id = models.PositiveIntegerField(blank=True, null=True)
    reg_no = models.CharField(max_length=20, blank=True, null=True)
    reg_no_int = models.PositiveIntegerField(blank=True, null=True)
    reg_no_str = models.CharField(max_length=10, blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    boat_name = models.CharField(max_length=50, blank=True, null=True)
    boat_type_id = models.PositiveIntegerField(blank=True, null=True)
    boat_length = models.CharField(max_length=50, blank=True, null=True)
    boat_breadth = models.CharField(max_length=50, blank=True, null=True)
    boat_tonnage = models.CharField(max_length=50, blank=True, null=True)
    boat_kole = models.CharField(max_length=100, blank=True, null=True)
    boat_built = models.CharField(max_length=100, blank=True, null=True)
    boat_location_id = models.PositiveIntegerField(blank=True, null=True)
    boat_engine_no = models.CharField(max_length=100, blank=True, null=True)
    boat_purpose_id = models.PositiveIntegerField(blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    pc_issue_date = models.DateField(blank=True, null=True)
    pc_days = models.IntegerField(blank=True, null=True)
    pc_expiry_date = models.DateField(blank=True, null=True)
    communication_equipment = models.CharField(max_length=255, blank=True, null=True)
    boat_photo = models.CharField(max_length=30, blank=True, null=True)
    boat_remarks = models.TextField(blank=True, null=True)
    user_location_id = models.PositiveIntegerField(blank=True, null=True)
    is_updated_photo = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boats'


class Commoditys(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commoditys'


class CrewLogs(models.Model):
    boat_trip_log_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crew_logs'


class Dhows(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dhows'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class FishTypes(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fish_types'


class Jetty(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    user_location_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jetty'


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class ModelHasPermissions(models.Model):
    permission_id = models.PositiveBigIntegerField(primary_key=True)
    model_type = models.CharField(max_length=255)
    model_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_has_permissions'
        unique_together = (('permission_id', 'model_id', 'model_type'),)


class ModelHasRoles(models.Model):
    role_id = models.PositiveBigIntegerField(primary_key=True)
    model_type = models.CharField(max_length=255)
    model_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_has_roles'
        unique_together = (('role_id', 'model_id', 'model_type'),)


class MultiplePhotos(models.Model):
    boat = models.ForeignKey(Boats, models.DO_NOTHING, blank=True, null=True)
    photo_title = models.CharField(max_length=255, blank=True, null=True)
    photo_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'multiple_photos'


class NakwaLogs(models.Model):
    boat_trip_log_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nakwa_logs'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class People(models.Model):
    old_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    s_w_d_of = models.CharField(max_length=50, blank=True, null=True)
    cnic_no = models.CharField(unique=True, max_length=13, blank=True, null=True)
    cnic_expiry_date = models.DateField(blank=True, null=True)
    life_time = models.CharField(max_length=1, blank=True, null=True)
    cnic_photo = models.CharField(max_length=50, blank=True, null=True)
    photo = models.CharField(max_length=50, blank=True, null=True)
    cell_no = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_updated_photo = models.CharField(max_length=1, blank=True, null=True)
    is_updated_cnic = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    guard_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class RoleHasPermissions(models.Model):
    permission_id = models.PositiveBigIntegerField(primary_key=True)
    role_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'role_has_permissions'
        unique_together = (('permission_id', 'role_id'),)


class Roles(models.Model):
    name = models.CharField(max_length=255)
    guard_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class UseLogs(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'use_logs'


class UserLocations(models.Model):
    title = models.CharField(max_length=30, db_collation='utf8mb4_unicode_ci', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_locations'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    username = models.CharField(unique=True, max_length=60)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    user_location_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class WarningCrewLogs(models.Model):
    boat_warning_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warning_crew_logs'


class WarningNakwaLogs(models.Model):
    boat_warning_id = models.PositiveIntegerField(blank=True, null=True)
    person_id = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warning_nakwa_logs'
