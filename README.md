# Acortador de enlaces en AWS

Midterm de Arquitectura en la Nube. Es una app para acortar enlaces que usa S3, EC2 y DynamoDB.

## Arquitectura
- **S3:** aloja el frontend (HTML, CSS y JS) como sitio web estático.
- **EC2:** corre la API hecha con FastAPI y Uvicorn en el puerto 8000. Usa systemd para que siga corriendo.
- **DynamoDB:** tabla `urls` con `short_code` como clave de partición.
- **IAM:** la EC2 tiene el rol `rol-ec2-acortador`, que solo deja hacer `PutItem` y `GetItem` en la tabla. No hay claves de AWS en el código.

## Endpoints
| Método | Ruta | Qué hace |
|---|---|---|
| POST | `/shorten` | Genera el UUID, guarda el enlace en DynamoDB y devuelve el enlace corto |
| GET | `/{short_code}` | Busca el enlace y redirige con 307 (404 si no existe) |
| GET | `/urls/{short_code}` | Devuelve la info del enlace en JSON (404 si no existe) |

## Estructura
```
backend/            API (main.py, db.py, requirements.txt, .env.example)
frontend/           index.html, style.css, app.js
acortador.service   servicio de systemd para la EC2
```

## Cómo desplegar en la EC2 (Amazon Linux 2023)
```
sudo dnf install -y git python3.11
git clone https://github.com/Lean131X/acortador-aws.git
cd acortador-aws/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
sudo cp ../acortador.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now acortador
```

## Links
- Frontend: http://leandro-acortador-front.s3-website-us-east-1.amazonaws.com
- API: http://52.206.183.98:8000/docs
