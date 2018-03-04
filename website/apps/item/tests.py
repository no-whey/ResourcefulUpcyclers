from django.test import TestCase
from .models import *
from website.apps.profiles.models import *
from website.apps.item.models import *
from django.contrib.auth.models import User
import random
# Create your tests here.

class testDonations(TestCase):


    def testSetUp(self):

        NUM_OF_DONATIONS = 100

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

        user_list = []
        for i in range(NUM_OF_DONATIONS):
            user_list.append(User.objects.create(username="testuser"+str(i),
                                                 first_name="first"+str(i),
                                                 last_name="last"+str(i),
                                                 email="testuser"+str(i)+"@example.com"))

        for i in range(NUM_OF_DONATIONS):
            donor = random.choice(user_list)
            Donation.objects.create(name = random.choice(name_list),
                                    text_description = random.choice(text_description_list),
                                    quantity = random.randint(1, 100),
                                    img_link = random.choice(img_link_list),
                                    city = random.choice(city_list),
                                    donor = donor,
                                    donor_email = donor.email,
                                    needs_pickup = bool(random.getrandbits(1))
                                    )

    def testTearDown(self):
        all_donations = Donation.objects.all()
        for donation in all_donations:
            donation.delete()

#Tests for Offers
class testOffers(TestCase):
    
    def testSetUp(self):
    
        NUM_OF_OFFERS = 100
        
        isPrivate = False
        
        names = ["Chair", "Desk", "Fridge", "Microphone", "The Planet Mars", "Puzzle Box", "Whiteboard",
                 "Bed", "Cheese"]
        
        locations = ["Over there", "Under the thing", "Behind the safe",
                     "In the ceiling", "Rack 2B Section A"]
        
        descriptions = ["A thing", "A cool thing", "A cooler thing", "A less cool thing", "Some stuff"]
        
        images = ["https://imgs.xkcd.com/comics/code_golf.png",
                  "https://imgs.xkcd.com/comics/the_simpsons.png",
                  "https://imgs.xkcd.com/comics/self_driving_issues.png",
                  "https://imgs.xkcd.com/comics/2018_cve_list.png",
                  "https://imgs.xkcd.com/comics/unification.png"]
        
        tag_list = ["old", "new", "red", "blue", "yellow", "scratched", "like new", "broken"]
        
        for i in range(NUM_OF_OFFERS):
            Inventory.objects.create(name = random.choice(names),
                                 price = i + 0.99,
                                 location = random.choice(locations),
                                 text_description = random.choice(descriptions),
                                 img_link = random.choice(images),
                                 quantity = i,
                                 private = isPrivate,
                                 tag_pile = random.choice(tag_list),
                                 )
            isPrivate = not isPrivate
    
    def testTearDown(self):
        all_offers = Inventory.objects.all()
        for offer in all_offers:
            offer.delete()
    
    
    
    
    
    