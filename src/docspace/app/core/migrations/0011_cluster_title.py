# Generated by Django 3.2.14 on 2022-12-11 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_cluster_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]