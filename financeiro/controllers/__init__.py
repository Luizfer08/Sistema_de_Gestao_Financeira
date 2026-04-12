from .auth_controller import (
    home_view,
    login_view,
    logout_view,
    cadastro_view,
    api_login,
    api_cadastro,
)

from .dashboard_controller import (
    dashboard,
    dashboard_dados,
)

from .receitas_controller import (
    listar_receitas_view,
    criar_receita_view,
    editar_receita_view,
    excluir_receita_view,
)

from .despesas_controller import (
    listar_despesas_view,
    criar_despesa_view,
    editar_despesa_view,
    excluir_despesa_view,
)

from .categorias_controller import (
    listar_categorias_view,
    criar_categoria_view,
    editar_categoria_view,
    excluir_categoria_view,
)