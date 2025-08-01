# Generated by Django 5.2 on 2025-06-03 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0002_remove_tour_difficulty_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='difficulty_level',
            field=models.CharField(blank=True, choices=[('קל', 'קל'), ('בינוני', 'בינוני'), ('קשה', 'קשה'), ('קשה מאוד', 'קשה מאוד')], db_column='רמת_קושי', max_length=20, null=True, verbose_name='רמת קושי'),
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_description',
            field=models.CharField(blank=True, db_column='פרטי_הטיול', null=True, verbose_name='פרטי הטיול'),
        ),
    ]
