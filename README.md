# CDFJ-Opportunity (Centro de Direcionamento à Faculdade Juvenil)

- Portal web e aplicação Android que liga jovens dos 18 aos 35 anos a bolsas de estudo no exterior, mentoria para candidaturas e pessoas capacitadas para tratar da documentação. Resolve a dificuldade de encontrar sites de bolsas e de ter orientação nas inscrições.

## Elementos do Grupo

- Nome Completo 1 (Username GitHub)
- Nome Completo 2 (Username GitHub)
- Nome Completo 3 (Username GitHub)
- Nome Completo 4 (Username GitHub)

## Funcionalidades

- Cadastro e login (nome, e-mail, telefone, idade e senha com hash), só para 18 a 35 anos
- Lista automática de sites de bolsas de estudo, com pesquisa, actualizada a cada 24 h por pesquisa na web
- Pedidos de mentoria e de apoio documental, com histórico por utilizador
- Versão APK para Android (Kivy + WebView)

## Stack Técnica

- Linguagem: Python 3.x
- Paradigma: Programação Orientada a Objetos (POO)
- Armazenamento: SQLite
- Dependências: Flask (inclui Werkzeug); Kivy e Buildozer apenas para gerar o APK

## Arquitectura

- `main.py`: ponto de entrada (PC e Android), arranque do servidor e da actualização automática
- `web.py`: rotas e páginas Flask
- `modelos.py`: classes `Utilizador`, `Bolsa`, `Validador`, `ServicoUtilizadores`, `ServicoBolsas`, `ServicoMentoria`
- `database.py`: classe `Database` (SQLite)
- `excecoes.py`: excepções personalizadas (`ErroValidacao`, `ErroAutenticacao`, `ErroBaseDados`)

## Requisitos

- Python 3.8 ou superior instalado no computador.

## Instalação e Execução

```bash
git clone https://github.com/SEU-USERNAME/Projecto_Python_Unisave_2026.git
cd Projecto_Python_Unisave_2026
pip install -r requirements.txt
python main.py
```

Para gerar o APK (Linux, WSL ou Google Colab): `pip install buildozer cython` e `buildozer android debug`.
