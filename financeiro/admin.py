# Importa o painel administrativo padrao do Django.
from django.contrib import admin

# Importa os models que devem aparecer no admin.
from .models import AceiteTermos, Categoria, Receita, Despesa


# Disponibiliza as categorias no painel administrativo.
admin.site.register(Categoria)

# Disponibiliza as receitas no painel administrativo.
admin.site.register(Receita)

# Disponibiliza as despesas no painel administrativo.
admin.site.register(Despesa)

# Disponibiliza os aceites dos termos no painel administrativo.
admin.site.register(AceiteTermos)
