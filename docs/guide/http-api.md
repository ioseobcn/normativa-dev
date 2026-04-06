# API HTTP REST

`normativa` expone una API REST completa via FastAPI, con especificacion OpenAPI generada automaticamente. Compatible con ChatGPT Actions, Codex, Claude.ai web y cualquier cliente HTTP.

## Iniciar el servidor

```bash
# Instalacion
pip install normativa

# Iniciar en el puerto por defecto (8787)
normativa serve --mode http

# Puerto personalizado
normativa serve --mode http --port 9000

# Host personalizado (por defecto 0.0.0.0)
normativa serve --mode http --host 127.0.0.1 --port 8787
```

El servidor muestra al iniciar:

```
Iniciando API HTTP en http://0.0.0.0:8787
Documentacion: http://0.0.0.0:8787/docs
OpenAPI spec:  http://0.0.0.0:8787/api/openapi.json
```

---

## Endpoints

### General

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/` | Pagina de inicio y health check |
| GET | `/docs` | Documentacion interactiva (Swagger UI) |
| GET | `/redoc` | Documentacion alternativa (ReDoc) |
| GET | `/api/openapi.json` | Especificacion OpenAPI (JSON) |

### Dominios

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/api/dominios` | Lista todos los dominios tematicos |

### Busqueda

| Metodo | Endpoint | Parametros | Descripcion |
|---|---|---|---|
| GET | `/api/buscar` | `dominio`, `subtema`, `caso` | Busca por dominio tematico |
| GET | `/api/buscar/texto` | `q` (requerido), `limit`, `rango`, `departamento`, `fecha_desde`, `fecha_hasta`, `offset` | Busqueda texto libre |

### Normas

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/api/norma/{boe_id}/metadatos` | Metadatos completos |
| GET | `/api/norma/{boe_id}/analisis` | Materias y referencias cruzadas |
| GET | `/api/norma/{boe_id}/indice` | Tabla de contenidos |
| GET | `/api/norma/{boe_id}/articulo/{bloque}` | Texto de un articulo |
| GET | `/api/norma/{boe_id}/articulos` | Rango de articulos (`desde`, `hasta`, `max_bloques`) |

### Sumarios diarios

| Metodo | Endpoint | Parametros | Descripcion |
|---|---|---|---|
| GET | `/api/boe/sumario/{fecha}` | `seccion`, `departamento`, `dominio` | Sumario del BOE |
| GET | `/api/borme/sumario/{fecha}` | -- | Sumario del BORME |

### Datos auxiliares

| Metodo | Endpoint | Parametros | Descripcion |
|---|---|---|---|
| GET | `/api/auxiliar/{tipo}` | `buscar` | Datos de referencia (materias, departamentos, rangos, ambitos) |

---

## Ejemplos con curl

### Listar dominios tematicos

```bash
curl -s http://localhost:8787/api/dominios | python -m json.tool
```

### Buscar por dominio

```bash
# Legislacion fiscal sobre IVA
curl -s "http://localhost:8787/api/buscar?dominio=fiscal&subtema=iva"

# Legislacion laboral sobre despido
curl -s "http://localhost:8787/api/buscar?dominio=laboral&subtema=despido"

# Busqueda por caso de uso (sin especificar dominio)
curl -s "http://localhost:8787/api/buscar?caso=alquiler+vivienda+zona+tensionada"
```

### Busqueda texto libre

```bash
# Busqueda simple
curl -s "http://localhost:8787/api/buscar/texto?q=proteccion+datos+personales&limit=5"

# Con filtros
curl -s "http://localhost:8787/api/buscar/texto?q=impuesto&rango=Ley&limit=10"
```

### Leer un articulo

```bash
# Primero, obtener el indice
curl -s http://localhost:8787/api/norma/BOE-A-2014-12328/indice

# Leer el articulo 29 (tipo de gravamen IS)
curl -s http://localhost:8787/api/norma/BOE-A-2014-12328/articulo/a29
```

### Rango de articulos

```bash
curl -s "http://localhost:8787/api/norma/BOE-A-2014-12328/articulos?desde=a1&hasta=a5"
```

### Sumarios diarios

```bash
# Sumario BOE de hoy
curl -s http://localhost:8787/api/boe/sumario/2026-04-05

# Sumario BOE filtrado por dominio
curl -s "http://localhost:8787/api/boe/sumario/2026-04-05?dominio=laboral"

