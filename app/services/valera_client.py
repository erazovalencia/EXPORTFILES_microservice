import os
from typing import Any, Dict, List
import requests


def _get_base_url() -> str:
    base = os.getenv("VALERA_API", "http://localhost:3000/api/")
    return base.rstrip("/")


def get_reports() -> List[Dict[str, Any]]:
    """Obtiene todos los reportes LORA desde la API VALERA"""
    url = f"{_get_base_url()}/lora-report"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_report_by_id(report_id: int) -> Dict[str, Any]:
    """Obtiene un reporte LORA por ID desde la API VALERA"""
    url = f"{_get_base_url()}/lora-report/{report_id}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

