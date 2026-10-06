"""Registro de disponibilidad durante un periodo de evaluación (#25, RNF-03).

Uso, desde backend:

    python -m benchmarks.monitor_disponibilidad --url http://127.0.0.1:8000/salud \
        --intervalo 60 --duracion 3600 --salida disponibilidad.csv

Consulta /salud a intervalos fijos y guarda, por sondeo, fecha UTC, código HTTP,
estado y latencia; nunca datos de personas. Un sondeo cuenta como disponible si
responde 200 (estado ok o degradado) antes del tiempo límite. Criterio de
aceptación RNF-03: disponibilidad mayor o igual al 95 % del periodo.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UMBRAL_DISPONIBILIDAD = 95.0
CAMPOS = ["fecha_utc", "codigo", "estado", "latencia_ms"]


def sondear(url: str, limite_s: float = 5.0) -> dict:
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=limite_s) as respuesta:
            codigo = respuesta.status
            estado = json.loads(respuesta.read()).get("estado", "desconocido")
    except urllib.error.HTTPError as error:
        codigo, estado = error.code, "no_disponible"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        codigo, estado = 0, "sin_respuesta"
    return {
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "codigo": codigo,
        "estado": estado,
        "latencia_ms": round((time.perf_counter() - inicio) * 1000, 1),
    }


def resumir(registros: list[dict]) -> dict:
    total = len(registros)
    disponibles = sum(1 for r in registros if int(r["codigo"]) == 200)
    porcentaje = round(100 * disponibles / total, 2) if total else 0.0
    return {
        "sondeos": total,
        "disponibles": disponibles,
        "degradados": sum(1 for r in registros if r["estado"] == "degradado"),
        "disponibilidad_pct": porcentaje,
        "umbral_pct": UMBRAL_DISPONIBILIDAD,
        "cumple": total > 0 and porcentaje >= UMBRAL_DISPONIBILIDAD,
    }


def monitorear(url: str, intervalo_s: float, duracion_s: float, salida: Path | None) -> dict:
    registros = []
    fin = time.monotonic() + duracion_s
    archivo = salida.open("w", newline="", encoding="utf-8") if salida else None
    try:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS) if archivo else None
        if escritor:
            escritor.writeheader()
        while True:
            registro = sondear(url)
            registros.append(registro)
            if escritor:
                escritor.writerow(registro)
                archivo.flush()
            if time.monotonic() + intervalo_s > fin:
                break
            time.sleep(intervalo_s)
    finally:
        if archivo:
            archivo.close()
    return resumir(registros)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", default="http://127.0.0.1:8000/salud")
    parser.add_argument("--intervalo", type=float, default=60.0, help="segundos entre sondeos")
    parser.add_argument("--duracion", type=float, default=3600.0, help="segundos del periodo")
    parser.add_argument("--salida", type=Path, help="CSV con un registro por sondeo")
    args = parser.parse_args()

    resultado = monitorear(args.url, args.intervalo, args.duracion, args.salida)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if resultado["cumple"] else 1


if __name__ == "__main__":
    sys.exit(main())
