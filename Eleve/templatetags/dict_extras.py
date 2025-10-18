from django import template

register = template.Library()

@register.filter
def get_value(dictionnaire, cle):
    """Permet d'accéder à dictionnaire[cle] dans un template."""
    if isinstance(dictionnaire, dict):
        return dictionnaire.get(str(cle), None)
    return None