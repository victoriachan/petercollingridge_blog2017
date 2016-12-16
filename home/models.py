from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, StreamFieldPanel, InlinePanel, PageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


# A section of content, such as Tutorials to show on the home page
class HomePageSection(models.Model):
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    body = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        PageChooserPanel('link_page'),
        FieldPanel('body'),
    ]

    class Meta:
        abstract = True


# Sections for the home page collected together in an orderable way
class HomePageSections(Orderable, HomePageSection):
    page = ParentalKey('HomePage', related_name='sections')


class HomePage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        InlinePanel('sections', label="Sections"),
    ]

    # Return sections to show on front page
    def get_sections(self):
        return IndexPage.objects.filter(path__startswith=self.path).order_by('path')

    # Get a list of child pages which will be the main sections of the site
    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        # Add extra variables and return the updated context
        context['children'] = IndexPage.objects.child_of(self).live()
        return context


# Non-snippet version of Icon
class IconLink(models.Model):
    name = models.CharField(max_length=255)
    font_awesome_class = models.CharField(max_length=255, blank=True)
    svg = models.CharField(max_length=2048, blank=True)
    url = models.URLField(null=True, blank=True)

    @property
    def image(self):
        if self.font_awesome_class:
            return ('<i class="fa %s fa-4x"></i>' % self.font_awesome_class)
        else:
            return '<i>%s</i>' % self.svg

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('font_awesome_class'),
        FieldPanel('svg'),
    ]

    class Meta:
        abstract = True


# Sections for the home page collected together in an orderable way
class IconLinks(Orderable, IconLink):
    page = ParentalKey('AboutPage', related_name='icons')


class AboutPage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        InlinePanel('icons', label="social icons"),
    ]


# A relative link path (used for CSS and JS)
class LinkFragment(models.Model):
    path = models.CharField(max_length=255, help_text="Relative URL")
    panels = [FieldPanel('path')]

    class Meta:
        abstract = True


class CSSLinkFragments(Orderable, LinkFragment):
    page = ParentalKey('GenericPage', related_name='css_links')


class JSLinkFragments(Orderable, LinkFragment):
    page = ParentalKey('GenericPage', related_name='js_links')



class CodeBlock(blocks.StructBlock):
    code = blocks.TextBlock(required=True)
    language = blocks.CharBlock(required=False)
    line_number = blocks.IntegerBlock(required=False)

    class Meta:
        icon = 'code'
        label = 'Code'
        template = 'home/blocks/code_block.html'


# https://jossingram.wordpress.com/2015/07/30/some-wagtail-v1-streamfield-examples/
class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock()),
    ], icon='arrow-left', label='Left column content')

    right_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock()),
    ], icon='arrow-right', label='Right column content')

    class Meta:
        icon = 'placeholder'
        label = 'Two Columns'
        template = 'home/blocks/two_column_block.html'


# GenericPage uses a Streamfield with a raw HTML block so is relatively flexible
# Used for all leave nodes (tools, tutorial pages, blog posts) other than special pages
class GenericPage(Page):
    date = models.DateField("Post date")

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock()),
        ('two_columns', TwoColumnBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        InlinePanel('css_links', label="CSS links"),
        InlinePanel('js_links', label="JS links"),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(GenericPage, self).get_context(request)
        # Add extra variables and return the updated context
        #context['children'] = IndexPage.objects.live().descendant_of(self)
        context["previous_page"] = self.get_prev_siblings().live().first()
        context["next_page"] = self.get_next_siblings().live().first()
        return context


# A page containing a list of child pages.
class IndexPage(Page):
    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        InlinePanel('featured_content', label="Featured content"),
    ]

    def get_context(self, request):
        context = super(IndexPage, self).get_context(request)
        # Add extra variables and return the updated context
        #context['children'] = IndexPage.objects.live().descendant_of(self)
        context['children'] = GenericPage.objects.child_of(self).live()
        context['index_children'] = IndexPage.objects.child_of(self).live()
        return context

    def get_featured_content(self):
        children = GenericPage.objects.child_of(self).live()
        return [children.get(pk=content.link_page) for content in self.featured_content.all()]


# Link to a featured page within an index
class FeaturedContent(models.Model):
    description = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )

    panels = [
        FieldPanel('description'),
        PageChooserPanel('link_page', page_type=GenericPage),
    ]


# A group of featured content to display on the home page
class FeaturedContentSet(Orderable, FeaturedContent):
    page = ParentalKey('IndexPage', related_name='featured_content')


# Page for prototyping the homepage
class HomePageTest(Page):
    pass
