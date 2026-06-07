# Evita que o test discovery importe esta pasta como "models".
# Os models so devem ser carregados pelo caminho correto: "financeiro.models".
if __name__ != 'models':

    from .receita import Receita
    from .despesa import Despesa
    from .categoria import Categoria
    from .aceite_termos import AceiteTermos
