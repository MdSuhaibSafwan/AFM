from django import forms
from django.utils import formats
from django.templatetags.static import static
from django.core.files.storage import get_storage_class

class DropzoneWidget(forms.widgets.FileInput):
    template_name = 'forms/widgets/dropzone.html'

    class Media:
        js = ("https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/min/dropzone.min.js",)
        css = {
            'all': ("https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/dropzone.css",)
        }

    def __init__(self, attrs=None, options={}):
        self.options = options
        super().__init__(attrs)

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.
        """
        if value == '' or value is None:
            return None
        if self.is_localized:
            return formats.localize_input(value)

        media_storage = get_storage_class()()
        value = media_storage.url(name=str(value))

        return str(value)

    def absolute_path(self, path):
        """
        Given a relative or absolute path to a static asset, return an absolute
        path. An absolute path will be returned unchanged while a relative path
        will be passed to django.templatetags.static.static().
        """
        if path.startswith(('http://', 'https://', '/')):
            return path
        return static(path)

    def get_context(self, name, value, attrs):
        current_class = attrs.get('class')
        custom_class = 'custom-dropzone-widget-' + name

        if current_class:
            attrs['class'] = current_class + ' ' + custom_class
        else:
            attrs['class'] = custom_class
        context = super(DropzoneWidget, self).get_context(name, value, attrs)
        self.options.update({
            'class': custom_class,
            'paramName': name
        })
        context['options'] = self.options
        return context


class ImageDropzoneWidget(forms.widgets.FileInput):
    template_name = 'forms/widgets/dropzone.html'

    class Media:
        js = ("https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/min/dropzone.min.js",)
        css = {
            'all': ("https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/dropzone.css",)
        }

    def __init__(self, attrs=None, options={}):
        self.options = options

        super().__init__(attrs)

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.
        """
        if value == '' or value is None:
            return None
        if self.is_localized:
            return formats.localize_input(value)

        media_storage = get_storage_class()()
        value = media_storage.url(name=str(value))

        return str(value)

    def absolute_path(self, path):
        """
        Given a relative or absolute path to a static asset, return an absolute
        path. An absolute path will be returned unchanged while a relative path
        will be passed to django.templatetags.static.static().
        """
        if path.startswith(('http://', 'https://', '/')):
            return path
        return static(path)

    def get_context(self, name, value, attrs):
        current_class = attrs.get('class')
        custom_class = 'custom-dropzone-widget-' + name
        if current_class:
            attrs['class'] = current_class + ' ' + custom_class
        else:
            attrs['class'] = custom_class
        context = super(ImageDropzoneWidget, self).get_context(name, value, attrs)

        self.options.update({
            'class': custom_class,
            'paramName': name
        })

        context['options'] = self.options
        return context


class FileDropzoneWidget(forms.widgets.FileInput):
    template_name = 'forms/widgets/dropzone-file.html'

    class Media:
        js = ("https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/min/dropzone.min.js",)
        css = {
            'all': ("https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.2/dropzone.css",)
        }

    def __init__(self, attrs=None, options={}):
        self.options = options

        super().__init__(attrs)

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.
        """
        if value == '' or value is None:
            return None
        if self.is_localized:
            return formats.localize_input(value)
        return str(value)

    def absolute_path(self, path):
        """
        Given a relative or absolute path to a static asset, return an absolute
        path. An absolute path will be returned unchanged while a relative path
        will be passed to django.templatetags.static.static().
        """
        if path.startswith(('http://', 'https://', '/')):
            return path
        return static(path)

    def get_context(self, name, value, attrs):
        current_class = attrs.get('class')
        custom_class = 'custom-dropzone-widget-' + name

        if current_class:
            attrs['class'] = current_class + ' ' + custom_class
        else:
            attrs['class'] = custom_class
        context = super(FileDropzoneWidget, self).get_context(name, value, attrs)

        self.options.update({
            'class': custom_class,
            'paramName': name
        })

        context['options'] = self.options
        return context
