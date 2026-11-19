"""Interface web (Flask) do CDFJ-Opportunity: páginas e rotas."""
import os
from functools import wraps

from flask import Flask, flash, redirect, render_template_string, request, session, url_for

from excecoes import ErroAutenticacao, ErroBaseDados, ErroCDFJ, ErroValidacao
from modelos import (IDADE_MAX, IDADE_MIN, TIPOS_MENTORIA, ServicoBolsas,
                     ServicoMentoria, ServicoUtilizadores)

LAYOUT = """<!doctype html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>CDFJ-Opportunity</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;background:#f4f6fb;color:#1b2430}
header{background:#12355b;color:#fff;padding:14px 18px;display:flex;justify-content:space-between;align-items:center}
header a{color:#fff;margin-left:12px;text-decoration:none;font-size:14px}
main{max-width:760px;margin:0 auto;padding:18px}
.card{background:#fff;border-radius:12px;padding:16px;margin:12px 0;box-shadow:0 1px 4px #0002}
input,select,textarea{width:100%;padding:11px;margin:6px 0 12px;border:1px solid #ccd;border-radius:8px;font-size:16px}
button,.btn{background:#e8a317;border:0;color:#12355b;font-weight:700;padding:12px 18px;border-radius:8px;font-size:16px;text-decoration:none;display:inline-block}
.msg{background:#fff3cd;padding:10px;border-radius:8px;margin:10px 0}small{color:#667}
</style></head><body>
<header><strong>CDFJ-Opportunity</strong><nav>
{% if session.uid %}<a href="/painel">Bolsas</a><a href="/mentoria">Mentoria</a><a href="/sair">Sair</a>
{% else %}<a href="/entrar">Entrar</a><a href="/cadastro">Cadastro</a>{% endif %}</nav></header>
<main>{% for m in get_flashed_messages() %}<div class="msg">{{ m }}</div>{% endfor %}{{ body|safe }}</main>
</body></html>"""


def pagina(corpo, **ctx):
    return render_template_string(LAYOUT, body=render_template_string(corpo, **ctx))


def criar_app(db):
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "muda-esta-chave-em-producao")
    utilizadores, bolsas, mentoria = ServicoUtilizadores(db), ServicoBolsas(db), ServicoMentoria(db)

    def login_required(f):
        @wraps(f)
        def interior(*a, **k):
            if "uid" not in session:
                return redirect(url_for("entrar"))
            return f(*a, **k)
        return interior

    @app.errorhandler(ErroBaseDados)
    def erro_bd(e):
        return pagina('<div class="card">Erro na base de dados. Tenta novamente.</div>'), 500

    @app.route("/")
    def inicio():
        return pagina("""<div class="card"><h2>Centro de Direcionamento à Faculdade Juvenil</h2>
        <p>Portal que liga jovens dos {{a}} aos {{b}} anos a bolsas de estudo no exterior, mentoria para
        candidaturas e pessoas capacitadas para tratar da documentação.</p>
        <a class="btn" href="/cadastro">Criar conta</a> &nbsp; <a href="/entrar">Já tenho conta</a></div>""",
                      a=IDADE_MIN, b=IDADE_MAX)

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            f = request.form
            try:
                utilizadores.registar(f.get("nome"), f.get("email"), f.get("telefone"),
                                      f.get("idade"), f.get("senha"))
                flash("Conta criada! Faz login.")
                return redirect(url_for("entrar"))
            except ErroValidacao as e:
                flash(str(e))
        return pagina("""<div class="card"><h2>Cadastro</h2><form method="post">
        Nome<input name="nome" required>E-mail<input name="email" type="email" required>
        Número de telefone<input name="telefone" type="tel" required>
        Idade<input name="idade" type="number" min="{{a}}" max="{{b}}" required>
        Senha<input name="senha" type="password" minlength="6" required>
        <button>Cadastrar</button></form></div>""", a=IDADE_MIN, b=IDADE_MAX)

    @app.route("/entrar", methods=["GET", "POST"])
    def entrar():
        if request.method == "POST":
            try:
                u = utilizadores.autenticar(request.form.get("email"), request.form.get("senha"))
                session["uid"], session["nome"] = u.id, u.nome
                return redirect(url_for("painel"))
            except ErroAutenticacao as e:
                flash(str(e))
        return pagina("""<div class="card"><h2>Entrar</h2><form method="post">
        E-mail<input name="email" type="email" required>Senha<input name="senha" type="password" required>
        <button>Entrar</button></form></div>""")

    @app.route("/sair")
    def sair():
        session.clear()
        return redirect(url_for("inicio"))

    @app.route("/painel")
    @login_required
    def painel():
        q = request.args.get("q", "")
        return pagina("""<h2>Olá, {{ session.nome }} 👋</h2>
        <form><input name="q" placeholder="Pesquisar bolsa, país ou faculdade..." value="{{ q }}"></form>
        {% for b in lista %}<div class="card"><strong>{{ b.nome }}</strong><br><small>{{ b.descricao }}</small><br><br>
        <a class="btn" href="{{ b.url }}" target="_blank" rel="noopener">Abrir site</a></div>
        {% else %}<div class="card">Sem resultados.</div>{% endfor %}""", lista=bolsas.listar(q), q=q)

    @app.route("/mentoria", methods=["GET", "POST"])
    @login_required
    def pagina_mentoria():
        if request.method == "POST":
            try:
                mentoria.pedir(session["uid"], request.form.get("tipo"), request.form.get("mensagem"))
                flash("Pedido enviado! Um mentor vai contactar-te.")
            except ErroCDFJ as e:
                flash(str(e))
            return redirect(url_for("pagina_mentoria"))
        return pagina("""<h2>Mentoria e documentação</h2>
        {% for t,d in tipos.items() %}<div class="card"><strong>{{ t }}</strong><br><small>{{ d }}</small></div>{% endfor %}
        <div class="card"><form method="post">Tipo de ajuda<select name="tipo">
        {% for t in tipos %}<option>{{ t }}</option>{% endfor %}</select>
        Mensagem<textarea name="mensagem" rows="4"></textarea><button>Pedir ajuda</button></form></div>
        {% if pedidos %}<h3>Os meus pedidos</h3>{% for p in pedidos %}
        <div class="card"><strong>{{ p.tipo }}</strong><br><small>{{ p.mensagem }}</small></div>{% endfor %}{% endif %}""",
                      tipos=TIPOS_MENTORIA, pedidos=mentoria.do_utilizador(session["uid"]))

    app.servico_bolsas = bolsas
    return app
