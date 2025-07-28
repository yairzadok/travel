from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import EmailMessage, send_mass_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from tours.models import TravelerRegistration, Tour


@csrf_exempt
def update_presence(request):
    if request.method == "POST":
        registration_id = request.POST.get('id')
        is_present = request.POST.get('present') == 'true'
        registration = get_object_or_404(TravelerRegistration, id=registration_id)
        registration.traveler_attendance = is_present
        registration.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def send_attendance_report(request):
    if request.method == 'POST':
        tour_guide_email = request.POST.get('tour_guide_email')
        if not tour_guide_email:
            return JsonResponse({'success': False, 'error': 'No tour_guide_email provided'})

        registrations = TravelerRegistration.objects.all()
        now = timezone.localtime().strftime("%d/%m/%Y %H:%M")
        body = f"דו\"ח נוכחות לסיור נכון ל-{now}:\n\n"
        for reg in registrations:
            status = "✅ נוכח" if reg.traveler_attendance else "❌ לא נוכח"
            body += f"{reg.traveler_first_name} {reg.traveler_last_name} | {reg.traveler_phone} | {status}\n"

        email_message = EmailMessage(
            subject=f'דו"ח נוכחות לסיור - {now}',
            body=body,
            to=[tour_guide_email]
        )
        email_message.send()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'})


@csrf_exempt
def mark_present_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('registration_code')
        if not code:
            return JsonResponse({'success': False, 'error': 'Missing registration code'})
        try:
            registration = TravelerRegistration.objects.get(registration_code=code)
            registration.traveler_attendance = True
            registration.save()
            return JsonResponse({'success': True, 'id': registration.id})
        except TravelerRegistration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registration not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def send_reminder_per_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    emails = [reg.traveler_email for reg in tour.registrations.all() if reg.traveler_email]

    messages = [
        (
            f'הזכרת השתתפות בטיול "{tour.tour_title}"',
            f'שלום,\n\nתזכורת להשתתפותך בטיול שיתקיים בתאריך {tour.tour_date}.\n\nבברכה,\nצוות ההדרכה',
            'your@tour_guide_email.com',
            [email]
        )
        for email in emails
    ]
    send_mass_mail(messages, fail_silently=False)
    return redirect('participants_list')
