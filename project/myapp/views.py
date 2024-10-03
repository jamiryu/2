from django.http import JsonResponse
from .models import WeldRecord
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from datetime import datetime
import pandas as pd
from django.core.files.storage import FileSystemStorage



def index(request):
    return render(request, 'myapp/index.html')


def weldrecord_data(request):
    weldrecords = list(WeldRecord.objects.values())
    return JsonResponse(weldrecords, safe=False)


@csrf_exempt
def update_weldrecord(request, id):
    if request.method == 'PUT':
        try:
            weldrecord = WeldRecord.objects.get(pk=id)
        except WeldRecord.DoesNotExist:
            return JsonResponse({'error': 'WeldRecord not found'}, status=404)

        try:
            data = json.loads(request.body.decode('utf-8'))
            for field, value in data.items():
                if hasattr(weldrecord, field):
                    setattr(weldrecord, field, value)

            weldrecord.save()
            return JsonResponse({'success': 'WeldRecord updated successfully'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
import json
from .models import WeldRecord

@csrf_exempt
def add_weldrecord(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # WeldRecord modeline göre gerekli alanları dolduruyoruz
            weldrecord = WeldRecord(
                weld_no=data.get('weld_no', ''),
                isometri_no=data.get('isometri_no', ''),
                spool_no=data.get('spool_no', ''),
                dia_inch=data.get('dia_inch', 0),
                dn=data.get('dn', 0),
                thick_1=data.get('thick_1', 0),
                heat_no1=data.get('heat_no1', ''),
                to_desc_2=data.get('to_desc_2', ''),
                heat_no2=data.get('heat_no2', ''),
                fit_up_controlid=data.get('fit_up_controlid', ''),
                fitup_date=parse_date(data.get('fitup_date', '2000-01-01')),
                fit_result=data.get('fit_result', ''),
                welder_id=data.get('welder_id', ''),
                welder_2id=data.get('welder_2id', ''),
                weld_date=parse_date(data.get('weld_date', '2000-01-01')),
                weld_result=data.get('weld_result', '')
            )

            # Veritabanına kaydet
            weldrecord.save()
            return JsonResponse({'success': True, 'id': weldrecord.id})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Beklenmeyen hatalar için genel bir yakalama bloğu
            return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def delete_weldrecord(request, id):
    if request.method == 'DELETE':
        try:
            weldrecord = WeldRecord.objects.get(pk=id)
            weldrecord.delete()
            return JsonResponse({'success': True})
        except WeldRecord.DoesNotExist:
            return JsonResponse({'error': 'WeldRecord not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.shortcuts import render
from .models import WeldRecord

def isometri_list(request):
    isometries = WeldRecord.objects.values_list('isometri_no', flat=True).distinct()
    return render(request, 'myapp/isometries_list.html', {'isometries': isometries})

def welds_by_isometri(request, isometri_no):
    welds = WeldRecord.objects.filter(isometri_no=isometri_no)

    # Distinct values for the select fields from the database
    weld_type_options = WeldRecord.objects.values_list('weld_type', flat=True).distinct()
    dn_options = WeldRecord.objects.values_list('dn', flat=True).distinct()
    from_desc_1_options = WeldRecord.objects.values_list('from_desc_1', flat=True).distinct()
    to_desc_2_options = WeldRecord.objects.values_list('to_desc_2', flat=True).distinct()
    wps_no_options = WeldRecord.objects.values_list('wps_no', flat=True).distinct()
    welder_id_options = WeldRecord.objects.values_list('welder_id', flat=True).distinct()
    welder_2id_options = WeldRecord.objects.values_list('welder_2id', flat=True).distinct()
    weld_process_options = WeldRecord.objects.values_list('weld_process', flat=True).distinct()

    # If fitter_id, fittup_checked_count, and remarks are related to welds, ensure they are part of WeldRecord model.
    return render(request, 'myapp/welds_by_isometri.html', {
        'isometri_no': isometri_no,
        'welds': welds,
        'weld_type_options': weld_type_options,
        'dn_options': dn_options,
        'from_desc_1_options': from_desc_1_options,
        'to_desc_2_options': to_desc_2_options,
        'wps_no_options': wps_no_options,
        'welder_id_options': welder_id_options, 
        'welder_2id_options': welder_2id_options,
        'weld_process_options': weld_process_options,
        'fitter_id': welds[0].fitter_id if welds else None,  # Fitter ID (assuming all welds have the same fitter_id)
        'fittup_checked_count': welds[0].fittup_checked_count if welds else None,  # Fitup Checked Count
        'remarks': welds[0].remarks if welds else None  # Remarks
    })



@csrf_exempt
def update_weldrecord(request, id):
    if request.method == 'PUT':
        try:
            weldrecord = WeldRecord.objects.get(pk=id)
        except WeldRecord.DoesNotExist:
            return JsonResponse({'error': 'WeldRecord not found'}, status=404)

        try:
            data = json.loads(request.body.decode('utf-8'))
            for field, value in data.items():
                if hasattr(weldrecord, field):
                    setattr(weldrecord, field, value)

            weldrecord.save()
            return JsonResponse({'success': 'WeldRecord updated successfully'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)






import numpy as np
from django.db import IntegrityError, transaction

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from .models import WeldRecord

# Helper function to parse dates (including handling Excel serial date numbers)
def parse_date(date_value):
    try:
        if pd.isnull(date_value):  # Handle missing or NaT values
            return None
        # Handle Excel serial date numbers (valid only if numeric)
        if isinstance(date_value, (int, float)):
            return pd.to_datetime('1899-12-30') + pd.to_timedelta(date_value, 'D')
        # Handle regular date strings or datetime objects
        return pd.to_datetime(date_value).date()
    except Exception as e:
        # In case of any other error, return None to avoid crashing
        return None

@csrf_exempt
def import_welds(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Save the file temporarily
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_path = fs.path(filename)

        # Read the .xlsb Excel file using pyxlsb engine
        try:
            df = pd.read_excel(uploaded_file_path, engine='pyxlsb')

            # Use Django's atomic transaction to ensure that all or nothing is saved
            with transaction.atomic():
                for index, row in df.iterrows():
                    birlestir_value = row.get('birlestir', '').strip() if pd.notnull(row.get('birlestir')) else None

                    # Check if 'birlestir' is empty and stop import if it's missing
                    if not birlestir_value:
                        return JsonResponse({
                            "success": False, 
                            "error": f"Row {index + 1}: 'birlestir' field cannot be empty."
                        }, status=400)

                    # Check if 'birlestir' exists in the database
                    try:
                        weld_record = WeldRecord.objects.get(birlestir=birlestir_value)
                        # Update the existing record
                        weld_record.control_no = row.get('control_no', '') if pd.notnull(row.get('control_no')) else ''
                        weld_record.shop_field = row.get('shop_field', '') if pd.notnull(row.get('shop_field')) else ''
                        weld_record.weld_no = row.get('weld_no', '') if pd.notnull(row.get('weld_no')) else ''
                        weld_record.dia_inch = row.get('dia_inch') if pd.notnull(row.get('dia_inch')) else None
                        weld_record.dn = row.get('dn') if pd.notnull(row.get('dn')) else None
                        weld_record.isometri_no = row.get('isometri_no', '') if pd.notnull(row.get('isometri_no')) else ''
                        weld_record.spool_no = row.get('spool_no', '') if pd.notnull(row.get('spool_no')) else ''
                        weld_record.revision = row.get('revision', '') if pd.notnull(row.get('revision')) else ''
                        weld_record.specs = row.get('specs', '') if pd.notnull(row.get('specs')) else ''
                        weld_record.material = row.get('material', '') if pd.notnull(row.get('material')) else ''
                        weld_record.weld_type = row.get('weld_type', '') if pd.notnull(row.get('weld_type')) else ''
                        weld_record.size_1 = row.get('size_1', '') if pd.notnull(row.get('size_1')) else ''
                        weld_record.thick_1 = row.get('thick_1') if pd.notnull(row.get('thick_1')) else None
                        weld_record.size_2 = row.get('size_2', '') if pd.notnull(row.get('size_2')) else ''
                        weld_record.thick_2 = row.get('thick_2') if pd.notnull(row.get('thick_2')) else None
                        weld_record.from_mat = row.get('from_mat', '') if pd.notnull(row.get('from_mat')) else ''
                        weld_record.to_mat = row.get('to_mat', '') if pd.notnull(row.get('to_mat')) else ''
                        weld_record.wps_no = row.get('wps_no', '') if pd.notnull(row.get('wps_no')) else ''
                        weld_record.from_desc_1 = row.get('from_desc_1', '') if pd.notnull(row.get('from_desc_1')) else ''
                        weld_record.heat_no1 = row.get('heat_no1', '') if pd.notnull(row.get('heat_no1')) else ''
                        weld_record.to_desc_2 = row.get('to_desc_2', '') if pd.notnull(row.get('to_desc_2')) else ''
                        weld_record.heat_no2 = row.get('heat_no2', '') if pd.notnull(row.get('heat_no2')) else ''
                        weld_record.fit_up_controlid = row.get('fit_up_controlid', '') if pd.notnull(row.get('fit_up_controlid')) else ''
                        
                        # Correct date parsing, including serial date handling
                        weld_record.fitup_date = parse_date(row.get('fitup_date'))
                        weld_record.weld_date = parse_date(row.get('weld_date'))
                        weld_record.mt_pt_date = parse_date(row.get('mt_pt_date'))
                        weld_record.rt_ut_date = parse_date(row.get('rt_ut_date'))
                        
                        weld_record.fit_result = row.get('fit_result', '') if pd.notnull(row.get('fit_result')) else ''
                        weld_record.welder_id = row.get('welder_id', '') if pd.notnull(row.get('welder_id')) else ''
                        weld_record.welder_2id = row.get('welder_2id', '') if pd.notnull(row.get('welder_2id')) else ''
                        weld_record.weld_result = row.get('weld_result', '') if pd.notnull(row.get('weld_result')) else ''
                        weld_record.weld_process = row.get('weld_process', '') if pd.notnull(row.get('weld_process')) else ''
                        weld_record.circ_seams_mt_pt = row.get('circ_seams_mt_pt', '') if pd.notnull(row.get('circ_seams_mt_pt')) else ''
                        weld_record.circ_seams_rt_ut = row.get('circ_seams_rt_ut', '') if pd.notnull(row.get('circ_seams_rt_ut')) else ''
                        weld_record.nozzle_welds_mt_pt = row.get('nozzle_welds_mt_pt', '') if pd.notnull(row.get('nozzle_welds_mt_pt')) else ''
                        weld_record.nozzle_welds_rt_ut = row.get('nozzle_welds_rt_ut', '') if pd.notnull(row.get('nozzle_welds_rt_ut')) else ''
                        weld_record.fillet_welds_mt_pt = row.get('fillet_welds_mt_pt', '') if pd.notnull(row.get('fillet_welds_mt_pt')) else ''
                        weld_record.mt_pt_result = row.get('mt_pt_result', '') if pd.notnull(row.get('mt_pt_result')) else ''
                        weld_record.mt_pt_reports = row.get('mt_pt_reports', '') if pd.notnull(row.get('mt_pt_reports')) else ''
                        weld_record.rt_ut_result = row.get('rt_ut_result', '') if pd.notnull(row.get('rt_ut_result')) else ''
                        weld_record.rt_ut_reports = row.get('rt_ut_reports', '') if pd.notnull(row.get('rt_ut_reports')) else ''
                        weld_record.sub_system = row.get('sub_system', '') if pd.notnull(row.get('sub_system')) else ''
                        weld_record.description_area = row.get('description_area', '') if pd.notnull(row.get('description_area')) else ''
                        weld_record.total_length = row.get('total_length') if pd.notnull(row.get('total_length')) else None
                        weld_record.ped_cat = row.get('ped_cat', '') if pd.notnull(row.get('ped_cat')) else ''
                        weld_record.dn1 = row.get('dn1') if pd.notnull(row.get('dn1')) else None
                        weld_record.dn2 = row.get('dn2') if pd.notnull(row.get('dn2')) else None
                        weld_record.sheet_no = row.get('sheet_no', '') if pd.notnull(row.get('sheet_no')) else ''
                        weld_record.extra_welding_joint = row.get('extra_welding_joint', '') if pd.notnull(row.get('extra_welding_joint')) else ''
                        weld_record.modification_responsible = row.get('modification_responsible', '') if pd.notnull(row.get('modification_responsible')) else ''
                        weld_record.test_package_no = row.get('test_package_no', '') if pd.notnull(row.get('test_package_no')) else ''

                        # Save the updated record
                        weld_record.save()

                    except WeldRecord.DoesNotExist:
                        # If the record does not exist, create a new one
                        WeldRecord.objects.create(
                            birlestir=birlestir_value,
                            control_no=row.get('control_no', '') if pd.notnull(row.get('control_no')) else '',
                            shop_field=row.get('shop_field', '') if pd.notnull(row.get('shop_field')) else '',
                            weld_no=row.get('weld_no', '') if pd.notnull(row.get('weld_no')) else '',
                            dia_inch=row.get('dia_inch') if pd.notnull(row.get('dia_inch')) else None,
                            dn=row.get('dn') if pd.notnull(row.get('dn')) else None,
                            isometri_no=row.get('isometri_no', '') if pd.notnull(row.get('isometri_no')) else '',
                            spool_no=row.get('spool_no', '') if pd.notnull(row.get('spool_no')) else '',
                            revision=row.get('revision', '') if pd.notnull(row.get('revision')) else '',
                            specs=row.get('specs', '') if pd.notnull(row.get('specs')) else '',
                            material=row.get('material', '') if pd.notnull(row.get('material')) else '',
                            weld_type=row.get('weld_type', '') if pd.notnull(row.get('weld_type')) else '',
                            size_1=row.get('size_1', '') if pd.notnull(row.get('size_1')) else '',
                            thick_1=row.get('thick_1') if pd.notnull(row.get('thick_1')) else None,
                            size_2=row.get('size_2', '') if pd.notnull(row.get('size_2')) else '',
                            thick_2=row.get('thick_2') if pd.notnull(row.get('thick_2')) else None,
                            from_mat=row.get('from_mat', '') if pd.notnull(row.get('from_mat')) else '',
                            to_mat=row.get('to_mat', '') if pd.notnull(row.get('to_mat')) else '',
                            wps_no=row.get('wps_no', '') if pd.notnull(row.get('wps_no')) else '',
                            from_desc_1=row.get('from_desc_1', '') if pd.notnull(row.get('from_desc_1')) else '',
                            heat_no1=row.get('heat_no1', '') if pd.notnull(row.get('heat_no1')) else '',
                            to_desc_2=row.get('to_desc_2', '') if pd.notnull(row.get('to_desc_2')) else '',
                            heat_no2=row.get('heat_no2', '') if pd.notnull(row.get('heat_no2')) else '',
                            fit_up_controlid=row.get('fit_up_controlid', '') if pd.notnull(row.get('fit_up_controlid')) else '',
                            fitup_date=parse_date(row.get('fitup_date')),
                            fit_result=row.get('fit_result', '') if pd.notnull(row.get('fit_result')) else '',
                            welder_id=row.get('welder_id', '') if pd.notnull(row.get('welder_id')) else '',
                            welder_2id=row.get('welder_2id', '') if pd.notnull(row.get('welder_2id')) else '',
                            weld_date=parse_date(row.get('weld_date')),
                            weld_result=row.get('weld_result', '') if pd.notnull(row.get('weld_result')) else '',
                            weld_process=row.get('weld_process', '') if pd.notnull(row.get('weld_process')) else '',
                            circ_seams_mt_pt=row.get('circ_seams_mt_pt', '') if pd.notnull(row.get('circ_seams_mt_pt')) else '',
                            circ_seams_rt_ut=row.get('circ_seams_rt_ut', '') if pd.notnull(row.get('circ_seams_rt_ut')) else '',
                            nozzle_welds_mt_pt=row.get('nozzle_welds_mt_pt', '') if pd.notnull(row.get('nozzle_welds_mt_pt')) else '',
                            nozzle_welds_rt_ut=row.get('nozzle_welds_rt_ut', '') if pd.notnull(row.get('nozzle_welds_rt_ut')) else '',
                            fillet_welds_mt_pt=row.get('fillet_welds_mt_pt', '') if pd.notnull(row.get('fillet_welds_mt_pt')) else '',
                            mt_pt_date=parse_date(row.get('mt_pt_date')),
                            mt_pt_result=row.get('mt_pt_result', '') if pd.notnull(row.get('mt_pt_result')) else '',
                            mt_pt_reports=row.get('mt_pt_reports', '') if pd.notnull(row.get('mt_pt_reports')) else '',
                            rt_ut_date=parse_date(row.get('rt_ut_date')),
                            rt_ut_result=row.get('rt_ut_result', '') if pd.notnull(row.get('rt_ut_result')) else '',
                            rt_ut_reports=row.get('rt_ut_reports', '') if pd.notnull(row.get('rt_ut_reports')) else '',
                            sub_system=row.get('sub_system', '') if pd.notnull(row.get('sub_system')) else '',
                            description_area=row.get('description_area', '') if pd.notnull(row.get('description_area')) else '',
                            total_length=row.get('total_length') if pd.notnull(row.get('total_length')) else None,
                            ped_cat=row.get('ped_cat', '') if pd.notnull(row.get('ped_cat')) else '',
                            dn1=row.get('dn1') if pd.notnull(row.get('dn1')) else None,
                            dn2=row.get('dn2') if pd.notnull(row.get('dn2')) else None,
                            sheet_no=row.get('sheet_no', '') if pd.notnull(row.get('sheet_no')) else '',
                            extra_welding_joint=row.get('extra_welding_joint', '') if pd.notnull(row.get('extra_welding_joint')) else '',
                            modification_responsible=row.get('modification_responsible', '') if pd.notnull(row.get('modification_responsible')) else '',
                            test_package_no=row.get('test_package_no', '') if pd.notnull(row.get('test_package_no')) else ''
                        )

            return JsonResponse({"success": True, "message": "Weld records imported/updated successfully"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return render(request, 'myapp/import_welds.html')


from django.http import HttpResponse
from openpyxl import Workbook
from .models import WeldRecord

def export_weldrecords_excel(request):
    # Yeni bir çalışma kitabı oluştur
    wb = Workbook()
    ws = wb.active
    ws.title = "Weld Records"

    # Başlık satırını yaz
    ws.append([
        'Birleştir', 'Control No', 'Shop Field', 'Weld No', 'DIA Inch', 'DN', 
        'ISOMETRI No', 'Spool No', 'REV', 'Specs', 'Material', 'Weld Type', 
        'Size 1', 'Thick 1', 'Size 2', 'Thick 2', 'From Mat', 'To Mat', 'WPS No',
        'From Desc 1', 'Heat No 1', 'To Desc 2', 'Heat No 2', 'Fit-Up Control ID',
        'Fitup Date', 'Fit Result', 'Welder ID', 'Welder 2 ID', 'Weld Date', 'Weld Result',
        'Weld Process', 'Circ Seams MT/PT', 'Circ Seams RT/UT', 'Nozzle Welds MT/PT',
        'Nozzle Welds RT/UT', 'Fillet Welds MT/PT', 'MT/PT Date', 'MT/PT Result', 
        'MT/PT Reports', 'RT/UT Date', 'RT/UT Result', 'RT/UT Reports', 'Sub-system',
        'Description Area', 'Total Length', 'Ped Cat', 'DN1', 'DN2', 'Sheet No',
        'Extra Welding Joint', 'Responsible for Modification', 'Test Package No', 
        'Fitter ID', 'Fitup Checked Count', 'Remarks'
    ])

    # Veritabanından tüm weld kayıtlarını çek ve satır satır yaz
    for weldrecord in WeldRecord.objects.all():
        ws.append([
            weldrecord.birlestir, weldrecord.control_no, weldrecord.shop_field, weldrecord.weld_no, 
            weldrecord.dia_inch, weldrecord.dn, weldrecord.isometri_no, weldrecord.spool_no, 
            weldrecord.revision, weldrecord.specs, weldrecord.material, weldrecord.weld_type,
            weldrecord.size_1, weldrecord.thick_1, weldrecord.size_2, weldrecord.thick_2,
            weldrecord.from_mat, weldrecord.to_mat, weldrecord.wps_no, weldrecord.from_desc_1,
            weldrecord.heat_no1, weldrecord.to_desc_2, weldrecord.heat_no2, weldrecord.fit_up_controlid,
            weldrecord.fitup_date, weldrecord.fit_result, weldrecord.welder_id, weldrecord.welder_2id,
            weldrecord.weld_date, weldrecord.weld_result, weldrecord.weld_process, 
            weldrecord.circ_seams_mt_pt, weldrecord.circ_seams_rt_ut, weldrecord.nozzle_welds_mt_pt,
            weldrecord.nozzle_welds_rt_ut, weldrecord.fillet_welds_mt_pt, weldrecord.mt_pt_date,
            weldrecord.mt_pt_result, weldrecord.mt_pt_reports, weldrecord.rt_ut_date,
            weldrecord.rt_ut_result, weldrecord.rt_ut_reports, weldrecord.sub_system,
            weldrecord.description_area, weldrecord.total_length, weldrecord.ped_cat,
            weldrecord.dn1, weldrecord.dn2, weldrecord.sheet_no, weldrecord.extra_welding_joint,
            weldrecord.modification_responsible, weldrecord.test_package_no, 
            weldrecord.fitter_id, weldrecord.fittup_checked_count, weldrecord.remarks
        ])

    # HTTP yanıtı ve Excel dosyası oluştur
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="weldrecords.xlsx"'

    # Workbook'u yanıtın çıktısına kaydet
    wb.save(response)

    return response

from django.http import HttpResponse
from openpyxl import Workbook
from .models import WeldRecord
from django.utils.dateparse import parse_date

def export_welds_by_date(request):
    if request.method == 'POST':  # POST request check
        # Get the type of date filter (fitup or weld)
        date_type = request.POST.get('date_type')

        # Initialize an empty queryset
        records = WeldRecord.objects.none()

        # Process Fit-up Date Filter
        if date_type == 'fitup':
            fitup_start_date = request.POST.get('fitup_start_date')
            fitup_end_date = request.POST.get('fitup_end_date')

            # Check if both fitup start and end dates are provided
            if fitup_start_date and fitup_end_date:
                fitup_start_date = parse_date(fitup_start_date)
                fitup_end_date = parse_date(fitup_end_date)

                if fitup_start_date and fitup_end_date:
                    records = WeldRecord.objects.filter(fitup_date__range=[fitup_start_date, fitup_end_date])

        # Process Weld Date Filter
        elif date_type == 'weld':
            weld_start_date = request.POST.get('weld_start_date')
            weld_end_date = request.POST.get('weld_end_date')

            # Check if both weld start and end dates are provided
            if weld_start_date and weld_end_date:
                weld_start_date = parse_date(weld_start_date)
                weld_end_date = parse_date(weld_end_date)

                if weld_start_date and weld_end_date:
                    records = WeldRecord.objects.filter(weld_date__range=[weld_start_date, weld_end_date])

        # If no records are found, return an error message
        if not records.exists():
            return HttpResponse("No records found for the selected date range.")

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Weld Records"
        
        # Add headers for each field in the WeldRecord model
        ws.append([
            'Birleştir', 'Control No', 'Shop Field', 'Weld No', 'DIA Inch', 'DN', 'Isometri No', 'Spool No', 'Revision',
            'Specs', 'Material', 'Weld Type', 'Size 1', 'Thick 1', 'Size 2', 'Thick 2', 'From Mat', 'To Mat',
            'WPS No', 'From Desc 1', 'Heat No1', 'To Desc 2', 'Heat No2', 'Fit-up Control ID', 'Fit-up Date', 'Fit Result',
            'Welder ID', 'Welder 2ID', 'Weld Date', 'Weld Result', 'Weld Process', 'Circ Seams MT/PT', 'Circ Seams RT/UT',
            'Nozzle Welds MT/PT', 'Nozzle Welds RT/UT', 'Fillet Welds MT/PT', 'MT/PT Date', 'MT/PT Result', 'MT/PT Reports',
            'RT/UT Date', 'RT/UT Result', 'RT/UT Reports', 'Sub System', 'Description Area', 'Total Length', 'Ped Cat',
            'DN1', 'DN2', 'Sheet No', 'Extra Welding Joint', 'Modification Responsible', 'Test Package No', 'Fitter ID',
            'Fit-up Checked Count', 'Remarks'
        ])
        
        # Add the rows of data from the filtered records
        for record in records:
            ws.append([
                record.birlestir, record.control_no, record.shop_field, record.weld_no, record.dia_inch, record.dn,
                record.isometri_no, record.spool_no, record.revision, record.specs, record.material, record.weld_type,
                record.size_1, record.thick_1, record.size_2, record.thick_2, record.from_mat, record.to_mat, record.wps_no,
                record.from_desc_1, record.heat_no1, record.to_desc_2, record.heat_no2, record.fit_up_controlid, record.fitup_date,
                record.fit_result, record.welder_id, record.welder_2id, record.weld_date, record.weld_result, record.weld_process,
                record.circ_seams_mt_pt, record.circ_seams_rt_ut, record.nozzle_welds_mt_pt, record.nozzle_welds_rt_ut,
                record.fillet_welds_mt_pt, record.mt_pt_date, record.mt_pt_result, record.mt_pt_reports, record.rt_ut_date,
                record.rt_ut_result, record.rt_ut_reports, record.sub_system, record.description_area, record.total_length,
                record.ped_cat, record.dn1, record.dn2, record.sheet_no, record.extra_welding_joint, record.modification_responsible,
                record.test_package_no, record.fitter_id, record.fittup_checked_count, record.remarks
            ])

        # Send the Excel file as an HTTP response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="weld_records.xlsx"'
        wb.save(response)

        return response

    return HttpResponse("Invalid request method")

def export_page(request):
    return render(request, 'myapp/export.html')