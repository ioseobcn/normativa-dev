# Transporte HTTP (desarrollo)

Documentacion tecnica del modulo `src/normativa/api.py` que expone las herramientas MCP como API REST via FastAPI.

## Arquitectura

El transporte HTTP es una capa delgada sobre las mismas funciones de herramientas que usa el servidor MCP:

```
Cliente HTTP  -->  FastAPI (api.py)  -->  tools/*.py  -->  BOE API
Cliente MCP   -->  FastMCP (server.py)  -->  tools/*.py  -->  BOE API
```

Ambos transportes reutilizan exactamente las mismas funciones async de `normativa.tools.*`. No hay duplicacion de logica.

## Estructura del modulo

El archivo `src/normativa/api.py` contiene:

1. **App FastAPI** — con metadatos para la especificacion OpenAPI
2. **Middleware CORS** — configurado para desarrollo (abierto)
3. **Endpoints** — cada uno llama a la funcion de herramienta correspondiente
4. **Manejador de errores** — convierte errores de herramientas en HTTP 400
5. **Landing page** — HTML simple con enlaces a documentacion

## Como envuelve las herramientas

Cada endpoint sigue el mismo patron:

```python
@app.get("/api/norma/{boe_id}/articulo/{bloque}", tags=["textos"])
async def api_leer_articulo(
    boe_id: str = Path(..., description="Identificador BOE"),
    bloque: str = Path(..., description="ID del bloque"),
):
    from normativa.tools.text import leer_articulo
    result = await leer_articulo(boe_id=boe_id, bloque_id=bloque)
    return _handle_error(result)
```

Pasos:

1. FastAPI valida y documenta los parametros (Path, Query)
2. Se importa la funcion de herramienta (lazy import para evitar dependencias circulares)
3. Se llama a la funcion async con los parametros mapeados
4. `_handle_error()` verifica si hay clave `"error"` en el resultado y lanza HTTP 400
5. FastAPI serializa el dict a JSON

## Anadir un nuevo endpoint

Para exponer una nueva herramienta como endpoint HTTP:

### 1. Crea la funcion de herramienta

En `src/normativa/tools/`, siguiendo el patron existente:

```python
# src/normativa/tools/mi_herramienta.py
async def mi_nueva_herramienta(param1: str, param2: int = 10) -> dict:
    """Descripcion de la herramienta."""
    try:
        # logica
        return {"resultado": "..."}
    except Exception as exc:
        return {"error": str(exc), "tool": "mi_nueva_herramienta"}
```

### 2. Registra en el servidor MCP

En `src/normativa/server.py`:

```python
from normativa.tools.mi_herramienta import mi_nueva_herramienta
mcp.tool()(mi_nueva_herramienta)
```

### 3. Anade el endpoint HTTP

En `src/normativa/api.py`:

```python
@app.get(
    "/api/mi-endpoint",
    summary="Descripcion corta",
    description="Descripcion larga para OpenAPI.",
    tags=["categoria"],
)
async def api_mi_herramienta(
    param1: str = Query(..., description="Primer parametro"),
    param2: int = Query(10, description="Segundo parametro"),
):
    from normativa.tools.mi_herramienta import mi_nueva_herramienta
    result = await mi_nueva_herramienta(param1=param1, param2=param2)
    return _handle_error(result)
```

### 4. Verifica

```bash
# Comprobar que la app carga
uv run python -c "from normativa.api import app; print(len(app.routes), 'routes')"

# Probar el endpoint
uv run normativa serve --mode http --port 8787 &
curl -s http://localhost:8787/api/mi-endpoint?param1=test
```

## Generacion OpenAPI

FastAPI genera la especificacion automaticamente en `/api/openapi.json`. Para que la documentacion sea util:

- Usa `summary` corto (aparece en listas)
- Usa `description` detallada (aparece al expandir)
- Usa `tags` para agrupar endpoints
- Usa `Query(description=...)` y `Path(description=...)` para documentar parametros
- Indica valores por defecto, minimos y maximos con `ge=`, `le=`, etc.

## Mapeo de parametros

| Fuente | FastAPI | Ejemplo |
|---|---|---|
| Path de URL | `Path(...)` | `/api/norma/{boe_id}` |
| Query string | `Query(...)` | `?dominio=fiscal&subtema=iva` |
| Body JSON | `Body(...)` | No usado (solo GET) |

Todos los endpoints son GET porque la API es de solo lectura.

## Manejo de errores

Las funciones de herramientas devuelven `{"error": "mensaje"}` cuando fallan. El helper `_handle_error()` convierte esto en una respuesta HTTP 400:

```python
def _handle_error(result: dict) -> dict:
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
```

Ademas, hay un manejador global para excepciones no controladas que devuelve HTTP 500.

## CORS

Configuracion actual (desarrollo):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Para produccion, restringe `allow_origins` a los dominios que necesites (ChatGPT usa `https://chat.openai.com`).

## Punto de entrada

El CLI maneja el inicio del servidor HTTP en `src/normativa/cli.py`:

```python
@main.command()
@click.option("--mode", type=click.Choice(["mcp", "http"]), default="mcp")
@click.option("--port", default=8787)
@click.option("--host", default="0.0.0.0")
def serve(mode, port, host):
    if mode == "http":
        import uvicorn
        uvicorn.run("normativa.api:app", host=host, port=port, log_level="info")
    else:
        from normativa.server import mcp
        mcp.run()
```

Uvicorn recibe la app como string (`"normativa.api:app"`) para soportar reload en desarrollo:

```bash
# Con auto-reload (desarrollo)
uvicorn normativa.api:app --reload --port 8787
```

## Tests

Para testear los endpoints HTTP, usa `httpx` con `TestClient` de FastAPI:

```python
from fastapi.testclient import TestClient
from normativa.api import app

client = TestClient(app)

def test_landing():
    r = client.get("/")
    assert r.status_code == 200
    assert "normativa" in r.text

def test_dominios():
    r = client.get("/api/dominios")
    assert r.status_code == 200
    data = r.json()
    assert "dominios" in data
```
