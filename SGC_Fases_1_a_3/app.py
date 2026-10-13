"""
SGC - Sistema de Gestão de Catálogo
Aplicação Flask com autenticação e CRUD de clientes e produtos.
"""
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sgc.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-por-uma-chave-segura"
db = SQLAlchemy(app)


class Usuario(db.Model):
    """Usuário autorizado a acessar o sistema."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)


class Cliente(db.Model):
    """Cliente cadastrado no sistema."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    cpf_cnpj = db.Column(db.String(30), unique=True, nullable=True)
    data_cadastro = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)


def login_required(view):
    """Impede acesso a páginas internas sem autenticação."""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar o sistema.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.context_processor
def dados_globais():
    """Disponibiliza o usuário logado nos templates."""
    usuario = db.session.get(Usuario, session.get("usuario_id")) if session.get("usuario_id") else None
    return {"usuario_logado": usuario}


@app.route("/")
def index():
    """Redireciona para o catálogo de produtos ou para o login."""
    if session.get("usuario_id"):
        return redirect(url_for("produtos"))
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    """Cria uma conta de usuário armazenando apenas o hash da senha."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")

        if not username or not email or not senha:
            flash("Preencha todos os campos obrigatórios.", "danger")
        elif len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.", "danger")
        elif senha != confirmar:
            flash("As senhas não coincidem.", "danger")
        elif Usuario.query.filter(
            db.or_(Usuario.username == username, Usuario.email == email)
        ).first():
            flash("Nome de usuário ou e-mail já cadastrado.", "danger")
        else:
            usuario = Usuario(
                username=username,
                email=email,
                senha_hash=generate_password_hash(senha)
            )
            try:
                db.session.add(usuario)
                db.session.commit()
                flash("Conta criada! Você já pode entrar.", "success")
                return redirect(url_for("login"))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Não foi possível criar a conta. Tente novamente.", "danger")
    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Autentica o usuário comparando a senha com o hash salvo."""
    if request.method == "POST":
        identificador = request.form.get("identificador", "").strip()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter(
            db.or_(Usuario.username == identificador, Usuario.email == identificador.lower())
        ).first()
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session.clear()
            session["usuario_id"] = usuario.id
            flash(f"Bem-vindo(a), {usuario.username}!", "success")
            return redirect(url_for("produtos"))
        flash("Usuário/e-mail ou senha inválidos.", "danger")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    """Encerra a sessão atual."""
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


@app.route("/clientes")
@login_required
def clientes():
    """Lista clientes, com busca opcional por nome."""
    lista_clientes = Cliente.query.order_by(Cliente.nome).all()
    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/cliente/novo", methods=["GET", "POST"])
@login_required
def cliente_novo():
    """Exibe formulário e cadastra um cliente."""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        documento = request.form.get("cpf_cnpj", "").strip() or None
        if not nome or not email:
            flash("Nome e e-mail são obrigatórios.", "danger")
        elif Cliente.query.filter_by(email=email).first():
            flash("Já existe um cliente com esse e-mail.", "danger")
        elif documento and Cliente.query.filter_by(cpf_cnpj=documento).first():
            flash("Já existe um cliente com esse CPF/CNPJ.", "danger")
        else:
            try:
                db.session.add(Cliente(nome=nome, email=email, telefone=telefone, cpf_cnpj=documento))
                db.session.commit()
                flash("Cliente cadastrado com sucesso.", "success")
                return redirect(url_for("clientes"))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Erro ao salvar cliente.", "danger")
    return render_template("cliente_form.html", cliente=None, titulo="Novo cliente")


@app.route("/cliente/editar/<int:id>", methods=["GET", "POST"])
@login_required
def cliente_editar(id):
    """Edita um cliente existente."""
    cliente = db.get_or_404(Cliente, id)
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        documento = request.form.get("cpf_cnpj", "").strip() or None
        email_duplicado = Cliente.query.filter(Cliente.email == email, Cliente.id != id).first()
        doc_duplicado = Cliente.query.filter(Cliente.cpf_cnpj == documento, Cliente.id != id).first() if documento else None
        if not nome or not email:
            flash("Nome e e-mail são obrigatórios.", "danger")
        elif email_duplicado:
            flash("Esse e-mail já pertence a outro cliente.", "danger")
        elif doc_duplicado:
            flash("Esse CPF/CNPJ já pertence a outro cliente.", "danger")
        else:
            cliente.nome, cliente.email = nome, email
            cliente.telefone, cliente.cpf_cnpj = telefone, documento
            try:
                db.session.commit()
                flash("Cliente atualizado com sucesso.", "success")
                return redirect(url_for("clientes"))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Erro ao atualizar cliente.", "danger")
    return render_template("cliente_form.html", cliente=cliente, titulo="Editar cliente")


@app.route("/cliente/excluir/<int:id>", methods=["POST"])
@login_required
def cliente_excluir(id):
    """Exclui cliente após confirmação no formulário."""
    cliente = db.get_or_404(Cliente, id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente excluído.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Não foi possível excluir o cliente.", "danger")
    return redirect(url_for("clientes"))




@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
