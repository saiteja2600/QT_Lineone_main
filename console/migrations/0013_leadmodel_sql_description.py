# Generated by Django 5.0.4 on 2024-04-17 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0012_alter_leadmodel_lead_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadmodel',
            name='sql_description',
            field=models.TextField(null=True),
        ),
    ]
