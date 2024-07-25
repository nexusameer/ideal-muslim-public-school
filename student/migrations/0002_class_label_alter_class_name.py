# Generated by Django 4.2.5 on 2023-11-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='label',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]