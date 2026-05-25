# 🏠 hometri.com

<div align="center">

**A comprehensive real estate platform built with Django**

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

*Designed to manage agents, listings, teams, and users with a robust backend, admin interface, and customizable frontend for real estate operations.*

[Features](#-features) • [Installation](#-installation) • [Documentation](#-table-of-contents) • [Contributing](#-contributing)

</div>

---

## 📑 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🗄️ Database Migrations](#️-database-migrations)
- [▶️ Running the Project](#️-running-the-project)
- [📦 Static & Media Files](#-static--media-files)
- [👨‍💼 Admin Panel](#-admin-panel)
- [🧪 Testing](#-testing)
- [🖼️ Adding Images](#️-adding-images)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

## 🎯 Project Overview

**hometri.com** is a Django-based web application for real estate management. It supports agent profiles, property listings, team management, and user authentication. The project is modular, scalable, and ready for production deployment.

> **Built for**: Real estate agencies, property management companies, and housing platforms
> 
> **Tech Stack**: Django, Python, SQLite/PostgreSQL, Bootstrap

---

## ✨ Features

### 🎨 Additional Features
- 🎛️ **Admin Interface** - Custom templates with enhanced UI
- 📁 **File Handling** - Static and media file management
- 🧩 **Modular Design** - Separated apps (agents, team, users, hometri)
- 🎨 **Bootstrap UI** - Responsive and modern interface design
- 🗄️ **Database Flexibility** - Support for SQLite and PostgreSQL

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PostgreSQL (optional, for production)

### Step-by-Step Setup

**1️⃣ Clone the repository:**
```bash
git clone https://github.com/spyberpolymath/hometri.com.git
cd hometri.com
```

**2️⃣ Create a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

**3️⃣ Install dependencies:**
```bash
pip install -r requirements.txt
```

> 💡 **Tip**: Ensure your virtual environment is activated before installing dependencies!

---

## ⚙️ Configuration

### Settings Configuration

Main settings are located in `server/settings.py`. Key configurations to update:

#### SQLite Configuration (Default - Development)
```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL Configuration (Recommended - Production)
```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hometri_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Other Key Settings
```python
# Allowed Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Static Files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media Files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Bootstrap (already included in templates)
# Ensure Bootstrap CSS/JS are loaded in your base template
```

### Environment Variables

For production, use environment variables for sensitive data:

```bash
# Create a .env file
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/hometri_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

> ⚠️ **Security**: Never commit your `.env` file or expose your `SECRET_KEY`!

### PostgreSQL Setup

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS (using Homebrew)
brew install postgresql

# Windows
# Download installer from postgresql.org
```

**Create Database:**
```bash
# Access PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE hometri_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE hometri_db TO your_db_user;
\q
```

**Install psycopg2:**
```bash
pip install psycopg2-binary
```

---

## 🗄️ Database Migrations

Set up your database with these commands:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### Migration Tips
- Run migrations after every model change
- Check migration status: `python manage.py showmigrations`
- Rollback if needed: `python manage.py migrate <app_name> <migration_name>`

---

## ▶️ Running the Project

Start the development server:

```bash
python manage.py runserver
```

**🌐 Access your application:**
- Main site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### Custom Port
```bash
python manage.py runserver 8080
```

### Network Access
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📦 Static & Media Files

### Static Files Management

**Development:**
- Place static assets in `hometri/static/` or app-specific static folders
- Django automatically serves them in DEBUG mode
- Bootstrap is integrated via CDN or local files

**Production:**
```bash
# Collect all static files
python manage.py collectstatic

# Answer 'yes' to confirm
```

Configuration in `settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Bootstrap Integration

Bootstrap is included in the project for responsive UI design:

```html
<!-- In your base template -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

### Media Files Management

Uploaded files are stored in `media/` directory.

Configuration:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Ensure `MEDIA_ROOT` and `MEDIA_URL` are properly configured in your settings!

---

## 👨‍💼 Admin Panel

### Accessing the Admin Panel

**URL:** `/admin/`

### Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password

### Admin Features

- ✅ Custom admin templates in `hometri/templates/admin/`
- ✅ App-specific admin customizations
- ✅ User and permission management
- ✅ Model CRUD operations
- ✅ Bulk actions and filters

### Customization

Admin templates can be customized in:
- `hometri/templates/admin/` - Global admin templates
- `<app>/templates/admin/<app>/` - App-specific templates

---

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific App Tests

```bash
python manage.py test agents
python manage.py test team
python manage.py test users
```

### Test with Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Writing Tests

Tests are located in each app's `tests.py`:
```python
from django.test import TestCase

class AgentTestCase(TestCase):
    def test_agent_creation(self):
        # Your test code here
        pass
```

---

## 🖼️ Adding Images

### Image Gallery / Screenshots

Showcase the application with project screenshots. All images are from the `/images` folder.

---

### 📸 Project Demo Overview

![Project Demo](images/demo.png)
*Project demo overview*

---

### 🏠 Home Page

![Home Page 1](images/home/1.png)
![Home Page 2](images/home/2.png)
![Home Page 3](images/home/3.png)
![Home Page 4](images/home/4.png)
![Home Page 5](images/home/5.png)
![Home Page 6](images/home/6.png)
![Home Page 7](images/home/7.png)

---

### 📖 About Page

![About Page 1](images/about/1.png)
![About Page 2](images/about/2.png)
![About Page 3](images/about/3.png)
![About Page 4](images/about/4.png)
![About Page 5](images/about/5.png)
![About Page 6](images/about/6.png)
![About Page 7](images/about/7.png)

---

### 🔧 Admin Panel

![Admin Panel 1](images/admin/1.png)
![Admin Panel 2](images/admin/2.png)
![Admin Panel 3](images/admin/3.png)
![Admin Panel 4](images/admin/4.png)
![Admin Panel 5](images/admin/5.png)
![Admin Panel 6](images/admin/6.png)
![Admin Panel 7](images/admin/7.png)
![Admin Panel 8](images/admin/8.png)
![Admin Panel 9](images/admin/9.png)
![Admin Panel 11](images/admin/11.png)
![Admin Panel 12](images/admin/12.png)
![Admin Panel 13](images/admin/13.png)
![Admin Panel 14](images/admin/14.png)

---

### 🏢 Hometri Admin

![Hometri Admin 1](images/Hometri-admin/1.png)
![Hometri Admin 2](images/Hometri-admin/2.png)
![Hometri Admin 3](images/Hometri-admin/3.png)
![Hometri Admin 4](images/Hometri-admin/4.png)
![Hometri Admin 5](images/Hometri-admin/5.png)
![Hometri Admin 6](images/Hometri-admin/6.png)
![Hometri Admin 7](images/Hometri-admin/7.png)
![Hometri Admin 8](images/Hometri-admin/8.png)

---

### 👥 Agents - Admin Side

![Agents Admin 1](images/agents/admin-side/1.png)
![Agents Admin 2](images/agents/admin-side/2.png)
![Agents Admin 3](images/agents/admin-side/3.png)
![Agents Admin 4](images/agents/admin-side/4.png)
![Agents Admin 5](images/agents/admin-side/5.png)
![Agents Admin 6](images/agents/admin-side/6.png)
![Agents Admin 7](images/agents/admin-side/7.png)
![Agents Admin 8](images/agents/admin-side/8.png)
![Agents Admin 9](images/agents/admin-side/9.png)
![Agents Admin 10](images/agents/admin-side/10.png)
![Agents Admin 11](images/agents/admin-side/11.png)
![Agents Admin 12](images/agents/admin-side/12.png)
![Agents Admin 13](images/agents/admin-side/13.png)
![Agents Admin 14](images/agents/admin-side/14.png)
![Agents Admin 15](images/agents/admin-side/15.png)
![Agents Admin 16](images/agents/admin-side/16.png)
![Agents Admin 17](images/agents/admin-side/17.png)
![Agents Admin 18](images/agents/admin-side/18.png)

---

### 👥 Agents - Client Side

![Agents Client 1](images/agents/clinet-side/1.png)
![Agents Client 2](images/agents/clinet-side/2.png)
![Agents Client 3](images/agents/clinet-side/3.png)
![Agents Client 4](images/agents/clinet-side/4.png)
![Agents Client 5](images/agents/clinet-side/5.png)
![Agents Client 6](images/agents/clinet-side/6.png)
![Agents Client 7](images/agents/clinet-side/7.png)
![Agents Client 8](images/agents/clinet-side/8.png)
![Agents Client 9](images/agents/clinet-side/9.png)
![Agents Client 10](images/agents/clinet-side/10.png)
![Agents Client 11](images/agents/clinet-side/11.png)

---

### 📞 Contact - Admin Side

![Contact Admin 1](images/contact/admin-side/1.png)
![Contact Admin 2](images/contact/admin-side/2.png)
![Contact Admin 3](images/contact/admin-side/3.png)
![Contact Admin 4](images/contact/admin-side/4.png)

---

### 📞 Contact - Client Side

![Contact Client 1](images/contact/clinet-side/1.png)
![Contact Client 2](images/contact/clinet-side/2.png)
![Contact Client 3](images/contact/clinet-side/3.png)

---

### 🏘️ Property - Admin Side

![Property Admin 1](images/property/admin-side/1.png)
![Property Admin 2](images/property/admin-side/2.png)
![Property Admin 3](images/property/admin-side/3.png)
![Property Admin 4](images/property/admin-side/4.png)
![Property Admin 5](images/property/admin-side/5.png)
![Property Admin 6](images/property/admin-side/6.png)

---

### 🏘️ Property - Client Side

![Property Client 1](images/property/client-side/1.png)
![Property Client 2](images/property/client-side/2.png)
![Property Client 3](images/property/client-side/3.png)
![Property Client 4](images/property/client-side/4.png)
![Property Client 5](images/property/client-side/5.png)
![Property Client 6](images/property/client-side/6.png)
![Property Client 7](images/property/client-side/7.png)

---

### 🔍 Search Functionality

![Search 1](images/search/1.png)
![Search 2](images/search/2.png)
![Search 3](images/search/3.png)

---

### 🛠️ Services

![Services 1](images/services/1.png)
![Services 2](images/services/2.png)
![Services 3](images/services/3.png)
![Services 4](images/services/4.png)
![Services 5](images/services/5.png)

---

### 👨‍👩‍👧‍👦 Team - Admin Side

![Team Admin 1](images/team/admin-side/1.png)
![Team Admin 2](images/team/admin-side/2.png)
![Team Admin 3](images/team/admin-side/3.png)
![Team Admin 4](images/team/admin-side/4.png)
![Team Admin 5](images/team/admin-side/5.png)
![Team Admin 6](images/team/admin-side/6.png)
![Team Admin 7](images/team/admin-side/7.png)
![Team Admin 8](images/team/admin-side/8.png)
![Team Admin 9](images/team/admin-side/9.png)
![Team Admin 10](images/team/admin-side/10.png)
![Team Admin 11](images/team/admin-side/11.png)
![Team Admin 12](images/team/admin-side/12.png)
![Team Admin 13](images/team/admin-side/13.png)
![Team Admin 14](images/team/admin-side/14.png)
![Team Admin 15](images/team/admin-side/15.png)
![Team Admin 16](images/team/admin-side/16.png)

---

### 👨‍👩‍👧‍👦 Team - Client Side

![Team Client 1](images/team/clinet-side/1.png)
![Team Client 2](images/team/clinet-side/2.png)
![Team Client 3](images/team/clinet-side/3.png)
![Team Client 4](images/team/clinet-side/4.png)
![Team Client 5](images/team/clinet-side/5.png)
![Team Client 6](images/team/clinet-side/6.png)
![Team Client 7](images/team/clinet-side/7.png)
![Team Client 8](images/team/clinet-side/8.png)
![Team Client 9](images/team/clinet-side/9.png)
![Team Client 10](images/team/clinet-side/10.png)

---

### 🏗️ Architecture Diagram

```mermaid
%%{ init: { "theme": "neutral" } }%%

graph TD

    A[👤 User Request] --> B[🌐 server/urls.py]

    B --> C1[📁 agents/urls.py]
    B --> C2[📁 hometri/urls.py]
    B --> C3[📁 team/urls.py]
    B --> C4[📁 users/urls.py]

    C1 --> D1[🧠 agents/views.py]
    C2 --> D2[🧠 hometri/views.py]
    C3 --> D3[🧠 team/views.py]
    C4 --> D4[🧠 users/views.py]

    D1 --> E1[🗃️ agents/models.py]
    D2 --> E2[🗃️ hometri/models.py]
    D3 --> E3[🗃️ team/models.py]
    D4 --> E4[🗃️ users/models.py]

    E1 --> G1[(💾 db.sqlite3)]
    E2 --> G1
    E3 --> G1
    D4 --> G1

    E1 --> G2[(🐘 PostgreSQL)]
    E2 --> G2
    E3 --> G2
    D4 --> G2

    E1 --> F1[🖼️ agents/templates/]
    E2 --> F2[🖼️ hometri/templates/]
    E3 --> F3[🖼️ team/templates/]
    D4 --> F4[🖼️ users/templates/]

    B --> H1[📦 static/]
    B --> H2[🖇️ media/]

    classDef urls fill:#E3F2FD,stroke:#2196F3,stroke-width:1px;
    classDef views fill:#FFF3E0,stroke:#FF9800,stroke-width:1px;
    classDef models fill:#E8F5E9,stroke:#4CAF50,stroke-width:1px;
    classDef templates fill:#F3E5F5,stroke:#9C27B0,stroke-width:1px;
    classDef database fill:#E0F7FA,stroke:#0288D1,stroke-width:2px;
    classDef static fill:#ECEFF1,stroke:#607D8B;
    classDef request fill:#FFEBEE,stroke:#D32F2F;

    class A request;
    class B,C1,C2,C3,C4 urls;
    class D1,D2,D3,D4 views;
    class E1,E2,E3,E4 models;
    class F1,F2,F3,F4 templates;
    class G1,G2 database;
    class H1,H2 static;
```
*System architecture overview*

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Contribution Workflow

**1️⃣ Fork the repository**
```bash
# Click 'Fork' button on GitHub
```

**2️⃣ Create a new branch**
```bash
git checkout -b feature/your-feature-name
```

**3️⃣ Make your changes**
- Write clean, documented code
- Follow PEP 8 style guidelines
- Add tests for new features

**4️⃣ Commit your changes**
```bash
git commit -am 'Add new feature: brief description'
```

**5️⃣ Push to your branch**
```bash
git push origin feature/your-feature-name
```

**6️⃣ Open a Pull Request**
- Go to the original repository
- Click 'New Pull Request'
- Describe your changes in detail

### Contribution Guidelines

- ✅ Write meaningful commit messages
- ✅ Update documentation for new features
- ✅ Ensure all tests pass
- ✅ Follow the existing code style
- ✅ Be respectful and collaborative

---

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---

## 👨‍💻 Author

### **Aman Anil**

💼 LinkedIn: [linkedin.com/in/spyberpolymath](https://linkedin.com/in/spyberpolymath)  
💻 GitHub: [@spyberpolymath](https://github.com/spyberpolymath)  
🐦 Twitter (X): [@spyberpolymath](https://x.com/spyberpolymath)  
🌐 Portfolio: [spyberpolymath.com](https://spyberpolymath.com)  
📧 Email: [projects@spyberpolymath.com](mailto:projects@spyberpolymath.com)

**Made with ❤️ and Python by Aman Anil**

---

<div align="center">

⭐ **Star this repository if you find it helpful!** ⭐

</div>