"""Modelos (POO) e serviços de negócio do CDFJ-Opportunity."""
import re
import sqlite3
import urllib.parse
import urllib.request
from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash

from excecoes import ErroAutenticacao, ErroBaseDados, ErroValidacao

IDADE_MIN, IDADE_MAX = 18, 35

BOLSAS_INICIAIS = [
    ("Chevening (Reino Unido)", "Mestrado no Reino Unido", "https://www.chevening.org"),
    ("Fulbright (EUA)", "Mestrado e investigação nos EUA", "https://foreign.fulbrightonline.org"),
    ("Erasmus+ (Europa)", "Mobilidade e mestrados na Europa", "https://erasmus-plus.ec.europa.eu"),
    ("DAAD (Alemanha)", "Bolsas para estudar na Alemanha", "https://www.daad.de/en/"),
    ("Commonwealth Scholarships", "Mestrado e doutoramento no Reino Unido", "https://cscuk.fcdo.gov.uk"),
    ("Campus France", "Estudar em França", "https://www.campusfrance.org"),
    ("Mastercard Foundation Scholars", "Bolsas para jovens africanos", "https://mastercardfdn.org/all/scholars/"),
    ("Campus China (CSC)", "Bolsa do governo chinês", "https://www.campuschina.org"),
    ("Turkiye Burslari", "Bolsas do governo da Turquia", "https://turkiyeburslari.gov.tr"),
    ("MEXT (Japão)", "Bolsas do governo japonês", "https://www.studyinjapan.go.jp"),
    ("Stipendium Hungaricum", "Bolsas na Hungria", "https://stipendiumhungaricum.hu"),
    ("Instituto Camões", "Bolsas para países de língua portuguesa", "https://www.instituto-camoes.pt"),
    ("Gates Cambridge", "Pós-graduação em Cambridge", "https://www.gatescambridge.org"),
    ("DGES (Portugal)", "Ensino superior em Portugal", "https://www.dges.gov.pt"),
]

TIPOS_MENTORIA = {
    "Mentoria de candidatura": "Carta de motivação, CV e preparação de entrevista",
    "Apoio documental": "Certificados, tradução, passaporte e visto",
    "Orientação de percurso": "Escolher curso, país e bolsa certa",
}


@dataclass
class Utilizador:
    id: int
    nome: str
    email: str
    telefone: str
    idade: int


@dataclass
class Bolsa:
    id: int
    nome: str
    descricao: str
    url: str
    origem: str = "base"


class Validador:
    """Validações dos dados do cadastro."""

    @staticmethod
    def nome(valor):
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ErroValidacao("O nome deve ter pelo menos 3 caracteres.")
        return valor

    @staticmethod
    def email(valor):
        valor = (valor or "").strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ErroValidacao("E-mail inválido.")
        return valor

    @staticmethod
    def telefone(valor):
        limpo = re.sub(r"[\s\-()]", "", valor or "")
        if not re.fullmatch(r"\+?\d{9,15}", limpo):
            raise ErroValidacao("Número de telefone inválido (9 a 15 dígitos).")
        return limpo

    @staticmethod
    def idade(valor):
        try:
            idade = int(valor)
        except (TypeError, ValueError):
            raise ErroValidacao("Idade inválida.")
        if not IDADE_MIN <= idade <= IDADE_MAX:
            raise ErroValidacao(f"O portal é para jovens dos {IDADE_MIN} aos {IDADE_MAX} anos.")
        return idade

    @staticmethod
    def senha(valor):
        if not valor or len(valor) < 6:
            raise ErroValidacao("A senha deve ter pelo menos 6 caracteres.")
        return valor


class ServicoUtilizadores:
    def __init__(self, db):
        self.db = db

    def registar(self, nome, email, telefone, idade, senha):
        dados = (Validador.nome(nome), Validador.email(email), Validador.telefone(telefone),
                 Validador.idade(idade), generate_password_hash(Validador.senha(senha)))
        try:
            uid = self.db.executar(
                "INSERT INTO utilizadores(nome,email,telefone,idade,senha_hash) VALUES(?,?,?,?,?)", dados)
        except sqlite3.IntegrityError:
            raise ErroValidacao("Este e-mail já está registado.")
        return Utilizador(uid, dados[0], dados[1], dados[2], dados[3])

    def autenticar(self, email, senha):
        linhas = self.db.consultar("SELECT * FROM utilizadores WHERE email=?",
                                   ((email or "").strip().lower(),))
        if not linhas or not check_password_hash(linhas[0]["senha_hash"], senha or ""):
            raise ErroAutenticacao("E-mail ou senha incorrectos.")
        u = linhas[0]
        return Utilizador(u["id"], u["nome"], u["email"], u["telefone"], u["idade"])


class ServicoBolsas:
    def __init__(self, db):
        self.db = db
        self.semear()

    def semear(self):
        """Insere as bolsas iniciais (ignora as que já existem)."""
        for nome, descricao, url in BOLSAS_INICIAIS:
            try:
                self.db.executar("INSERT INTO bolsas(nome,descricao,url) VALUES(?,?,?)", (nome, descricao, url))
            except sqlite3.IntegrityError:
                pass

    def listar(self, pesquisa=""):
        p = f"%{(pesquisa or '').strip()}%"
        linhas = self.db.consultar(
            "SELECT * FROM bolsas WHERE nome LIKE ? OR descricao LIKE ? ORDER BY origem, nome", (p, p))
        return [Bolsa(**l) for l in linhas]

    def actualizar_automaticamente(self, termo="scholarships for international students"):
        """Pesquisa na web novas bolsas/faculdades e guarda-as. Sem internet, falha em silêncio.
        Devolve o número de bolsas novas."""
        novas = 0
        try:
            url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": termo})
            pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(pedido, timeout=10) as r:
                html = r.read().decode("utf-8", "ignore")
        except (OSError, ValueError):
            return 0
        for href, titulo in re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.S)[:10]:
            titulo = re.sub(r"<[^>]+>", "", titulo).strip()[:120]
            if "uddg=" in href:
                href = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("uddg", [href])[0]
            if not titulo or not href.startswith("http"):
                continue
            try:
                self.db.executar("INSERT INTO bolsas(nome,descricao,url,origem) VALUES(?,?,?,'auto')",
                                 (titulo, "Encontrada automaticamente na web", href))
                novas += 1
            except (sqlite3.IntegrityError, ErroBaseDados):
                pass
        return novas


class ServicoMentoria:
    def __init__(self, db):
        self.db = db

    def pedir(self, utilizador_id, tipo, mensagem=""):
        if tipo not in TIPOS_MENTORIA:
            raise ErroValidacao("Tipo de ajuda inválido.")
        self.db.executar("INSERT INTO pedidos_mentoria(utilizador_id,tipo,mensagem) VALUES(?,?,?)",
                         (utilizador_id, tipo, (mensagem or "").strip()[:1000]))

    def do_utilizador(self, utilizador_id):
        return self.db.consultar(
            "SELECT tipo, mensagem FROM pedidos_mentoria WHERE utilizador_id=? ORDER BY id DESC", (utilizador_id,))
