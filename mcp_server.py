import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HMS.settings")

import django

django.setup()

from asgiref.sync import sync_to_async
from mcp.server.fastmcp import FastMCP

from home.models import Booking, dept, doctor

mcp = FastMCP("Hospital Management System")


@sync_to_async
def get_departments() -> list[dict[str, object]]:
    return [
        {
            "id": department.id,
            "name": department.dept_name,
            "description": department.dept_desc,
        }
        for department in dept.objects.order_by("dept_name")
    ]


@sync_to_async
def get_doctors() -> list[dict[str, object]]:
    return [
        {
            "id": item.id,
            "name": item.doctor_name,
            "specialization": item.specialization,
            "department": item.dept_name.dept_name,
            "description": item.doctor_desc,
        }
        for item in doctor.objects.select_related("dept_name").order_by("doctor_name")[:50]
    ]


@sync_to_async
def get_appointment_count() -> int:
    return Booking.objects.count()


@mcp.tool()
async def list_departments() -> str:
    """List hospital departments and their descriptions."""
    departments = await get_departments()
    return json.dumps(departments)


@mcp.tool()
async def list_doctors() -> str:
    """List up to 50 doctors with their specialties and departments."""
    doctors = await get_doctors()
    return json.dumps(doctors)


@mcp.tool()
async def count_appointments() -> str:
    """Count appointment records without exposing patient details."""
    total = await get_appointment_count()
    return json.dumps({"total_appointments": total})


if __name__ == "__main__":
    mcp.run(transport="stdio")
