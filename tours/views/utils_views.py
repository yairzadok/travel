# --- ייבוא ספריות ---

import io
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from email.mime.image import MIMEImage
from email.utils import make_msgid

from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404

from tours.models import TravelerRegistration
from tours.utils.excel_utils import export_registrations_excel


# --- 1. אישור תשלום (שליחת מייל פשוט) ---

def checkout_submit(request, traveler_id):
    if request.method == 'POST':
        traveler = get_object_or_404(TravelerRegistration, id=traveler_id)
        user_email = traveler.traveler_email
        tour_name = traveler.tour.tour_title
        amount = round(traveler.tour.tour_price * request.session.get('num_participants', 1), 2)

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

        return redirect('success', traveler_id=traveler.id)


# --- 2. שליחת מייל הרשמה עם QR ותמונה ---

def generate_qr_with_text(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    width, height = qr_img.size
    total_height = height + 50

    new_img = Image.new("RGB", (width, total_height), "white")
    new_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    reversed_text = "אנא הצג קוד זה למדריך"[::-1]
    text_x = (width - draw.textlength(reversed_text, font=font)) // 2
    draw.text((text_x, height + 10), reversed_text, font=font, fill="black")

    qr_io = io.BytesIO()
    new_img.save(qr_io, format='PNG')
    qr_io.seek(0)
    return qr_io


def send_registration_email(registration, tour):
    qr_io = generate_qr_with_text(registration.registration_code)
    qr_cid = make_msgid(domain='example.com')[1:-1]
    tour_image_cid = make_msgid(domain='example.com')[1:-1]

    tour_image_path = os.path.join(settings.MEDIA_ROOT, str(tour.tour_image))
    with open(tour_image_path, 'rb') as img_file:
        tour_image_data = img_file.read()

    location_encoded = tour.google_maps_link.replace(' ', '+') if tour.google_maps_link else ''
    waze_link = f"https://waze.com/ul?q={location_encoded}&navigate=yes"

    context = {
        'first_name': registration.traveler_first_name,
        'last_name': registration.traveler_last_name,
        'tour_title': tour.tour_title,
        'tour_date': tour.tour_date,
        'tour_time': tour.tour_start_time,
        'tour_difficulty': tour.difficulty_level,
        'tour_equipment': ', '.join(tour.required_equipment or []),
        'registration_code': registration.registration_code,
        'qr_cid': qr_cid,
        'tour_image_cid': tour_image_cid,
        'waze_link': waze_link,
        'guide_name': (
            f"{tour.tour_guide_name.tour_guide_first_name} {tour.tour_guide_name.tour_guide_last_name}"
            if tour.tour_guide_name else ''
        ),
        'guide_phone': tour.tour_guide_name.tour_guide_phone if tour.tour_guide_name else '',
    }

    subject = 'אישור הרשמה לסיור'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = registration.traveler_email

    text_content = (
        f"שלום {registration.traveler_first_name}, "
        f"תודה על ההרשמה לטיול {tour.tour_title}. "
        f"קוד רישום: {registration.registration_code}"
    )

    html_content = render_to_string('emails/registration_email_template.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    tour_img = MIMEImage(tour_image_data)
    tour_img.add_header('Content-ID', f'<{tour_image_cid}>')
    msg.attach(tour_img)

    qr_image = MIMEImage(qr_io.read(), _subtype="png")
    qr_image.add_header('Content-ID', f'<{qr_cid}>')
    msg.attach(qr_image)

    msg.send(fail_silently=True)


# --- 3. הורדת קובץ Excel לפי מזהה טיול ---

def download_tour_excel(request, tour_id):
    return export_registrations_excel(tour_id)
