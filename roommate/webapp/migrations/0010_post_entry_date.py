# Generated by Django 5.1.3 on 2024-11-22 21:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_alter_post_bed_alter_post_furnished_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='entry_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]