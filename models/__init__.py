class Campo:
    def __init__(self, id, nome, localizacao, tipo, dimensoes, iluminacao, preco):
        self.id = id
        self.nome = nome
        self.localizacao = localizacao
        self.tipo = tipo
        self.dimensoes = dimensoes
        self.iluminacao = iluminacao
        self.preco = preco

    def __str__(self):
        return f"Campo {self.nome} (ID: {self.id}) - {self.localizacao}"