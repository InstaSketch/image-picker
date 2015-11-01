# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='key',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
