# Generated by Django 5.0 on 2024-02-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'مرد'), ('F', 'زن')], max_length=1, verbose_name='جنسیت'),
        ),
    ]
