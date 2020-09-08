# Generated by Django 3.0.5 on 2020-09-08 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20200822_1458'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='stock',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.CreateModel(
            name='DispenseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('dispense', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('author_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Drug')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Patient')),
            ],
            options={
                'verbose_name_plural': 'dispense history',
                'ordering': ['written_datetime'],
            },
        ),
    ]
