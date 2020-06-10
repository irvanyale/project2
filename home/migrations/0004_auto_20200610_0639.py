# Generated by Django 3.0.4 on 2020-06-09 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_databias_datatraining'),
    ]

    operations = [
        migrations.CreateModel(
            name='HasilTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(blank=True, max_length=50, null=True, verbose_name='No')),
                ('level', models.CharField(blank=True, max_length=50, null=True, verbose_name='Level')),
                ('n_ch4', models.CharField(blank=True, max_length=50, null=True, verbose_name='%CH4')),
                ('n_c2h4', models.CharField(blank=True, max_length=50, null=True, verbose_name='%C2H4')),
                ('n_c2h2', models.CharField(blank=True, max_length=50, null=True, verbose_name='%C2H2')),
                ('fault', models.CharField(blank=True, max_length=50, null=True, verbose_name='Fault')),
                ('kelas', models.CharField(blank=True, max_length=50, null=True, verbose_name='Kelas')),
                ('alpha', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alpha')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
        ),
        migrations.DeleteModel(
            name='DataTraining',
        ),
    ]