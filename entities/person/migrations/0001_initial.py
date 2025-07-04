# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 07:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinic', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('joined_on', models.DateTimeField(default=django.utils.timezone.now, help_text='Designates when the user joined the system.', verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='uploads/avatars/')),
                ('gender', models.IntegerField(choices=[(3, 'Unknown'), (2, 'Female'), (1, 'Male')], default=3, verbose_name='gender')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='address')),
                ('phone', models.CharField(max_length=255, unique=True, verbose_name='phone')),
                ('dob', models.DateField(default=datetime.date.today, verbose_name='date of birth')),
                ('verified', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='DoctorSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_time', models.IntegerField(db_index=True, default=10)),
                ('monday', models.TimeField(blank=True, null=True)),
                ('tuesday', models.TimeField(blank=True, null=True)),
                ('wednesday', models.TimeField(blank=True, null=True)),
                ('thursday', models.TimeField(blank=True, null=True)),
                ('friday', models.TimeField(blank=True, null=True)),
                ('saturday', models.TimeField(blank=True, null=True)),
                ('sunday', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='person.User')),
                ('role', models.IntegerField(default=1)),
                ('degree', models.CharField(blank=True, max_length=50, null=True, verbose_name='degree')),
                ('services', models.ManyToManyField(related_name='doctor', to='resources.Service')),
                ('specialization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='resources.Specialization')),
            ],
            options={
                'abstract': False,
            },
            bases=('person.user',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='person.User')),
                ('role', models.IntegerField(default=2)),
                ('height', models.FloatField(blank=True, null=True, verbose_name='height')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='weight')),
                ('marital_status', models.IntegerField(blank=True, choices=[(1, 'MARRIED'), (2, 'SINGLE')], null=True, verbose_name='marital status')),
                ('occupation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='resources.Occupation')),
            ],
            options={
                'abstract': False,
            },
            bases=('person.user',),
        ),
        migrations.AddField(
            model_name='verificationcode',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification_code', to='person.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='clinic.City'),
        ),
        migrations.AddField(
            model_name='user',
            name='clinic',
            field=models.ManyToManyField(blank=True, related_name='user', to='clinic.Clinic'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='clinic.Country'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='doctorsetting',
            name='physician',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='setting', to='person.Doctor'),
        ),
    ]
