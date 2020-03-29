# Generated by Django 3.0.4 on 2020-03-29 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person_alias',
            name='active_ind',
        ),
        migrations.AddField(
            model_name='person_alias',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='person_alias',
            name='active_status_cd',
            field=models.IntegerField(default=1, verbose_name='Ative Status'),
        ),
        migrations.AlterField(
            model_name='person_alias',
            name='alias',
            field=models.CharField(default='abc', max_length=200, verbose_name='Alias'),
        ),
        migrations.AlterField(
            model_name='person_alias',
            name='alias_expiry_dt_tm',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Alias Expiry Date'),
        ),
        migrations.AlterField(
            model_name='person_alias',
            name='alias_pool_cd',
            field=models.IntegerField(default=1, verbose_name='Alias Type'),
        ),
        migrations.AlterField(
            model_name='person_alias',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Person'),
        ),
    ]
