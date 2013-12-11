from django.conf import settings

def i18n(request):
    from django.utils import translation
    def get_language_code():
        base_code = translation.get_language()
        sub_codes = base_code.split('-')
        sub_codes[1] = sub_codes[1].upper()
        return "_".join(sub_codes)

    context_extras = {}
    context_extras['LANG'] = get_language_code()
    return context_extras