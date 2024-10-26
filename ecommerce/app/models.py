from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('Amazonas'     , 'Amazonas'),
    ('Áncash'       , 'Áncash'),
    ('Apurímac'     , 'Apurímac'),
    ('Arequipa'     , 'Arequipa'),
    ('Ayacucho'     , 'Ayacucho'),
    ('Cajamarca'    , 'Cajamarca'),
    ('Callao'       , 'Callao'),
    ('Cusco'        , 'Cusco'),
    ('Huancavelica' , 'Huancavelica'),
    ('Huánuco'      , 'Huánuco'),
    ('Ica'          , 'Ica'),
    ('Junín'        , 'Junín'),
    ('La Libertad'  , 'La Libertad'),
    ('Lambayeque'   , 'Lambayeque'),
    ('Lima'         , 'Lima'),
    ('Loreto'       , 'Loreto'),
    ('Madre de Dios', 'Madre de Dios'),
    ('Moquegua'     , 'Moquegua'),
    ('Pasco'        , 'Pasco'),
    ('Piura'        , 'Piura'),
    ('Puno'         , 'Puno'),
    ('San Martín'   , 'San Martín'),
    ('Tacna'        , 'Tacna'),
    ('Tumbes'       , 'Tumbes'),
    ('Ucayali'      , 'Ucayali')
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

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
    )

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=3)
    description = models.TextField(null=True)
    category_image = models.ImageField(upload_to="category")
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default="")
    prodapp = models.TextField(default="")
    #category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=100, null=True)
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
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.Product.discounted_price
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price