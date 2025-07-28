from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tours.views import auth_views
from django.views.generic import TemplateView

# Travelers
from tours.views.travelers_views import (
    home, register, payment_redirect, success, registration_list,
    delete_registration, toggle_attendance, participants_list, tour_detail
)

# Guides
from tours.views.guides_views import (
    register_tour_guide, thank_you, create_tour, edit_tour, delete_tour,
    tour_dashboard, guide_detail, all_guides_view,
    guides_list_view, export_guides_excel, email_all_guides,
    tours_by_guide, admin_dashboard  # ✅ נוספה הפונקציה admin_dashboard
)

# Utils
from tours.views.utils_views import (
    checkout_submit,
    download_tour_excel,
)

# API
from tours.views.api_views import (
    update_presence, send_attendance_report, mark_present_by_code, send_reminder_per_tour
)

# Payments
from tours.views.payments_views import (
    checkout_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # דף הבית וטיולים
    path('', home, name='home'),
    path('register/<int:tour_id>/', register, name='register'),
    path('success/<int:traveler_id>/', success, name='success'),
    path('tour/<int:pk>/', tour_detail, name='tour_detail'),
    path('about/', TemplateView.as_view(template_name='management/about_us.html'), name='about_us'),

    # רשומות נרשמים
    path('registrations/', registration_list, name='registration_list'),
    path('delete_registration/<int:registration_id>/', delete_registration, name='delete_registration'),
    path('toggle_attendance/<int:registration_id>/', toggle_attendance, name='toggle_attendance'),
    path('participants/', participants_list, name='participants_list'),

    # ייצוא נרשמים לפי טיול
    path('download-tour-excel/<int:tour_id>/', download_tour_excel, name='download_tour_excel'),

    # API
    path('update_presence/', update_presence, name='update_presence'),
    path('send-attendance-report/', send_attendance_report, name='send_attendance_report'),
    path('mark_present_by_code/', mark_present_by_code, name='mark_present_by_code'),
    path('send-reminder/<int:tour_id>/', send_reminder_per_tour, name='send_reminder_per_tour'),

    # מדריכי טיולים
    path('register-guide/', register_tour_guide, name='register_tour_guide'),
    path('thank-you/', thank_you, name='guide_thank_you'),
    path('create-tour/', create_tour, name='create_tour'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('tour-dashboard/', tour_dashboard, name='tour_dashboard'),
    path('edit-tour/<int:tour_id>/', edit_tour, name='edit_tour'),
    path('delete-tour/<int:tour_id>/', delete_tour, name='delete_tour'),
    path('guide/<int:guide_id>/', guide_detail, name='guide_detail'),
    path('all-guides/', all_guides_view, name='all_guides'),
    path('guides-list/', guides_list_view, name='guides_list'),
    path('export-guides/', export_guides_excel, name='export_guides_excel'),
    path('email-all-guides/', email_all_guides, name='email_all_guides'),
    path('tours/guide/<int:guide_id>/', tours_by_guide, name='tours_by_guide'),

    # תשלום
    path('payment/', payment_redirect, name='payment_redirect'),
    path('checkout/<int:traveler_id>/', checkout_view, name='checkout'),
    path('checkout/<int:traveler_id>/submit/', checkout_submit, name='checkout_submit'),

        # התחברות והתנתקות
    path('login/', auth_views.admin_login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('management/login/', auth_views.admin_login_view, name='admin_login_view'),  # ✅ חדש

    # דשבורד מנהל
    path('management/dashboard/', admin_dashboard, name='admin_dashboard'),  # ✅
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
