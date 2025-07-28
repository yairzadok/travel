from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from tours.models import TravelerRegistration

def checkout_view(request, traveler_id):
    traveler = get_object_or_404(TravelerRegistration, id=traveler_id)
    tour = traveler.tour
    num_participants = request.session.get('num_participants', 1)
    total_price = round(tour.tour_price * num_participants, 2) if tour.tour_price else 0

    return render(request, 'payments/checkout.html', {
        'traveler': traveler,
        'tour': tour,
        'num_participants': num_participants,
        'total_price': total_price,
    })

def checkout_submit(request, traveler_id):
    if request.method == 'POST':
        traveler = get_object_or_404(TravelerRegistration, id=traveler_id)
        user_email = traveler.traveler_email
        tour_name = traveler.tour.tour_title
        amount = round(traveler.tour.tour_price * request.session.get('num_participants', 1), 2)

        try:
            send_mail(
                subject='התשלום בוצע בהצלחה',
                message=(
                    f'שלום {traveler.traveler_first_name},\n\n'
                    f'התשלום שלך עבור "{tour_name}" התקבל בהצלחה.\n'
                    f'סכום: ₪{amount}\n\n'
                    'תודה שבחרת בנו 🌿'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            print("✅ מייל נשלח ל:", user_email)
        except Exception as e:
            print("❌ שגיאה בשליחת מייל:", e)

        return redirect('success', traveler_id=traveler.id)

