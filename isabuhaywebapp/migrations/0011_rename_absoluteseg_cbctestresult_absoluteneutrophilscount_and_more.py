# Generated by Django 4.1.3 on 2022-12-05 03:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('isabuhaywebapp', '0010_payments_date_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cbctestresult',
            old_name='absoluteSeg',
            new_name='absoluteNeutrophilsCount',
        ),
        migrations.RenameField(
            model_name='cbctestresult',
            old_name='segmenters',
            new_name='neutrophils',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='date_created',
        ),
        migrations.AddField(
            model_name='payments',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cbctestresult',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cbctestresultdocx',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cbctestresultimage',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cbctestresultpdf',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payments',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='promooptions',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=1000000)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('read', models.BooleanField(default=False)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='isabuhaywebapp.room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
