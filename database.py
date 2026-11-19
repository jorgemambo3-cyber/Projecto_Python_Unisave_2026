"""Camada de acesso à base de dados SQLite (armazenamento local leve)."""
import os
import sqlite3

from excecoes import ErroBaseDados


class Database:
    """Encapsula todas as operações SQLite. Abre uma ligação por operação
    (seguro para o servidor web, que usa várias threads)."""

    ESQUEMA = """
    CREATE TABLE IF NOT EXISTS utilizadores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
        telefone TEXT NOT NULL, idade INTEGER NOT NULL, senha_hash TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS bolsas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE, descricao TEXT, url TEXT NOT NULL, origem TEXT DEFAULT 'base');
    CREATE TABLE IF NOT EXISTS pedidos_mentoria(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilizador_id INTEGER NOT NULL, tipo TEXT NOT NULL, mensagem TEXT,
        FOREIGN KEY(utilizador_id) REFERENCES utilizadores(id));
    """

    def __init__(self, caminho):
        self.caminho = caminho
        pasta = os.path.dirname(os.path.abspath(caminho))
        os.makedirs(pasta, exist_ok=True)
        self.inicializar()

    def _ligar(self):
        try:
            ligacao = sqlite3.connect(self.caminho, timeout=10)
            ligacao.row_factory = sqlite3.Row
            return ligacao
        except sqlite3.Error as e:
            raise ErroBaseDados(f"Não foi possível abrir a base de dados: {e}") from e

    def inicializar(self):
        self.executar_script(self.ESQUEMA)

    def executar_script(self, sql):
        ligacao = self._ligar()
        try:
            with ligacao:
                ligacao.executescript(sql)
        except sqlite3.Error as e:
            raise ErroBaseDados(str(e)) from e
        finally:
            ligacao.close()

    def executar(self, sql, params=()):
        """INSERT/UPDATE/DELETE. Devolve o id da última linha inserida."""
        ligacao = self._ligar()
        try:
            with ligacao:
                return ligacao.execute(sql, params).lastrowid
        except sqlite3.IntegrityError:
            raise
        except sqlite3.Error as e:
            raise ErroBaseDados(str(e)) from e
        finally:
            ligacao.close()

    def consultar(self, sql, params=()):
        """SELECT. Devolve lista de dicionários."""
        ligacao = self._ligar()
        try:
            return [dict(r) for r in ligacao.execute(sql, params).fetchall()]
        except sqlite3.Error as e:
            raise ErroBaseDados(str(e)) from e
        finally:
            ligacao.close()
