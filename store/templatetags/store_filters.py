from django import template

from creditcards import types

import datetime

from store.models import OrderedBook

register = template.Library()

@register.filter(name='get_authors_as_string')
def get_authors_as_string(book):
    authors = ''
    for author in book.authors.all():
        authors += str(author) + ', '
    return authors[:-2]

@register.filter(name='shorten')
def shorten(summary):
    if len(summary) > 250:
        return summary[:250] + '...'

@register.filter(name='get_genres_as_string')
def get_genres_as_string(book):
    genres = ''
    for genre in book.genres.all():
        genres += str(genre) + ', '
    return genres[:-2]

# ALL THE FUNCTIONS BELOW SHOULD BE IMPLEMENTED IN DB WHEN SHOPPING CART MODEL IS CREATED
@register.filter(name='selling_price_sum')
def selling_price_sum(items):
    sum = 0
    for item in items:
        sum += item.selling_price
    return sum

@register.filter(name="get_selling_price_taxes")
def get_selling_price_taxes(items):
    return round(.07 * selling_price_sum(items), 2)


@register.filter(name="get_total_price")
def get_total_price(items):
    return round(get_selling_price_taxes(items) + selling_price_sum(items), 2)

@register.filter(name="get_status_name")
def get_status_name(code):
    if code == "A":
        return "Active"
    if code == "I":
        return "Inactive"
    if code == "S":
        return "Suspended"

@register.filter(name="get_date")
def get_date(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
    return f'{date.strftime("%B %d, %Y, %H:%M:%S")}'

@register.filter(name="cc_string")
def cc_string(payment):
    card_type = types.get_type(payment.cc_number)
    for card in types.CC_TYPES:
        if card_type == card[0]:
            card_type = card[1]['title']
            break
    return f'{card_type} ending in {payment.get_ending()}'

@register.filter(name="promo_discount")
def promo_discount(promo, total):
    new_total = 0
    if not promo: return total
    if promo.discount_type == 'P':
        new_total = float(total) * (1 - promo.discount_amount * .01)
    else:
        new_total = float(total) - promo.discount_amount

    if new_total < 0:
        new_total = 0

    return "{:.2f}".format(new_total)

@register.filter(name="get_items")
def get_items(order):
    return OrderedBook.objects.filter(order=order)

@register.filter(name="money")
def get_items(num):
    return "{:.2f}".format(float(num))
