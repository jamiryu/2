from django.db import models

class WeldRecord(models.Model):
    birlestir = models.CharField(max_length=255, unique=False)  # Benzersiz 'birleştir' kolonu
    control_no = models.CharField(max_length=100, blank=True, null=True)  # CONTROL NO
    shop_field = models.CharField(max_length=100, blank=True, null=True)  # Shop Field
    weld_no = models.CharField(max_length=100, blank=True, null=True)  # Weld No
    dia_inch = models.FloatField(blank=True, null=True)  # DIA INCH
    dn = models.IntegerField(blank=True, null=True)  # DN
    isometri_no = models.CharField(max_length=100, blank=True, null=True)  # ISOMETRI NO
    spool_no = models.CharField(max_length=100, blank=True, null=True)  # SPOOL NO
    revision = models.CharField(max_length=50, blank=True, null=True)  # REV
    specs = models.CharField(max_length=100, blank=True, null=True)  # SPECS
    material = models.CharField(max_length=100, blank=True, null=True)  # MATERIAL
    weld_type = models.CharField(max_length=100, blank=True, null=True)  # WELD TYPE
    size_1 = models.CharField(max_length=50, blank=True, null=True)  # SIZE 1
    thick_1 = models.FloatField(blank=True, null=True)  # Thick. 1
    size_2 = models.CharField(max_length=50, blank=True, null=True)  # SIZE 2
    thick_2 = models.FloatField(blank=True, null=True)  # Thick. 2
    from_mat = models.CharField(max_length=100, blank=True, null=True)  # FROM Mat
    to_mat = models.CharField(max_length=100, blank=True, null=True)  # TO Mat
    wps_no = models.CharField(max_length=100, blank=True, null=True)  # WPS NO
    from_desc_1 = models.CharField(max_length=100, blank=True, null=True)  # FROM DESC.1
    heat_no1 = models.CharField(max_length=100, blank=True, null=True)  # HEAT NO1
    to_desc_2 = models.CharField(max_length=100, blank=True, null=True)  # TO DESC.2
    heat_no2 = models.CharField(max_length=100, blank=True, null=True)  # HEAT NO2
    fit_up_controlid = models.CharField(max_length=100, blank=True, null=True)  # FIT-UP CONTROLID
    fitup_date = models.DateField(blank=True, null=True)  # FITUP DATE
    fit_result = models.CharField(max_length=50, blank=True, null=True)  # FIT RESULT
    welder_id = models.CharField(max_length=100, blank=True, null=True)  # WELDER ID
    welder_2id = models.CharField(max_length=100, blank=True, null=True)  # WELDER 2ID
    weld_date = models.DateField(blank=True, null=True)  # WELD DATE
    weld_result = models.CharField(max_length=100, blank=True, null=True)  # WELD RESULT
    weld_process = models.CharField(max_length=100, blank=True, null=True)  # weld_process
    circ_seams_mt_pt = models.CharField(max_length=100, blank=True, null=True)  # circ. seams MT/PT
    circ_seams_rt_ut = models.CharField(max_length=100, blank=True, null=True)  # circ. seams RT/UT
    nozzle_welds_mt_pt = models.CharField(max_length=100, blank=True, null=True)  # nozzle welds MT/PT
    nozzle_welds_rt_ut = models.CharField(max_length=100, blank=True, null=True)  # nozzle welds RT/UT
    fillet_welds_mt_pt = models.CharField(max_length=100, blank=True, null=True)  # fillet welds MT/PT
    mt_pt_date = models.DateField(blank=True, null=True)  # MT/PT Date
    mt_pt_result = models.CharField(max_length=100, blank=True, null=True)  # MT/PT Result
    mt_pt_reports = models.CharField(max_length=100, blank=True, null=True)  # MT/PT Reports
    rt_ut_date = models.DateField(blank=True, null=True)  # RT/UT Date
    rt_ut_result = models.CharField(max_length=100, blank=True, null=True)  # RT/UT Result
    rt_ut_reports = models.CharField(max_length=100, blank=True, null=True)  # RT/UT Reports
    sub_system = models.CharField(max_length=100, blank=True, null=True)  # Sub-system
    description_area = models.CharField(max_length=255, blank=True, null=True)  # Description Area
    total_length = models.FloatField(blank=True, null=True)  # Total Length
    ped_cat = models.CharField(max_length=50, blank=True, null=True)  # Ped Cat
    dn1 = models.IntegerField(blank=True, null=True)  # DN1
    dn2 = models.IntegerField(blank=True, null=True)  # DN2
    sheet_no = models.CharField(max_length=50, blank=True, null=True)  # Sht.
    extra_welding_joint = models.CharField(max_length=255, blank=True, null=True)  # Extra Welding Joint By Teknokon
    modification_responsible = models.CharField(max_length=100, blank=True, null=True)  # Responsible for Modification
    test_package_no = models.CharField(max_length=100, blank=True, null=True)  # Test Package No
    fitter_id = models.CharField(max_length=100, blank=True, null=True)
    fittup_checked_count = models.IntegerField(blank=True, null=True)  # IntegerField doesn't support max_length
    remarks = models.CharField(max_length=100, blank=True, null=True)  # Fixed to lowercase 'remarks'

    def __str__(self):
        return f"Bireştir: {self.birlestir}, Weld No: {self.weld_no}, ISOMETRI NO: {self.isometri_no}"
