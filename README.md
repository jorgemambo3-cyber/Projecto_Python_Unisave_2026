CDFJ-Opportunity
Centro de Direcionamento à Faculdade Juvenil
Uma plataforma digital que aproxima os jovens das oportunidades de bolsas de estudo no exterior.

Sobre o Projecto
O CDFJ-Opportunity é um projecto que consiste no desenvolvimento de um portal web e de uma aplicação Android destinados a conectar jovens dos 18 aos 35 anos a oportunidades de bolsas de estudo internacionais.

A plataforma pretende facilitar o acesso à informação sobre bolsas de estudo, oferecendo orientação durante os processos de candidatura, serviços de mentoria e apoio na preparação e organização da documentação necessária.

O projecto surge como resposta às dificuldades enfrentadas por muitos jovens na procura de oportunidades de formação no exterior e na realização dos respectivos processos de candidatura.


Objectivos do Projecto
Objectivo Geral
Desenvolver uma plataforma digital que facilite o acesso dos jovens às oportunidades de bolsas de estudo internacionais, proporcionando orientação e apoio durante os processos de candidatura.

Objectivos Específicos
Facilitar a pesquisa de bolsas de estudo no exterior.
Disponibilizar oportunidades actualizadas automaticamente.
Permitir o cadastro e autenticação dos utilizadores.
Oferecer serviços de mentoria para candidaturas.
Facilitar o acesso a profissionais de apoio documental.
Permitir o acompanhamento e consulta do histórico dos pedidos.
Disponibilizar uma aplicação Android através de APK.

Funcionalidades Principais

Funcionalidade	Descrição
Cadastro	Registo com nome, e-mail, telefone, idade e senha
Login	Autenticação segura dos utilizadores
Restrição de idade	Acesso permitido dos 18 aos 35 anos
Bolsas de estudo	Listagem de oportunidades internacionais
Pesquisa	Pesquisa de bolsas e respectivos sites
Actualização automática	Actualização das oportunidades a cada 24 horas
Mentoria	Solicitação de orientação para candidaturas
Apoio documental	Solicitação de assistência documental
Histórico	Consulta dos pedidos realizados
Aplicação Android	Acesso à plataforma através de APK

Tecnologias Utilizadas
As seguintes tecnologias serão utilizadas no desenvolvimento:


Tecnologia	Utilização
Python 3.x	Linguagem principal
Flask	Desenvolvimento do portal web
Werkzeug	Hash e segurança das senhas
SQLite	Gestão da base de dados
HTML5	Estrutura das páginas
CSS3	Estilização das interfaces
JavaScript	Interactividade
Kivy	Desenvolvimento da aplicação Android
Buildozer	Compilação e geração do APK
WebView	Acesso ao portal através do Android

Arquitectura do Projecto
O projecto será desenvolvido seguindo o paradigma de Programação Orientada a Objectos (POO), com separação das responsabilidades por ficheiros e módulos.

Estrutura de Pastas

Text
CDFJ-Opportunity/

main.py
web.py
modelos.py
database.py
excecoes.py
requirements.txt
README.md

database/
cdfj_opportunity.db

services/
__init__.py
actualizador.py

templates/
base.html
index.html
cadastro.html
login.html
dashboard.html
bolsas.html
mentoria.html
documentacao.html
historico.html

static/
css/
style.css
js/
script.js
images/

android/
main.py
buildozer.spec

tests/
test_utilizadores.py
test_bolsas.py
test_servicos.py
Descrição dos Principais Ficheiros
Main.py: ponto de entrada e inicialização da aplicação.
Web.py: configuração das rotas e páginas Flask.
Modelos.py: implementação das classes e regras de negócio.
Database.py: criação e gestão da base de dados SQLite.
Excecoes.py: definição das excepções personalizadas.
Actualizador.py: pesquisa e actualização automática das bolsas.
Requirements.txt: lista das dependências necessárias.
Classes Principais (POO)
O sistema será composto pelas seguintes classes:

