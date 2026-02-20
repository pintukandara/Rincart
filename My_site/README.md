# 🛒 RinCart – E-commerce Web Application

RinCart is a full-stack e-commerce web application built to demonstrate how a real-world online shopping platform works under the hood. It covers backend architecture, REST APIs, authentication, database management, and frontend integration.

> Built with **Django**, **Django REST Framework**, **PostgreSQL**, and frontend technologies like **HTML**, **CSS**, and **JavaScript**.

---

## ✨ Features

- 🔐 **User Authentication** – Register, Login, and Logout
- 🛍️ **Product Listing & Detail View** – Browse and explore products
- 🛒 **Cart Management** – Add to / Remove from Cart
- 📦 **Order Placement System** – End-to-end order flow
- 📊 **Admin Panel** – Manage products and orders
- ⚙️ **Celery Integration** – Asynchronous task processing

---

## 🧰 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Django                    |
| Frontend   | HTML, CSS, JavaScript             |
| Database   | SQLite3                           |
| Task Queue | Celery                            |

---

## 📁 Project Structure

```
RinCart/
│
├── backend/
│   └── user_info/
│
├── frontend/
│   ├── static/
│   └── templates/
│
└── manage.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pintukandara/rincart.git
cd rincart
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv myenv

# Activate on Windows
myenv\Scripts\activate

# Activate on macOS/Linux
source myenv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the Database

Make sure PostgreSQL is running and update your database credentials in `settings.py` If you'r Using One:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run migrations:

```bash
python manage.py migrate
```

### 5️⃣ Start the Development Server

```bash
python manage.py runserver
```

### 6️⃣ Start the Celery Worker

```bash
celery -A My_site worker -l info
```

---

## 🛠️ API Overview

RinCart exposes Endpints using Djagno. You can explore and test endpoints through the browsable EndPoints at `http://127.0.0.1:8000/`.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, make your changes, and open a pull request.

---
## Contact For More information 
pintukandara124@gmail.com