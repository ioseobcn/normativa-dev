"""Herramienta de listado de dominios tematicos."""

from __future__ import annotations

from typing import Any

from normativa.domains import DOMINIOS, AVAILABLE_DOMAINS


async def listar_dominios() -> dict[str, Any]:
    """Lista todos los dominios tematicos disponibles con su descripcion.

    Cada dominio agrupa legislacion por area juridica (laboral, fiscal, penal, etc.)
    y permite buscar sin conocer la terminologia exacta del BOE.

    Los dominios con datos enriquecidos incluyen leyes clave con articulos
    de referencia. Usa buscar_por_dominio() con la clave del dominio.

    Devuelve: lista de dominios con clave, nombre, descripcion y subtemas disponibles.
    """
    try:
        dominios = []
        for clave, dom in DOMINIOS.items():
            entry: dict[str, Any] = {
                "clave": clave,
                "nombre": dom["nombre"],
                "descripcion": dom["descripcion"],
                "subtemas": list(dom.get("subtemas", {}).keys()),
            }

            # Enriquecer con leyes clave del DomainConfig si existe
            if clave in AVAILABLE_DOMAINS:
                try:
                    from normativa.registry import load_domain
                    cfg = load_domain(clave)
                    entry["leyes_clave"] = [
                        {"boe_id": boe_id, "nombre": ley.nombre_corto}
                        for boe_id, ley in cfg.leyes_clave.items()
                    ]
                    entry["enriquecido"] = True
                except Exception:
                    entry["enriquecido"] = False
            else:
                entry["enriquecido"] = False

            dominios.append(entry)

        return {
            "total": len(dominios),
            "dominios": dominios,
        }
    except Exception as exc:
        return {"error": str(exc), "tool": "listar_dominios", "dominios": []}
