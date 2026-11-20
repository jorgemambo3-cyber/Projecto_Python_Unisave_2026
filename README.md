CDFJ-Opportunity
Centro de Direcionamento à Faculdade Juvenil
Uma plataforma digital que aproxima os jovens das oportunidades de bolsas de estudo no exterior.

1. Sobre o Projecto
O CDFJ-Opportunity é um projecto que consiste no desenvolvimento de um portal web e de uma aplicação Android destinados a conectar jovens dos 18 aos 35 anos a oportunidades de bolsas de estudo internacionais.

A plataforma pretende facilitar o acesso à informação sobre bolsas de estudo, oferecendo orientação durante os processos de candidatura, serviços de mentoria e apoio na preparação e organização da documentação necessária.

O projecto surge como resposta às dificuldades enfrentadas por muitos jovens na procura de oportunidades de formação no exterior e na realização dos respectivos processos de candidatura.

2. Objectivos do Projecto
2.1. Objectivo Geral
Desenvolver uma plataforma digital que facilite o acesso dos jovens às oportunidades de bolsas de estudo internacionais, proporcionando orientação e apoio durante os processos de candidatura.

2.2. Objectivos Específicos
Facilitar a pesquisa de bolsas de estudo no exterior.

Disponibilizar oportunidades actualizadas automaticamente.

Permitir o cadastro e a autenticação dos utilizadores.

Oferecer serviços de mentoria para candidaturas.

Facilitar o acesso a profissionais de apoio documental.

Permitir o acompanhamento e a consulta do histórico dos pedidos.

Disponibilizar uma aplicação Android através de ficheiro APK.

3. Funcionalidades Principais
Funcionalidade	Descrição
Cadastro	Registo com nome, e-mail, telefone, idade e senha.
Login	Autenticação segura dos utilizadores.
Restrição de idade	Acesso permitido a jovens dos 18 aos 35 anos.
Bolsas de estudo	Listagem de oportunidades internacionais.
Pesquisa	Pesquisa de bolsas e respectivos sites oficiais.
Actualização automática	Actualização das oportunidades a cada 24 horas.
Mentoria	Solicitação de orientação para candidaturas.
Apoio documental	Solicitação de assistência na preparação de documentos.
Histórico	Consulta dos pedidos realizados.
Aplicação Android	Acesso à plataforma através de APK.
4. Tecnologias Utilizadas
As seguintes tecnologias serão utilizadas no desenvolvimento do projecto:

Tecnologia	Utilização
Python 3.x	Linguagem principal de programação.
Flask	Desenvolvimento do portal web.
Werkzeug	Segurança e hash das senhas.
SQLite	Gestão da base de dados.
HTML5	Estrutura das páginas web.
CSS3	Estilização das interfaces.
JavaScript	Interactividade das páginas.
Kivy	Desenvolvimento da aplicação Android.
Buildozer	Compilação e geração do APK.
WebView	Acesso ao portal através do Android.
5. Arquitectura do Projecto
O CDFJ-Opportunity será desenvolvido seguindo o paradigma de Programação Orientada a Objectos (POO), com separação de responsabilidades por ficheiros e módulos.

Esta organização permite melhorar a manutenção, reutilização, legibilidade e expansão do sistema.

5.1. Estrutura de Pastas
CDFJ-Opportunity/
│
├── main.py
├── web.py
├── modelos.py
├── database.py
├── excecoes.py
├── requirements.txt
├── README.md
│
├── database/
│   └── cdfj_opportunity.db
│
├── services/
│   ├── __init__.py
│   └── actualizador.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── cadastro.html
│   ├── login.html
│   ├── dashboard.html
│   ├── bolsas.html
│   ├── mentoria.html
│   ├── documentacao.html
│   └── historico.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── android/
│   ├── main.py
│   └── buildozer.spec
│
└── tests/
    ├── test_utilizadores.py
    ├── test_bolsas.py
    └── test_servicos.py
5.2. Descrição dos Principais Ficheiros
Ficheiro	Responsabilidade
main.py	Ponto de entrada e inicialização da aplicação.
web.py	Configuração das rotas e páginas Flask.
modelos.py	Implementação das classes e regras de negócio.
database.py	Criação e gestão da base de dados SQLite.
excecoes.py	Definição das excepções personalizadas.
actualizador.py	Pesquisa e actualização automática das bolsas.
requirements.txt	Lista das dependências necessárias.
6. Classes Principais (POO)
O sistema será composto pelas seguintes classes:

Utilizador: representa os utilizadores registados na plataforma.

Bolsa: representa uma oportunidade de bolsa de estudo.

Validador: valida os dados introduzidos pelos utilizadores.

ServicoUtilizadores: gere o cadastro e a autenticação.

ServicoBolsas: gere a pesquisa e a listagem de bolsas.

ServicoMentoria: gere os pedidos de mentoria e apoio documental.

Database: gere as operações da base de dados.

7. Base de Dados
Será utilizada a tecnologia SQLite para armazenar e gerir as informações do sistema.

7.1. Tabela: utilizadores
Campo	Descrição
id	Identificador único do utilizador.
nome	Nome completo.
email	Endereço electrónico.
telefone	Contacto telefónico.
idade	Idade do utilizador.
senha_hash	Senha armazenada através de hash.
7.2. Tabela: bolsas
Campo	Descrição
id	Identificador único da bolsa.
titulo	Título da oportunidade.
pais	País de destino.
instituicao	Instituição responsável.
link	Link oficial da oportunidade.
data_actualizacao	Data da última actualização.
7.3. Tabela: pedidos
Campo	Descrição
id	Identificador único do pedido.
utilizador_id	Referência ao utilizador.
tipo	Tipo de serviço solicitado.
descricao	Descrição do pedido.
estado	Estado actual do pedido.
data_pedido	Data de realização do pedido.
8. Equipa de Desenvolvimento
O projecto está a ser desenvolvido pelos seguintes integrantes:

Nº	Nome	GitHub
1	Cardoso Aulino Nhaule	@nhaulecardoso-lag0
2	Divino Felix Machava	@divinofelixmachava-fst
3	Felix Alson Jovo	@felialson1
4	Jorge Raimundo Mambo	@jorgemambo3-cyber
9. Requisitos do Sistema
Para executar o projecto, é necessário ter instalado:

Python 3.8 ou superior.

Git.

Pip (gestor de pacotes Python).

Visual Studio Code ou outro editor de código.

10. Testes
O projecto prevê a realização de testes para verificar o funcionamento dos principais componentes do sistema.

Os testes serão organizados em três áreas:

test_utilizadores.py: testes relacionados com o cadastro e autenticação.

test_bolsas.py: testes relacionados com as oportunidades de bolsas.

test_servicos.py: testes relacionados com os serviços de mentoria e apoio documental.

Para executar os testes, poderá ser utilizado:

python -m unittest discover -s tests
11. Impacto Esperado
O CDFJ-Opportunity pretende contribuir para a democratização do acesso à educação internacional, reduzindo as dificuldades encontradas pelos jovens na identificação e candidatura a bolsas de estudo.

Através da integração de informação, orientação e acompanhamento, a plataforma pretende tornar os processos de candidatura mais acessíveis, organizados e eficientes.

