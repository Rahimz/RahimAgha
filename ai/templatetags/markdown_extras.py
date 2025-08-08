import markdown
from django import template

register = template.Library()

@register.filter(name='markdown')
def markdown_to_html(text):
    extensions = [
        'fenced_code',
        'codehilite',  # Requires Pygments CSS
        'extra',
    ]
    extension_configs = {
        'codehilite': {
            'use_pygments': True,
            'css_class': 'codehilite',
            'guess_lang': True,      # Try to guess language if not specified
            'linenums': False,      # Disable line numbers
        }
    }
    return markdown.markdown(text, extensions=extensions, extension_configs=extension_configs)

@register.filter(name='escape_django_tags')
def escape_django_tags(text):
    if text:
        # text = text.replace("{%", "&#123;%")  # Replace "{%" with a safe equivalent
        # text = text.replace("%}", "%&#125;")  # Replace "%}" with a safe equivalent
        # text = text.replace("{{", "&#123;&#123;")  # Replace "{{" with a safe equivalent
        # text = text.replace("}}", "&#125;&#125;")  # Replace "}}" with a safe equivalent
        text = text.replace("{%", "**")  # Replace "{%" with a safe equivalent
        text = text.replace("%}", "**")  # Replace "%}" with a safe equivalent
        text = text.replace("{{", "**")  # Replace "{{" with a safe equivalent
        text = text.replace("}}", "**")  # Replace "}}" with a safe equivalent
    return text
