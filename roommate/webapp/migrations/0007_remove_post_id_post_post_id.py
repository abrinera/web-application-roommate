# Generated by Django 5.1.3 on 2024-11-22 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_post_location_alter_post_resident_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='id',
        ),
        migrations.AddField(
            model_name='post',
            name='post_id',
            field=models.CharField(default=114524112024, max_length=20, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
    ]
