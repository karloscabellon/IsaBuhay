# Generated by Django 4.1.2 on 2022-10-14 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=25, unique=True, verbose_name="username"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=50, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "firstname",
                    models.CharField(max_length=20, verbose_name="first name"),
                ),
                ("lastname", models.CharField(max_length=20, verbose_name="last name")),
                (
                    "phone_number",
                    models.CharField(max_length=15, verbose_name="phone number"),
                ),
                (
                    "birthdate",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="birthdate"
                    ),
                ),
                (
                    "blood_type",
                    models.CharField(
                        blank=True, max_length=5, null=True, verbose_name="blood type"
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="height"
                    ),
                ),
                (
                    "weight",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="weight"
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="CBCTestResultDocx",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("testDocx", models.FileField(upload_to="docs/")),
            ],
        ),
        migrations.CreateModel(
            name="CBCTestResultImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("testImage", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.CreateModel(
            name="CBCTestResultPDF",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("testPDF", models.FileField(upload_to="pdfs/")),
            ],
        ),
        migrations.CreateModel(
            name="CBCTestResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("source", models.CharField(max_length=50)),
                ("labNumber", models.CharField(max_length=50)),
                ("pid", models.CharField(max_length=50)),
                ("dateRequested", models.DateTimeField()),
                ("dateReceived", models.DateTimeField()),
                ("whiteBloodCells", models.FloatField()),
                ("redBloodCells", models.FloatField()),
                ("hemoglobin", models.FloatField()),
                ("hematocrit", models.FloatField()),
                ("meanCorpuscularVolume", models.FloatField()),
                ("meanCorpuscularHb", models.FloatField()),
                ("meanCorpuscularHbConc", models.FloatField()),
                ("rbcDistributionWidth", models.FloatField()),
                ("plateletCount", models.FloatField()),
                ("segmenters", models.FloatField()),
                ("lymphocytes", models.FloatField()),
                ("monocytes", models.FloatField()),
                ("eosinophils", models.FloatField()),
                ("basophils", models.FloatField()),
                ("bands", models.FloatField()),
                ("absoluteSeg", models.FloatField()),
                ("absoluteLymphocyteCount", models.FloatField()),
                ("absoluteMonocyteCount", models.FloatField()),
                ("absoluteEosinophilCount", models.FloatField()),
                ("absoluteBasophilCount", models.FloatField()),
                ("absoluteBandCount", models.FloatField()),
                (
                    "testDocx",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="isabuhaywebapp.cbctestresultdocx",
                    ),
                ),
                (
                    "testImage",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="isabuhaywebapp.cbctestresultimage",
                    ),
                ),
                (
                    "testPDF",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="isabuhaywebapp.cbctestresultpdf",
                    ),
                ),
            ],
        ),
    ]
