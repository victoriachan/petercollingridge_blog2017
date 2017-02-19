# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 22:51
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='introduction',
        ),
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('featured_pages', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock(label='featured_page')))], default=''),
            preserve_default=False,
        ),
    ]