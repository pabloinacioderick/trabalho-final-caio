# SGC — Fases 1, 2 e 3

Esta versão mantém a estrutura inicial (Fase 1), adiciona autenticação de usuários (Fase 2) e CRUD de clientes (Fase 3). As funcionalidades das Fases 4, 5 e 6 foram deixadas de fora para serem adicionadas depois.

## Funcionalidades
- Interface responsiva com Bootstrap 5.
- Registro de usuário, login e logout.
- Senhas armazenadas com hash.
- Páginas internas protegidas por login.
- Cadastro, listagem, edição e exclusão de clientes.
- Validação básica e prevenção de e-mail/CPF-CNPJ duplicados.

## Executar no Windows
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000 e crie uma conta.

## Importante para atualizar o GitHub
Se a Fase 1 já está no seu repositório, copie os arquivos desta pasta para dentro da pasta do seu repositório existente, mas **não apague a pasta `.git`**. Depois teste o sistema antes de fazer commit. Não envie `.venv` nem arquivos `.db`.
