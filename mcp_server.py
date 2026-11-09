import os
import sys
import json
from pathlib import Path
from asgiref.sync import sync_to_async
from django.db.models import F

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "hms.settings"
)

import django
django.setup()

from mcp.server.fastmcp import FastMCP
from home.models import dpt, doctors, book_appointment

mcp = FastMCP("Hospital Management Server")


@sync_to_async
def get_departments():
    return list(dpt.objects.values("id", "department_name", "dpt_description"))


@sync_to_async
def get_doctors(department_id=None):
    queryset = doctors.objects.select_related("department_name")
    if department_id is not None:
        queryset = queryset.filter(department_name_id=department_id)

    return [
        {
            "id": doctor.id,
            "name": doctor.doctor_name,
            "specialization": doctor.doctor_specialization,
            "department": doctor.department_name.department_name,
            "image": doctor.doctor_image.url if doctor.doctor_image else None,
        }
        for doctor in queryset.order_by("doctor_name")[:50]
    ]


@sync_to_async
def get_appointment_count():
    return book_appointment.objects.count()


@mcp.tool()
async def list_departments() -> str:
    """List all hospital departments and their descriptions."""
    departments = await get_departments()
    return json.dumps({"departments": departments}, default=str)


@mcp.tool()
async def list_doctors(department_id: int | None = None) -> str:
    """List registered doctors, optionally filtered by department ID."""
    doctor_list = await get_doctors(department_id)
    return json.dumps({"doctors": doctor_list}, default=str)


@mcp.tool()
async def count_appointments() -> str:
    """Count appointment records without exposing patient details."""
    total = await get_appointment_count()
    return json.dumps({"total_appointments": total})


if __name__ == "__main__":
    mcp.run(transport="stdio")