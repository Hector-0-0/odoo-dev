<div align="center">

# 🟣 Odoo Dev

![GitHub stars](https://img.shields.io/github/stars/Hector-0-0/odoo-dev?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/Hector-0-0/odoo-dev?style=flat-square)

**Colección de módulos personalizados para Odoo**

</div>

---

## 📋 Sobre el Proyecto

Repositorio de desarrollo con módulos personalizados para Odoo, enfocados en adaptaciones locales (Perú) y funcionalidades adicionales. Diseñado para documentar el desarrollo de módulos y servir de referencia a otros desarrolladores que trabajan con el framework de Odoo.

## 💻 Tecnologías

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Odoo](https://img.shields.io/badge/Odoo-714B67?style=flat&logo=odoo&logoColor=white)
![XML](https://img.shields.io/badge/XML-E34F26?style=flat&logo=xml&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)

## 📦 Módulos Disponibles

| Módulo | Descripción |
|--------|-------------|
| **l10n_pe_libro_reclamaciones** | Libro de reclamaciones para la localización peruana |

## 🗂️ Estructura del Proyecto

```
odoo-dev/
├── modulos/
│   └── nombre_modulo/
│       ├── models/          # Modelos de datos
│       ├── views/           # Vistas XML
│       ├── security/        # Reglas de acceso
│       ├── data/            # Datos iniciales
│       ├── controllers/     # Controladores HTTP
│       ├── static/          # Archivos estáticos (JS, CSS, img)
│       ├── __init__.py
│       └── __manifest__.py  # Metadatos del módulo
├── notas/                   # Apuntes y documentación
├── README.md
└── recursos.md
```

## 🚀 ¿Cómo usar este repo?

Clona el repositorio y copia el módulo que necesites dentro de tu carpeta de addons de Odoo:

```bash
git clone https://github.com/Hector-0-0/odoo-dev.git
cd odoo-dev

# Copiar un módulo a tu directorio de addons de Odoo
cp -r modulos/l10n_pe_libro_reclamaciones /ruta/a/tus/addons/
```

Luego activa el modo desarrollador en Odoo, actualiza la lista de aplicaciones e instala el módulo desde el menú de Aplicaciones.

## 👤 Autor

**Hector-0-0**
- GitHub: [@Hector-0-0](https://github.com/Hector-0-0)

---

<div align="center">
⭐ Si te fue útil, dale una estrella!
</div>
