# Generated by Django 3.1.4 on 2021-01-06 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package_Installer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pkg_name', models.CharField(max_length=200)),
                ('pkg_url', models.CharField(max_length=200)),
                ('pkg_summary', models.CharField(max_length=200)),
                ('installer_name', models.CharField(max_length=200)),
                ('installer_url', models.CharField(max_length=200)),
                ('anaconda_ver', models.CharField(max_length=200)),
                ('python_ver', models.CharField(max_length=200)),
                ('pkg_ver', models.CharField(max_length=200)),
                ('pkg_included', models.BooleanField()),
            ],
        ),
    ]