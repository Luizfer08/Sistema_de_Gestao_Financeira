# AppConfig registra as configuracoes do aplicativo financeiro no Django.
from django.apps import AppConfig


# Configuracao principal do app financeiro.
class FinanceiroConfig(AppConfig):

    # Nome usado pelo Django para localizar o aplicativo.
    name = 'financeiro'
