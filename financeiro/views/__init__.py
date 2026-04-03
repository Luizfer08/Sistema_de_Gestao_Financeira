from .dashboard_view import dashboard
from .receita_view import *
from .despesas_view import *
from .categorias_view import *
from .auth_view import login_view, logout_view, api_login, cadastro_view, api_cadastro


# RECEITAS
from .receita_view import (
    listar_receitas,
    criar_receita_view,
    editar_receita,
    excluir_receita,
)

# DESPESAS
from .despesas_view import (
    listar_despesas,
    criar_despesa,
    editar_despesa,
    excluir_despesa,
)

# CATEGORIAS
from .categorias_view import (
    listar_categorias,
    criar_categoria,
    editar_categoria,
    excluir_categoria,
)

# AUTENTICAÇÃO
from .auth_view import (
    login_view,
    logout_view,
    cadastro_view,
    api_login,
    api_cadastro,
    home_view,
)
