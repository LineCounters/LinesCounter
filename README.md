# Lines Counter

- Versión recomendada de Python: 3.11

## Para correr la aplicación en desarrollo:

1. Crear el entorno de desarrollo:

```bash
python3 -m venv env
```

2. Activar el entorno de desarrollo:

En `Windows`:

```bash
env\Scripts\activate
```

En `Unix/Linux` o `MacOS`:

```bash
source env/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt

pre-commit install
```

4. Copiar el contenido del archivo `example.env` a un archivo `.env` y rellenar las variables necesarias para correr el proyecto.

```bash
cp example.env .env
```
