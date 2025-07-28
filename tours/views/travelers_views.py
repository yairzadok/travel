from django.shortcuts import render, redirect, get_object_or_404
from tours.models import Tour, TravelerRegistration
from tours.forms import RegistrationForm
from django.db.models import Q
from django.forms import formset_factory
from django.conf import settings
from tours.views.utils_views import send_registration_email
def home(request):
    query = request.GET.get('q', '')
    guide = request.GET.get('guide', '')
    date = request.GET.get('date', '')

    tours = Tour.objects.all()

    if query:
        tours = tours.filter(
            Q(tour_title__icontains=query) |
            Q(tour_subtitle__icontains=query) |
            Q(tour_description__icontains=query)
        )

    if guide:
        tours = tours.filter(tour_guide_name__tour_guide_first_name__icontains=guide)

    if date:
        tours = tours.filter(tour_date=date)

    # מיון לפי תאריך
    tours = tours.order_by('tour_date')

    return render(request, 'travelers/home.html', {
        'tours': tours,
        'query': query,
        'guide': guide,
        'date': date
    })


def register(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    try:
        if request.method == 'POST':
            num_participants = int(request.POST.get('num_participants', 1))
        else:
            num_participants = int(request.GET.get('num_participants', 1))
    except (ValueError, TypeError):
        num_participants = 1

    num_participants = max(1, min(num_participants, tour.max_participants))
    RegistrationFormSet = formset_factory(RegistrationForm, extra=num_participants)

    total_price = round(tour.tour_price * num_participants, 2) if tour.tour_price else 0

    if request.method == 'POST':
        formset = RegistrationFormSet(request.POST)
        if formset.is_valid():
            main_traveler = None
            for i, form in enumerate(formset):
                traveler = form.save(commit=False)
                traveler.tour = tour
                if i == 0:
                    traveler.total_price = total_price  # 💾 שמירת סכום למשתתף הראשי
                    main_traveler = traveler
                traveler.save()

                # שליחת מייל מעוצב עם QR וקוד רישום
    #            send_registration_email(traveler, tour)

            request.session['num_participants'] = num_participants  # 🧠 שמירת מספר משתתפים ל־checkout
            return redirect('checkout', traveler_id=main_traveler.id)
    else:
        formset = RegistrationFormSet()

    context = {
        'tour': tour,
        'formset': formset,
        'num_participants': num_participants,
        'total_price': total_price,
    }
    return render(request, 'travelers/traveler_register.html', context)

def payment_redirect(request):
    return render(request, 'travelers/payment_redirect.html')

def success(request, traveler_id):
    traveler_registration = get_object_or_404(TravelerRegistration, id=traveler_id)
    return render(request, 'travelers/success.html', {
        'traveler_registration': traveler_registration
    })

def registration_list(request):
    tours = Tour.objects.prefetch_related('registrations').all()
    return render(request, 'travelers/registration_list.html', {'tours': tours})

def delete_registration(request, registration_id):
    traveler_attendance = get_object_or_404(TravelerRegistration, id=registration_id)
    traveler_attendance.delete()
    return redirect('registration_list')

def toggle_attendance(request, registration_id):
    traveler_attendance = get_object_or_404(TravelerRegistration, id=registration_id)
    traveler_attendance.is_present = not traveler_attendance.is_present
    traveler_attendance.save()
    return redirect('registration_list')

def participants_list(request):
    tour_id = request.GET.get('tour_id')
    if tour_id:
        traveler_attendance = TravelerRegistration.objects.filter(tour_id=tour_id)
    else:
        traveler_attendance = TravelerRegistration.objects.all()
    return render(request, 'travelers/participants_list.html', {'registrations': traveler_attendance})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    return render(request, 'travelers/tour_detail.html', {'tour': tour})

