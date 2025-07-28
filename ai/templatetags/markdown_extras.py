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
