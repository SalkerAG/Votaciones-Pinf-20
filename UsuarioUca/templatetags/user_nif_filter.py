from django import template

register = template.Library()

@register.filter()
def user_nif_filter(nif):
    nifReplace = nif.replace("u", "")
    return nifReplace