Utilizador: representa os utilizadores registados.
Bolsa: representa uma oportunidade de bolsa de estudo.
Validador: valida os dados introduzidos.
ServicoUtilizadores: gere o cadastro e a autenticação.
ServicoBolsas: gere a pesquisa e listagem de bolsas.
ServicoMentoria: gere os pedidos de mentoria e apoio documental.
Database: gere as operações da base de dados.

Base de Dados
Será utilizada a tecnologia SQLite para armazenar e gerir as informações do sistema.

Tabela: utilizadores
Id
Nome
Email
Telefone
Idade
Senha_hash
Tabela: bolsas
Id
Titulo
Pais
Instituicao
Link
Data_actualizacao
Tabela: pedidos
Id
Utilizador_id
Tipo
Descricao
Estado
Data_pedido

Equipa de Desenvolvimento
O projecto está a ser desenvolvido pelos seguintes integrantes:


Nº	Nome	GitHub
1	Cardoso Aulino Nhaule	(nhaulecardoso-lag0)
2	Divino Felix Machava	(divinofelixmachava-fst)
3	Felix Alson Jovo	(felialson1)
4	Jorge Raimundo Mambo	(jorgemambo3-cyber)

Requisitos do Sistema
Para executar o projecto, é necessário ter:

Python 3.8 ou superior.
Git instalado.
Pip (gestor de pacotes Python).
Visual Studio Code ou outro editor de código.

Instalação e Configuração
1.	Clonar o repositório

Bash
Git clone https://github.com/SEU-USERNAME/Projecto_Python_Unisave_2026.git
2.	Entrar na pasta do projecto

Bash
Cd Projecto_Python_Unisave_2026
3.	Criar um ambiente virtual

Bash
Python -m venv venv
4.	Activar o ambiente virtual
Windows:


Bash
Venv\Scripts\activate
Linux:


Bash
Source venv/bin/activate
5.	Instalar as dependências

Bash
Pip install -r requirements.txt
6.	Executar a aplicação

Bash
Python main.py
7.	Aceder ao sistema
Abrir o navegador e inserir o seguinte endereço:


Text
http://127.0.0.1:5000


Segurança
O CDFJ-Opportunity deverá implementar mecanismos de segurança, nomeadamente:

Hash seguro das senhas dos utilizadores.
Validação dos dados durante o cadastro.
Restrição de acesso por faixa etária.
Protecção das páginas que exigem autenticação.
Utilização de consultas parametrizadas na base de dados.
Gestão segura das sessões dos utilizadores.

Versão Android
O projecto contará também com uma aplicação para dispositivos Android, distribuída em formato APK.

A aplicação utilizará Kivy e WebView para permitir o acesso às funcionalidades do portal através de dispositivos móveis.

A comunicação com o servidor Flask será realizada através de uma ligação de rede.


Actualização Automática das Bolsas
O sistema contará com um mecanismo de pesquisa na web para identificar novas oportunidades de bolsas de estudo.

A actualização será realizada a cada 24 horas, seguindo as seguintes etapas:

Pesquisar sites e portais de bolsas de estudo.
Recolher informações sobre as oportunidades.
Validar os links encontrados.
Evitar oportunidades duplicadas.
Actualizar a base de dados SQLite.
Disponibilizar as oportunidades aos utilizadores.


Estado do Projecto
Estado actual: Em desenvolvimento.

As funcionalidades serão implementadas, integradas e testadas progressivamente até à disponibilização das versões web e Android.


Contexto Académico
Projecto desenvolvido no âmbito da formação universitária, com o objectivo de aplicar conhecimentos de programação Python, Programação Orientada a Objectos, desenvolvimento web e gestão de bases de dados.


Licença
Projecto desenvolvido para fins académicos.

🌍 CDFJ-Opportunity
Aproximando os jovens das oportunidades de formação internacional!

