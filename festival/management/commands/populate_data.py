from django.core.management.base import BaseCommand
from festival.models import Building, Floor, Room


class Command(BaseCommand):
    help = "Populates the database with buildings, floors, and rooms"

    def handle(self, *args, **kwargs):
        # Define buildings and their respective number of floors
        buildings_data = {
            "Unit 1": 3,
            "Unit 2": 2,
            "Unit 3": 4,
            "Unit 4": 1,
            "Unit 5": 5,
        }

        for building_name, num_floors in buildings_data.items():
            # Create the building
            building, created = Building.objects.get_or_create(name=building_name)
            self.stdout.write(self.style.SUCCESS(f"Created Building: {building.name}"))

            # Create floors for the building
            for floor_number in range(1, num_floors + 1):
                floor, created = Floor.objects.get_or_create(
                    building=building, floor_number=floor_number
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created Floor: {floor.building.name} - Floor {floor.floor_number}"
                    )
                )

                # Create rooms for the floor
                for room_number in range(1, 21):  # 20 rooms per floor
                    room_number_str = f"{floor_number}{room_number:02d}"  # Room numbers like 101, 102, ..., 120, 201, etc.
                    Room.objects.get_or_create(floor=floor, room_number=room_number_str)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created Room: {floor.building.name} - Floor {floor.floor_number} - Room {room_number_str}"
                        )
                    )
