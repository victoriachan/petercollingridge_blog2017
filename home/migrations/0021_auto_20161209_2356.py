# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-09 23:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('home', '0020_auto_20161209_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='IconLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(max_length=255)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='aboutpage',
            name='social_icon',
        ),
        migrations.AddField(
            model_name='iconlinks',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='icons', to='home.AboutPage'),
        ),
    ]
