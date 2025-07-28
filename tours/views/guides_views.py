from django.shortcuts import render, redirect, get_object_or_404
from tours.models import Tour, TourGuide
from tours.forms import TourForm, TourGuideForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, 'management/admin_dashboard.html')

def all_guides_view(request):
    query = request.GET.get('q', '')
    guides = TourGuide.objects.all()

    if query:
        guides = guides.filter(
            Q(tour_guide_first_name__icontains=query) |
            Q(tour_guide_last_name__icontains=query)
        )

    return render(request, 'guides/all_guides.html', {
        'guides': guides,
        'query': query,
    })

def tours_by_guide(request, guide_id):
    guide = get_object_or_404(TourGuide, id=guide_id)
    tours = Tour.objects.filter(tour_guide_name=guide).order_by('tour_date')
    return render(request, 'travelers/home.html', {
        'tours': tours,
        'guide': guide,
    })

def email_all_guides(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        recipients = TourGuide.objects.values_list('tour_guide_email', flat=True)
        datatuple = [
            (subject, message, None, [email]) for email in recipients if email
        ]

        send_mass_mail(datatuple, fail_silently=False)
        messages.success(request, "המייל נשלח לכל מורי הדרך בהצלחה.")
        return redirect('guides_list')  # חזרה לרשימה לאחר השליחה

    return render(request, 'guides/send_email.html')


def guides_list_view(request):
    guides = TourGuide.objects.all()
    return render(request, 'guides/guides_list.html', {'guides': guides})

def export_guides_excel(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="guides_export.csv"'

    # כתיבה בקידוד שתואם לאקסל (כולל BOM)
    writer = csv.writer(response)
    response.write('\ufeff')  # כתיבת BOM ידנית כדי לתמוך בעברית באקסל

    writer.writerow(['שם פרטי', 'שם משפחה', 'טלפון', 'אימייל', 'שפות', 'התמחויות', 'ניסיון', 'המלצות'])

    for guide in TourGuide.objects.all():
        writer.writerow([
            guide.tour_guide_first_name,
            guide.tour_guide_last_name,
            f'="{guide.tour_guide_phone}"',
            guide.tour_guide_email,
            guide.languages,
            guide.specialties,
            guide.experience,
            guide.recommendations,
        ])

    return response

def register_tour_guide(request):
    if request.method == 'POST':
        form = TourGuideForm(request.POST, request.FILES)
        if form.is_valid():
            guide = form.save()

            # שמירת שם המדריך ב-session
            request.session['guide_first_name'] = guide.tour_guide_first_name

            # תוכן המייל
            context = {
                'first_name': guide.tour_guide_first_name,
            }

            subject = 'Travel2Go - ההרשמה שלך התקבלה בהצלחה'
            text_content = render_to_string('emails/guide_welcome.txt', context)
            html_content = render_to_string('emails/guide_welcome.html', context)

            # שליחת מייל
            send_mail(
                subject,
                text_content,
                'noreply@travel2go.com',  # כתובת השולח
                [guide.tour_guide_email],  # למי לשלוח
                html_message=html_content,
                fail_silently=False,
            )

            return redirect('guide_thank_you')
    else:
        form = TourGuideForm()
    return render(request, 'guides/tour_guide_register.html', {'form': form})


def thank_you(request):
    guide_first_name = request.session.pop('guide_first_name', '')
    return render(request, 'guides/thank_you.html', {
        'tour_guide_first_name': guide_first_name
    })


def create_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 הסיור נוצר בהצלחה! מעבירים אותך לדף הבית ")
            return redirect('create_tour')  # חזרה לאותו עמוד
    else:
        form = TourForm()
    return render(request, 'guides/create_tour.html', {'form': form})


def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_dashboard')
    else:
        form = TourForm(instance=tour)
    return render(request, 'guides/edit_tour.html', {'form': form, 'tour': tour})

def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tour_dashboard')

def tour_dashboard(request):
    tours = Tour.objects.all().order_by('-tour_date', '-tour_start_time')
    return render(request, 'guides/tour_dashboard.html', {'tours': tours})


def guide_detail(request, guide_id):
    guide = get_object_or_404(TourGuide, id=guide_id)
    return render(request, 'guides/guide_detail.html', {'guide': guide})

