# Generated by Django 4.1.3 on 2022-12-10 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isabuhaywebapp', '0013_rename_promooptions_promo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payments',
            new_name='Payment',
        ),
    ]
