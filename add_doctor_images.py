import urllib.request
from pathlib import Path

from django.conf import settings
from home.models import doctor

# Save images inside media/doctors/
BASE_DIR = Path(settings.BASE_DIR)
MEDIA_ROOT = Path(settings.MEDIA_ROOT) if settings.MEDIA_ROOT else BASE_DIR / "media"

image_folder = MEDIA_ROOT / "doctors"
image_folder.mkdir(parents=True, exist_ok=True)

doctors = doctor.objects.order_by("id")
updated = 0
failed = 0

for index, doctor_record in enumerate(doctors, start=1):
    gender = "men" if index % 2 else "women"
    photo_id = ((index + 49) % 99) + 1

    image_name = f"doctor_{doctor_record.id}_portrait_v2.jpg"
    image_path = image_folder / image_name
    image_field_path = f"doctors/{image_name}"

    if doctor_record.doctors_image.name == image_field_path and image_path.is_file():
        print(f"Already has refreshed image: {doctor_record.doctor_name}")
        continue

    url = f"https://randomuser.me/api/portraits/{gender}/{photo_id}.jpg"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ClinicDemo/1.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            image_data = response.read()

        # Check that the response resembles a JPEG file
        if not image_data.startswith(b"\xff\xd8\xff"):
            raise ValueError("Downloaded file is not a JPEG image")

        image_path.write_bytes(image_data)

        # Store a path relative to MEDIA_ROOT
        doctor_record.doctors_image = image_field_path
        doctor_record.save(update_fields=["doctors_image"])

        updated += 1
        print(f"Added image: {doctor_record.doctor_name}")

    except Exception as error:
        failed += 1
        print(f"Failed: {doctor_record.doctor_name}: {error}")

print("\nImage assignment completed.")
print("New images:", updated)
print("Failed:", failed)
print("Doctors with images:", doctor.objects.exclude(doctors_image="").count())
print("Image folder:", image_folder)