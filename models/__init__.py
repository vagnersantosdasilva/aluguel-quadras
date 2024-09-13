from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Campo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    dimensoes = db.Column(db.String(50), nullable=False)
    iluminacao = db.Column(db.Boolean, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    # Relacionamentos
    horarios = db.relationship('GradeHorario', backref='campo', lazy=True)
    excecoes = db.relationship('ExcecaoHorario', backref='campo', lazy=True)

    def __repr__(self):
        return f'<Campo {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'localizacao': self.localizacao,
            'tipo': self.tipo,
            'dimensoes': self.dimensoes,
            'iluminacao': self.iluminacao,
            'preco': float(self.preco)  # Convertendo Decimal para float para serialização JSON
        }

class GradeHorario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campo_id = db.Column(db.Integer, db.ForeignKey('campo.id'), nullable=False)
    dia_semana = db.Column(db.String(10), nullable=False)  # Ex: 'Segunda', 'Terça', etc.
    horario_abertura = db.Column(db.Time, nullable=False)
    horario_fechamento = db.Column(db.Time, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)  # Para desativar horários sem apagá-los

    def to_dict(self):
        return {
            'id': self.id,
            'campo_id': self.campo_id,
            'dia_semana': self.dia_semana,
            'horario_abertura': self.horario_abertura.strftime("%H:%M"),
            'horario_fechamento': self.horario_fechamento.strftime("%H:%M"),
            'ativo': self.ativo
        }

class ExcecaoHorario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campo_id = db.Column(db.Integer, db.ForeignKey('campo.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)  # Data específica da exceção
    horario_abertura = db.Column(db.Time, nullable=False)
    horario_fechamento = db.Column(db.Time, nullable=False)
    descricao = db.Column(db.String(255))  # Descrição da exceção, ex: 'Feriado de Ano Novo'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)  # Email deve ser único
    tipo = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Mantém o nome 'password'
    apelido = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'apelido': self.apelido,
            'tipo': self.tipo
        }

    # Propriedade para manipular a senha
    @property
    def password_plain(self):
        raise AttributeError('A senha não pode ser lida diretamente.')

    @password_plain.setter
    def password_plain(self, password):
        # Gera o hash da senha ao definir
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # Verifica se a senha fornecida corresponde ao hash armazenado
        return check_password_hash(self.password, password)


class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    campo_id = db.Column(db.Integer, db.ForeignKey('campo.id'), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='PENDENTE')
    usuario = db.relationship('Usuario', backref=db.backref('locacoes', lazy=True))
    campo = db.relationship('Campo', backref=db.backref('locacoes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'campo_id': self.campo_id,
            'usuario_id': self.usuario_id,
            'data_inicio': self.data_inicio.strftime("%Y-%m-%d"),  # Converte para string no formato de data
            'horario_inicio': self.horario_inicio.strftime("%H:%M"),  # Converte para string no formato de hora
            'horario_fim': self.horario_fim.strftime("%H:%M"),  # Converte para string no formato de hora
            'valor_total': str(self.valor_total),  # Converte para string se for Decimal
            # Adicione outros atributos conforme necessário
        }

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacao.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pendente')  # Ex: 'pendente', 'confirmado', 'falhou'
    meio = db.Column(db.String(50), nullable=True)  # Ex: 'cartão', 'boleto', 'pix'
    data_pagamento = db.Column(db.DateTime, nullable=True)
    valor = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'locacao_id': self.locacao_id,
            'status': self.status,
            'meio': self.meio,
            'data_pagamento': self.data_pagamento.strftime("%Y-%m-%d %H:%M:%S") if self.data_pagamento else None,
            'valor': str(self.valor)
        }