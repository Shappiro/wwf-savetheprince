from math import ceil
from django import template

register = template.Library()

### Molto utile quando devo mettere immagini su più righe: con questo codice posso 
### decidere quanti elementi vanno per riga (chunk)! Es:
### for chunk in elements|as_chunk:3 ...
###     for element in chunk ...
@register.filter
def as_chunks(lst, chunk_size):
    limit = ceil(len(lst) / chunk_size)
    for idx in range(limit):
        yield lst[chunk_size * idx : chunk_size * (idx + 1)]