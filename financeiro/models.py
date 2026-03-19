from django.db import models  # importa o módulo de modelos do Django, usado para criar tabelas no banco de dados

from django.contrib.auth.models import User  # importa o modelo de usuário padrão do Django para relacionar os dados financeiros ao usuário logado


class Categoria(models.Model):  # cria a tabela Categoria no banco de dados

    nome = models.CharField(max_length=100)  # campo de texto que armazena o nome da categoria (ex: alimentação, salário)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    # cria um relacionamento com o usuário
    # cada categoria pertence a um usuário específico
    # CASCADE significa que se o usuário for deletado, as categorias dele também serão

    def __str__(self):  # define como o nome da categoria será exibido no sistema
        return self.nome


class Receita(models.Model):  # cria a tabela de receitas (dinheiro que entra)

    descricao = models.CharField(max_length=200)  
    # campo de texto para descrever a receita (ex: salário, freelances)

    valor = models.DecimalField(max_digits=10, decimal_places=2)  
    # armazena valores monetários com até 10 dígitos e 2 casas decimais

    data = models.DateField()  
    # armazena a data da receita

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  
    # relacionamento com categoria para classificar a receita

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    # relaciona a receita ao usuário que cadastrou

    def __str__(self):
        return self.descricao


class Despesa(models.Model):  # cria a tabela de despesas (dinheiro que sai)

    descricao = models.CharField(max_length=200)  
    # descrição da despesa (ex: mercado, gasolina)

    valor = models.DecimalField(max_digits=10, decimal_places=2)  
    # campo monetário para o valor gasto

    data = models.DateField()  
    # data em que a despesa ocorreu

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  
    # categoria associada à despesa

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    # usuário responsável por essa despesa

    def __str__(self):
        return self.descricao
