from datetime import datetime

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
    email = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    apelido = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Campo {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'apelido':self.apelido,
            'tipo':self.tipo
        }


class Locacao(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    campo_id = db.Column(db.Integer, db.ForeignKey('campo.id'), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('locacoes', lazy=True))
    campo = db.relationship('Campo', backref=db.backref('locacoes', lazy=True))