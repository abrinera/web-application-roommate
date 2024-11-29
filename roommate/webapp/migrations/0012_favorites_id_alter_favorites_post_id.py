# Generated by Django 5.1.3 on 2024-11-23 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1112222, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favorites',
            name='post_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webapp.post'),
        ),
    ]