# Sumario BORME
curl -s http://localhost:8787/api/borme/sumario/2026-04-05
```

### Datos auxiliares

```bash
# Listar materias
curl -s http://localhost:8787/api/auxiliar/materias

# Buscar departamentos
curl -s "http://localhost:8787/api/auxiliar/departamentos?buscar=hacienda"

# Tipos de norma
curl -s http://localhost:8787/api/auxiliar/rangos
```

---

## Especificacion OpenAPI

La especificacion se genera automaticamente en:

```
http://localhost:8787/api/openapi.json
```

Esta especificacion es compatible con:

- **ChatGPT Actions** — importa directamente la URL
- **Codex (OpenAI)** — usa la spec para generar clientes
- **Postman** — importa como OpenAPI 3.1
- **Cualquier generador de clientes** (openapi-generator, etc.)

---

## Usar con ChatGPT Actions

Paso a paso para crear un GPT personalizado con acceso a legislacion espanola:

### 1. Despliega el servidor

El servidor debe ser accesible desde internet. Opciones:

- **Tunel local** con ngrok, cloudflared, etc.
- **VPS/Cloud** con Docker o systemd
- **Servicio cloud** (Railway, Render, Fly.io, etc.)

### 2. Configura la Action en ChatGPT

1. Ve a [chat.openai.com](https://chat.openai.com) > "Explorar GPTs" > "Crear"
2. En la pestana "Configurar", baja a "Acciones" > "Crear nueva accion"
3. En "Importar desde URL", pega:

    ```
    https://tu-servidor.com/api/openapi.json
    ```

4. ChatGPT cargara automaticamente los 11 endpoints
5. Prueba con: "Busca legislacion sobre proteccion de datos"

### 3. Instrucciones recomendadas para el GPT

```
Eres un asistente legal espanol. Usas la API de normativa para buscar
legislacion en el BOE. Patron de uso:

1. Usa /api/buscar con dominio tematico para encontrar normas relevantes
2. Usa /api/norma/{id}/indice para ver la estructura
3. Usa /api/norma/{id}/articulo/{bloque} para leer articulos concretos

Nunca cargues leyes completas. Siempre cita el articulo y la norma exacta.
```

---

## Usar con Codex

Codex puede consumir la API directamente via HTTP:

```python
import httpx

BASE = "http://localhost:8787"

# Buscar legislacion
r = httpx.get(f"{BASE}/api/buscar", params={"dominio": "fiscal", "subtema": "iva"})
print(r.json())

# Leer articulo
r = httpx.get(f"{BASE}/api/norma/BOE-A-2014-12328/articulo/a29")
print(r.json()["texto"])
```

---

## Configuracion CORS

Por defecto, CORS esta abierto (`allow_origins=["*"]`) para facilitar el desarrollo. Para produccion, edita `src/normativa/api.py` y restringe los origenes:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chat.openai.com",
        "https://tu-dominio.com",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

---

## Opciones de despliegue

### Local (desarrollo)

```bash
normativa serve --mode http --port 8787
```

### Docker

```dockerfile
FROM python:3.12-slim
RUN pip install normativa
EXPOSE 8787
CMD ["normativa", "serve", "--mode", "http", "--port", "8787"]
```

```bash
docker build -t normativa-api .
docker run -p 8787:8787 normativa-api
```

### systemd (servidor Linux)

```ini
[Unit]
Description=normativa HTTP API
After=network.target

[Service]
Type=simple
User=normativa
ExecStart=/usr/local/bin/normativa serve --mode http --port 8787
Restart=always

[Install]
WantedBy=multi-user.target
```

### Cloud (Railway, Render, Fly.io)

Crea un `Procfile`:

```
web: normativa serve --mode http --port $PORT
```

O usa el Dockerfile anterior. La mayoria de plataformas detectan automaticamente el Dockerfile.

---

## Manejo de errores

Todos los endpoints devuelven JSON. En caso de error:

```json
{
  "detail": "boe_id invalido: 'XXXX'. Debe empezar por 'BOE-'."
}
```

Codigos HTTP:

| Codigo | Significado |
|---|---|
| 200 | Respuesta correcta |
| 400 | Parametros invalidos o error de la herramienta |
| 422 | Error de validacion (parametros requeridos faltantes) |
| 500 | Error interno del servidor |
