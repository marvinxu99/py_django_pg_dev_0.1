# Generated by Django 3.0.3 on 2020-03-03 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200302_2232'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CodeValue',
            new_name='Code_Value',
        ),
        migrations.RenameModel(
            old_name='PersonAlias',
            new_name='Person_Alias',
        ),
    ]
