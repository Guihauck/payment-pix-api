# Flask Pix Payment API 💳

Uma API RESTful em Flask para criação, exibição e confirmação de pagamentos via Pix, com suporte a WebSockets para notificações em tempo real.

## 🧰 Tecnologias utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-SocketIO
- SQLite (padrão, mas facilmente adaptável para MySQL/PostgreSQL)
- HTML (Jinja2) para renderização de páginas de pagamento

## 🚀 Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv
source venv/Scripts/activate      # Windows (Git Bash)
# ou
source venv/bin/activate          # Linux/macOS
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

> Gere um `requirements.txt` com:  
> `pip freeze > requirements.txt`

### 4. Rodar a aplicação

```bash
python app.py
```

Acesse em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📌 Endpoints

### `POST /payments/pix`

Cria um novo pagamento Pix.

**Request JSON:**
```json
{
  "Value": 150.00
}
```

**Response:**
```json
{
  "message": "The payment has been created",
  "payment": {
    "id": 1,
    "value": 150.00,
    "qr_code": "static/img/qrcode_123.png",
    ...
  }
}
```

---

### `GET /payments/pix/qr_code/<file_name>`

Retorna a imagem PNG do QR Code de pagamento Pix.

---

### `POST /payments/confirmation/pix`

Confirma manualmente um pagamento com `bank_payment_id`.

**Request JSON:**
```json
{
  "bank_payment_id": "1234567890",
  "value": 150.00
}
```

---

### `GET /payments/pix/<payment_id>`

Renderiza uma página HTML com o QR Code e status do pagamento.

---

## 🔔 WebSocket

A aplicação usa WebSockets para notificar clientes sobre a confirmação de pagamento.

- Evento: `payment-confirmation-<payment_id>`

---

## 📁 Estrutura básica do projeto

```
.
├── app.py
├── db/
│   └── payment.py
├── repository/
│   └── database.py
├── payment/
│   └── pix.py
├── static/
│   └── img/
├── templates/
│   ├── 404.html
│   ├── confirmed_payment.html
│   └── payment.html
```

---

## ✉ Contato

[Guilherme Jorge Hauck](https://github.com/Guihauck)
