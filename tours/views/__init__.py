from .travelers_views import (
    home,
    register,
    payment_redirect,
    success,
    registration_list,
    delete_registration,
    toggle_attendance,
    participants_list,
    tour_detail,
)

from .guides_views import (
    register_tour_guide,
    thank_you,
    create_tour,
    edit_tour,
    delete_tour,
    tour_dashboard,
    guide_detail,
    all_guides_view,
)

from .utils_views import (
    export_registrations_excel,
    generate_qr_with_text,
)

from .api_views import (
    update_presence,
    send_attendance_report,
    mark_present_by_code,
    send_reminder_per_tour,
)
