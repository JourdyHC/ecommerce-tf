from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('AMA', 'Amazonas'),
    ('ANC', 'Áncash'),
    ('APU', 'Apurímac'),
    ('ARE', 'Arequipa'),
    ('AYA', 'Ayacucho'),
    ('CAJ', 'Cajamarca'),
    ('CAL', 'Callao'),
    ('CUS', 'Cusco'),
    ('HUV', 'Huancavelica'),
    ('HUA', 'Huánuco'),
    ('ICA', 'Ica'),
    ('JUN', 'Junín'),
    ('LAL', 'La Libertad'),
    ('LAM', 'Lambayeque'),
    ('LIM', 'Lima'),
    ('LOR', 'Loreto'),
    ('MDD', 'Madre de Dios'),
    ('MOQ', 'Moquegua'),
    ('PAS', 'Pasco'),
    ('PIU', 'Piura'),
    ('PUN', 'Puno'),
    ('SAM', 'San Martín'),
    ('TAC', 'Tacna'),
    ('TUM', 'Tumbes'),
    ('UCA', 'Ucayali')
)

# Create your models here.

CATEGORY_CHOICES = (
    ("CR", "Curd"),
    ("ML", "Milk"),
    ("LS", "Lassi"),
    ("MS", "Milkshake"),
    ("PN", "Paneer"),
    ("GH", "Ghee"),
    ("CZ", "Cheese"),
    ("IC", "Ice-Creams")
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default="")
    prodapp = models.TextField(default="")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="product")

    def __str__(self) -> str:
        return self.title

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city= models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.Product.discounted_price