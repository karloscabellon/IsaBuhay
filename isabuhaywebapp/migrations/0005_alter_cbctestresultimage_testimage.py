# Generated by Django 4.1.2 on 2022-10-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isabuhaywebapp', '0004_alter_cbctestresult_datereceived_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cbctestresultimage',
            name='testImage',
            field=models.ImageField(upload_to='D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay\\images\\'),
        ),
    ]
