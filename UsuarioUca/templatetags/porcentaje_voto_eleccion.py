from django import template

register = template.Library()

@register.filter()
def porcentaje_voto_eleccion(votos, total):
    return (votos/total) * 100
