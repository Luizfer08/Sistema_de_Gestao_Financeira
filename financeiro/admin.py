from django.contrib import admin  # importa o sistema de administração do Django

from .models import Categoria, Receita, Despesa  # importa os modelos criados


admin.site.register(Categoria)  # registra a tabela Categoria no painel administrativo

admin.site.register(Receita)  # registra a tabela Receita no painel administrativo

admin.site.register(Despesa)  # registra a tabela Despesa no painel administrativo
