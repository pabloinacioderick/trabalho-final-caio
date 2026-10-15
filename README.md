# SGC — Sistema de Gestão de Catálogo

Projeto completo integrado das **Fases 1 a 6**, usando Python, Flask, Flask-SQLAlchemy, SQLite e Bootstrap 5.

## Funcionalidades incluídas

- Estrutura inicial do projeto e interface responsiva com Bootstrap 5.
- Registro, login e logout de usuários.
- Hash de senha (não armazena senha em texto puro).
- Proteção de páginas internas para usuários autenticados.
- CRUD de clientes: cadastro, listagem, edição e exclusão.
- Validação de e-mail e CPF/CNPJ duplicados.
- CRUD de produtos: cadastro, listagem, edição e exclusão.
- Validação de preço e estoque não negativos.
- Busca por nome em clientes e produtos.
- Mensagens `flash`, rollback de operações de banco e páginas 403/404.
- Documentação das rotas e guia de instalação.

## Requisitos

- Python 3.10 ou superior
- pip
- Conexão com a internet para carregar o Bootstrap 5 via CDN na interface

## Instalação no Windows / Visual Studio Code

1. Extraia o arquivo ZIP.
2. Abra a pasta `SGC_Completo_Fases_1_a_6` no VS Code.
3. Abra **Terminal → Novo Terminal**.
4. Execute um comando por vez:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

5. Acesse http://127.0.0.1:5000.
6. Clique em **Criar conta**, registre um usuário e entre no sistema.

## Estrutura do projeto

```text
SGC_Completo_Fases_1_a_6/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── templates/
    ├── base.html
    ├── login.html
    ├── registro.html
    ├── clientes.html
    ├── cliente_form.html
    ├── produtos.html
    ├── produto_form.html
    ├── 403.html
    └── 404.html
```

## Rotas principais

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Abre produtos se estiver autenticado; caso contrário, login |
| GET, POST | `/registro` | Criar usuário |
| GET, POST | `/login` | Entrar no sistema |
| POST | `/logout` | Encerrar sessão |
| GET | `/clientes` | Listar e buscar clientes |
| GET, POST | `/cliente/novo` | Cadastrar cliente |
| GET, POST | `/cliente/editar/<id>` | Editar cliente |
| POST | `/cliente/excluir/<id>` | Excluir cliente |
| GET | `/produtos` | Listar e buscar produtos |
| GET, POST | `/produto/novo` | Cadastrar produto |
| GET, POST | `/produto/editar/<id>` | Editar produto |
| POST | `/produto/excluir/<id>` | Excluir produto |

## Git e commits por fase

A pasta pode ser aberta como projeto único. Se a Fase 1 já estiver em um repositório Git com histórico que você precisa preservar, copie os arquivos deste projeto para dentro da pasta da Fase 1 e substitua os arquivos de mesmo nome; não apague a pasta `.git`.

Sugestões de commits para usar ao concluir cada etapa:

```bash
git add .
git commit -m "Setup inicial do projeto SGC"
git add .
git commit -m "Implementa sistema de autenticação e sessões"
git add .
git commit -m "Implementa CRUD completo de clientes"
git add .
git commit -m "Implementa CRUD completo de produtos"
git add .
git commit -m "Aprimora segurança, feedbacks e filtros de busca"
git add .
git commit -m "Entrega da versão final do SGC"
```

Não é necessário executar todos os commits de uma vez; faça cada commit após concluir e testar a fase correspondente. Se a Fase 1 já foi commitada, não repita o commit inicial.

## Segurança antes de publicar

- Troque `SECRET_KEY` por um segredo aleatório guardado em variável de ambiente.
- Desative `debug=True` em produção.
- Para um uso mais robusto, adicione proteção CSRF (por exemplo, Flask-WTF).
- Não envie `.venv`, arquivos `.db` nem segredos para o Git.
