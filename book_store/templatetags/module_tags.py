from django import template

register = template.Library()

@register.filter
def mines_two_number(first, second):
    return first - second

@register.filter
def create_list(number):   
    return [number] * number

@register.filter
def multiply_two_number(first, second):   
    return first * second
     