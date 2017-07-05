# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-13 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilityRestriction',
            fields=[
                ('cd', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dmd_lookup_availability_restriction',
            },
        ),
        migrations.CreateModel(
            name='ControlledDrugCategory',
            fields=[
                ('cd', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dmd_lookup_control_drug_category',
            },
        ),
        migrations.CreateModel(
            name='DMDProduct',
            fields=[
                ('dmdid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('bnf_code', models.CharField(db_index=True, max_length=15, null=True)),
                ('vpid', models.BigIntegerField(db_index=True, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('full_name', models.TextField()),
                ('ema', models.CharField(max_length=15, null=True)),
                ('concept_class', models.IntegerField(db_index=True)),
                ('product_type', models.IntegerField()),
                ('is_in_nurse_formulary', models.BooleanField(db_column='nurse_f')),
                ('is_in_dentist_formulary', models.BooleanField(db_column='dent_f')),
                ('product_order_no', models.TextField(db_column='prod_order_no', null=True)),
                ('is_blacklisted', models.BooleanField(db_column='sched_1')),
                ('is_schedule_2', models.BooleanField(db_column='sched_2')),
                ('can_have_personal_administration_fee', models.BooleanField(db_column='padm')),
                ('is_fp10', models.BooleanField(db_column='fp10_mda')),
                ('is_borderline_substance', models.BooleanField(db_column='acbs')),
                ('has_assorted_flavours', models.BooleanField(db_column='assort_flav')),
                ('is_imported', models.BooleanField(db_column='flag_imported')),
                ('is_broken_bulk', models.BooleanField(db_column='flag_broken_bulk')),
                ('is_non_bioequivalent', models.BooleanField(db_column='flag_non_bioequivalence')),
                ('is_special_container', models.BooleanField(db_column='flag_special_containers')),
                ('availability_restrictions', models.ForeignKey(db_column='avail_restrictcd', on_delete=django.db.models.deletion.CASCADE, to='dmd.AvailabilityRestriction')),
                ('controlled_drug_category', models.ForeignKey(db_column='catcd', on_delete=django.db.models.deletion.CASCADE, to='dmd.ControlledDrugCategory')),
            ],
            options={
                'db_table': 'dmd_product',
            },
        ),
        migrations.CreateModel(
            name='Prescribability',
            fields=[
                ('cd', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dmd_lookup_virtual_product_pres_status',
            },
        ),
        migrations.CreateModel(
            name='TariffCategory',
            fields=[
                ('cd', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dmd_lookup_dt_payment_category',
            },
        ),
        migrations.CreateModel(
            name='VMPNonAvailability',
            fields=[
                ('cd', models.IntegerField(primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dmd_lookup_virtual_product_non_avail',
            },
        ),
        migrations.AddField(
            model_name='dmdproduct',
            name='prescribability',
            field=models.ForeignKey(db_column='pres_statcd', on_delete=django.db.models.deletion.CASCADE, to='dmd.Prescribability'),
        ),
        migrations.AddField(
            model_name='dmdproduct',
            name='tariff_category',
            field=models.ForeignKey(db_column='tariff_category', on_delete=django.db.models.deletion.CASCADE, to='dmd.TariffCategory'),
        ),
        migrations.AddField(
            model_name='dmdproduct',
            name='vmp_non_availability',
            field=models.ForeignKey(db_column='non_availcd', on_delete=django.db.models.deletion.CASCADE, to='dmd.VMPNonAvailability'),
        ),
    ]