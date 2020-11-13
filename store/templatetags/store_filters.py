from django import template

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
