from django.urls import path
from .views import weldrecord_data, update_weldrecord, add_weldrecord, delete_weldrecord, index
from .views import isometri_list, welds_by_isometri, export_weldrecords_excel, import_welds, export_page,export_welds_by_date  

urlpatterns = [
    path('', index, name='index'),  # Ana sayfa (HTML sayfası)
    path('api/weldrecords/', weldrecord_data, name='weldrecord_data'),  # WeldRecord veri setini dönen API
    path('api/weldrecords/add/', add_weldrecord, name='add_weldrecord'),  # Yeni WeldRecord ekleme API'si
    path('api/weldrecords/<int:id>/', update_weldrecord, name='update_weldrecord'),  # WeldRecord güncelleme API'si
    path('api/weldrecords/delete/<int:id>/', delete_weldrecord, name='delete_weldrecord'),  # WeldRecord silme API'si
    path('isometries/', isometri_list, name='isometri_list'),
    path('api/welds/<str:isometri_no>/', welds_by_isometri, name='welds_by_isometri'),
    path('api/welds/<int:weld_id>/', welds_by_isometri, name='welds_by_isometri'),
    path('import-welds/', import_welds, name='import_welds'),
    path('isometries/welds/<str:isometri_no>/', welds_by_isometri, name='welds_by_isometri'),
    path('export-weldrecords-excel/', export_weldrecords_excel, name='export_weldrecords_excel'),
    path('export-page/', export_page, name='export_page'),  # Corrected syntax, no trailing comma here
    path('export-welds-by-date/', export_welds_by_date, name='export_welds_by_date'),  # Add this line

]
