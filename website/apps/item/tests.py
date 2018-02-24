from django.test import TestCase
from website.apps.item.models import Donation, Inventory
from django.contrib.auth.models import User
import random
# Create your tests here.

class DonationTestCase(TestCase):
    name_list = ["Chairs", "Desks", "Copiers", "File Cabinets", "Mats and Rugs",
                "Paper Reams", "Pack of Pens", "Pencil Sharpeners", "3-ring Binders",
                "Lamps", "Microwave", "Break Room Tables", "Orange Traffic Cones",
                "Cubical Walls", "Computer Monitors", "Keyboards", "Mice",
                "Printers", "Scanners"]

    text_description_list = ["Very worn down, but it's got some life in it",
                            "Pretty much brand new, never needed to use it",
                            "Brown in color, slightly used, should last a while",
                            "Slightly wobbly, set it on a stable surface",
                            "Moving to a new office space, need to get rid of these soon!",
                            "Best ones I've ever used, please take them off my hands",
                            "This is an awful donation, please don't take it"]

    img_link_list = ["https://i.imgur.com/RYYovsj.jpg",
                    "https://i.redd.it/dc36qq2pa0i01.jpg",
                    "https://i.imgur.com/aYUBpcd.jpg",
                    "https://i.redd.it/ixtfx1wxzzh01.png"]

    city_list = ["Santa Cruz", "Capitola", "Scott's Valley", "Aptos"]

    user_list = list(User.objects.all())

    def setUp(self):
        for i in range(10):
            Donation.objects.create(name = random.choice(name_list),
                                    text_description = random.choice(text_description_list),
                                    quantity = random.randint(1, 100),
                                    img_link = random.choice(img_link_list),
                                    city = random.choice(city_list),
                                    donor = random.choice(user_list),
                                    donor_email = donor.email,
                                    needs_pickup = bool(random.getrandbits(1))
                                    )
