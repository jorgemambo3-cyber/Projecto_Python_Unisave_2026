"""Excepções personalizadas do CDFJ-Opportunity."""


class ErroCDFJ(Exception):
    """Erro base da aplicação."""


class ErroValidacao(ErroCDFJ):
    """Dados inválidos introduzidos pelo utilizador."""


class ErroAutenticacao(ErroCDFJ):
    """E-mail ou senha incorrectos."""


class ErroBaseDados(ErroCDFJ):
    """Falha ao aceder à base de dados SQLite."""
