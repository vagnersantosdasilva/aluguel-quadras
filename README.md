Aqui está a versão refatorada e corrigida do seu README:

---

### **README.md**

# **Sistema de Aluguel de Quadras**

Este é um sistema desenvolvido em Flask para gerenciar o aluguel de quadras esportivas.

## **Pré-requisitos**

* **Git:** Para clonar o repositório.
* **Python 3.8.10** ou superior.
* **Virtualenv:** Para criar um ambiente virtual isolado para o projeto.

## **Instalação**

### **1. Clonar o Repositório**

```bash
git clone https://github.com/vagnersantosdasilva/aluguel-quadras.git
cd aluguel-quadras  # Acesse o diretório do projeto
```

### **2. Criar e Ativar o Ambiente Virtual**

* No **Linux/macOS**:
  ```bash
  python3 -m venv venv  # Cria um ambiente virtual
  source venv/bin/activate  # Ativa o ambiente virtual
  ```

* No **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Ativa o ambiente virtual
  ```

### **3. Instalar as Dependências**

```bash
pip install -r requirements.txt  # Instala as dependências listadas
```

### **4. Configurar o Ambiente**

1. **Criar o arquivo `.env`**: Na raiz do projeto, crie um arquivo `.env` e adicione as variáveis de ambiente necessárias:

```bash
LOCACAO_MONITOR_INTERVAL=15  # Intervalo para verificar locações canceladas
PAGAMENTO_MONITOR_INTERVAL=10  # Intervalo para verificar pagamentos pendentes
SGBD=mysql+mysqlconnector
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=seu_host
DB_NAME=nome_do_banco

MAIL_SERVER=smtp-relay.sendinblue.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=seu_email
MAIL_PASSWORD=sua_senha
MAIL_DEFAULT_NAME="Sistema de Aluguel de Quadras"
MAIL_DEFAULT_EMAIL=seu_email_padrao
```

2. **Configurar o banco de dados**: Crie o banco de dados e certifique-se de que as credenciais estejam corretas no arquivo `config.py`.

### **5. Executar a Aplicação**

Com o ambiente virtual ativado e as configurações corretas, execute a aplicação com o seguinte comando:

```bash
flask run
```

A aplicação estará acessível em `http://127.0.0.1:5000/`.

## **Funcionalidades**

* **Gerenciamento de usuários:** Cadastro
* **Gerenciamento de quadras:** Criação, edição e exclusão de quadras.
* **Agendamento de locações:** Reservas de quadras em horários disponíveis.
* **Monitoramento de listas de espera**
* **Controle de reservas para horários concorridos**
* **Envio de notificações por email**
* **Monitoramento de pagamentos:** Controle de pagamentos pendentes e confirmados.
