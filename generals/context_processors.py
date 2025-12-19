
from django.conf import settings
from django.urls import reverse
from django.utils import translation

def hreflang_alternates(request):
    """
    A context processor to add hreflang alternate URLs for the current page.
    """
    # Don't run for non-page views like AJAX calls or if there's no URL match
    if not hasattr(request, 'resolver_match') or not request.resolver_match:
        return {}

    # Get the view name and arguments from the matched URL
    view_name = request.resolver_match.view_name
    kwargs = request.resolver_match.kwargs

    alternates = []
    # Get the original language to switch back to it later
    current_language = translation.get_language()

    for lang_code, lang_name in settings.LANGUAGES:
        try:
            # Activate the language to generate its specific URL
            translation.activate(lang_code)
            # Reverse the URL for the activated language
            url = reverse(view_name, kwargs=kwargs)
            # Build the full absolute URL
            absolute_url = request.build_absolute_uri(url)
            alternates.append({
                'lang_code': lang_code,
                'url': absolute_url,
            })
        except Exception:
            # If a URL can't be reversed for a language, just skip it
            continue

    # Switch back to the original language
    translation.activate(current_language)

    # Determine the x-default URL (usually English or your primary language)
    x_default_url = ''
    for alt in alternates:
        if alt['lang_code'] == settings.LANGUAGE_CODE: # settings.LANGUAGE_CODE is your default lang ('en')
            x_default_url = alt['url']
            break
    if not x_default_url and alternates: # Fallback to the first available URL if default isn't found
        x_default_url = alternates[0]['url']

    return {
        'hreflang_alternates': alternates,
        'hreflang_x_default': x_default_url,
    }