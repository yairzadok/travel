import openpyxl
from django.http import HttpResponse
from tours.models import TravelerRegistration


def export_registrations_excel(tour_id=None):
    """
    יוצר קובץ Excel עם רשימת נרשמים. ניתן לסנן לפי סיור (tour_id).
    """
    # קובץ תגובה להורדה
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="registrations.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "נרשמים"

    # כותרות
    sheet.append(['שם פרטי', 'שם משפחה', 'טלפון', 'אימייל', 'נוכחות'])

    # סינון לפי סיור אם יש
    queryset = TravelerRegistration.objects.all()
    if tour_id:
        queryset = queryset.filter(tour_id=tour_id)

    for registration in queryset:
        sheet.append([
            registration.first_name,
            registration.last_name,
            registration.phone,
            registration.email,
            'הגיע' if registration.attendance else 'לא הגיע',
        ])

    workbook.save(response)
    return response
