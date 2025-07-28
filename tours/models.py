from django.db import models  # חובה תמיד בתחילת הקובץ
import random
from multiselectfield import MultiSelectField


class TourGuide(models.Model):
    tour_guide_first_name = models.CharField("שם פרטי", max_length=100)
    tour_guide_last_name = models.CharField("שם משפחה", max_length=100)
    tour_guide_phone = models.CharField("טלפון נייד", max_length=20)
    tour_guide_email = models.EmailField("כתובת מייל")
    tour_guide_profile_picture = models.ImageField("תמונת פרופיל", upload_to="guide_profiles/", blank=True, null=True)
    languages = models.CharField("שפות הדרכה", max_length=255, blank=True, null=True)
    specialties = models.CharField("תחומי התמחות", max_length=255, blank=True, null=True)
    experience = models.TextField("ניסיון מקצועי", blank=True, null=True)
    recommendations = models.TextField("המלצות או קישורים", blank=True, null=True)

    facebook_link = models.URLField("קישור לדף פייסבוק", blank=True, null=True,
                                    help_text="הזן קישור לעמוד הפייסבוק שלך")

    instagram_link = models.URLField("קישור לדף אינסטגרם", blank=True, null=True,
                                     help_text="הזן קישור לעמוד האינסטגרם שלך")
    whatsapp_link = models.URLField("קישור לוואטסאפ", blank=True, null=True)
    website_link = models.URLField("אתר אינטרנט", blank=True, null=True)


    def __str__(self):
        return f"{self.tour_guide_first_name} {self.tour_guide_last_name}"


class TravelerRegistration(models.Model):
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE, related_name='registrations', db_column='סיור')
    traveler_first_name = models.CharField(max_length=255, db_column='שם_פרטי')
    traveler_last_name = models.CharField(max_length=255, db_column='שם_משפחה')
    registration_code = models.CharField("קוד רישום", max_length=6, blank=True, null=True)
    traveler_phone = models.CharField(max_length=20)
    traveler_email = models.EmailField(db_column='אימייל')
    traveler_attendance = models.BooleanField(default=False, db_column='נוכחות')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.traveler_first_name} {self.traveler_last_name}"

class Tour(models.Model):
    tour_title = models.CharField("כותרת ראשית", max_length=255)
    tour_subtitle = models.CharField("כותרת משנית", max_length=255, db_column='כותרת_משנית')

    tour_image = models.ImageField("תמונה הראשית", upload_to='tours_images/', db_column='תמונה ')

    tour_date = models.DateField("תאריך הסיור", db_column='תאריך')
    tour_description = models.CharField("פרטי הטיול", blank=True, null=True, db_column='פרטי_הטיול')

    tour_start_time = models.TimeField("שעת התחלה", db_column='שעת_התחלה')
    tour_end_time = models.TimeField("שעת סיום משוערת", blank=True, null=True)

    meeting_point = models.CharField("מקום מפגש", max_length=255, db_column='מקום_המפגש')

    google_maps_link = models.CharField("קישור לנקודת המפגש במפת גוגל", max_length=500, blank=True, db_column='קישור_למפות_גוגל')

    tour_guide_name = models.ForeignKey(
        "TourGuide",
        verbose_name="שם המדריך",
        on_delete=models.CASCADE,
        related_name="tours",
        blank=True,
        null=True,
        db_column="שם_מדריך"
    )

    tour_price = models.DecimalField(
        "עלות הסיור",
        max_digits=8,
        decimal_places=2,
        help_text="יש להזין את העלות בשקלים חדשים (₪)",
        null=True,
        db_column='עלות'
    )

    target_audience = MultiSelectField(
        "קהל יעד",
        choices=[
            ("משפחות", "משפחות"),
            ("מבוגרים", "מבוגרים"),
            ("מיטבי לכת", "מיטבי לכת"),
            ("מיטיבי קשב", "מיטיבי קשב"),
        ],
        max_length=100,
        blank=True,
        null=True,
        db_column='קהל_יעד',
        help_text="ניתן לבחור יותר מאפשרות אחת על ידי לחיצה על Ctrl או Command"
    )

    difficulty_level = models.CharField(
        "רמת קושי",
        max_length=20,
        choices=[
            ("קל", "קל"),
            ("בינוני", "בינוני"),
            ("קשה", "קשה"),
            ("קשה מאוד", "קשה מאוד"),
        ],
        blank=True,
        null=True,
        db_column='רמת_קושי'
    )

    required_equipment = MultiSelectField(
        "ציוד נדרש",
        choices=[
            ("כובע", "כובע"),
            ("מים", "מים"),
            ("נעליים סגורות", "נעליים סגורות"),
            ("קרם הגנה", "קרם הגנה"),
            ("אחר", "אחר"),
        ],
        max_length=255,
        blank=True,
        null=True,
        db_column='ציוד_נדרש',
        help_text="ניתן לבחור יותר מפריט אחד על ידי לחיצה על Ctrl או Command"
    )

    max_participants = models.PositiveIntegerField(
        "מקסימום משתתפים",
        default=30,
        db_column='מקסימום_משתתפים'
    )

    def is_full(self):
        return self.registrations.count() >= self.max_participants

    def __str__(self):
        return self.tour_title
