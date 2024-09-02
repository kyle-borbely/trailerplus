from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ObjectDoesNotExist

ENGLISH = "EN"
SPANISH = "ES"
LANGUAGE_CHOICES = [
    (ENGLISH, "English"),
    (SPANISH, "Spanish"),
]


def DEFAULT_WORK_HOURS():
    return {
        "sunday_hours": None,
        "monday_hours": None,
        "tuesday_hours": None,
        "wednesday_hours": None,
        "thursday_hours": None,
        "friday_hours": None,
        "saturday_hours": None,
    }


class SecondDbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()

        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, "use_db"):
            qs = qs.using(self.model.use_db)

        return qs


class SecondDbBase(models.Model):
    use_db = "default"
    objects = SecondDbManager()

    class Meta:
        abstract = True


class Trailer(SecondDbBase):
    vin = models.CharField("VIN number", max_length=21, primary_key=True)
    store = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Trailer's location",
    )
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Trailer's type", null=True
    )
    # primary_web_category = models.CharField('Web Category', max_length=255)
    # ToDo Signal to set up
    order_number = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    cash_price = models.CharField(max_length=45, null=True, blank=True)
    calculated_cash_price = models.CharField(max_length=45, null=True, blank=True)
    msrp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    width = models.CharField(max_length=5, null=True, blank=True)
    length = models.CharField(max_length=5, null=True, blank=True)
    gvwr = models.IntegerField(null=True, blank=True)
    gawr = models.IntegerField(null=True, blank=True)
    empty_weight = models.IntegerField(null=True, blank=True)
    overall_height = models.IntegerField(null=True, blank=True)
    overall_length = models.IntegerField(null=True, blank=True)
    overall_width = models.IntegerField(null=True, blank=True)
    interior_height = models.IntegerField(null=True, blank=True)
    interior_length = models.IntegerField(null=True, blank=True)
    interior_width = models.IntegerField(null=True, blank=True)
    rear_door_height = models.IntegerField(null=True, blank=True)
    rear_door_width = models.IntegerField(null=True, blank=True)
    platform_height = models.IntegerField(null=True, blank=True)
    hitch_height = models.IntegerField(null=True, blank=True)
    frame_centers = models.IntegerField(null=True, blank=True)
    roof_centers = models.IntegerField(null=True, blank=True)
    wall_centers = models.IntegerField(null=True, blank=True)
    axles = models.IntegerField(null=True, blank=True)
    stone_guard = models.IntegerField(null=True, blank=True)
    door_type = models.CharField(max_length=50, null=True, blank=True)
    coupler = models.CharField(max_length=25, null=True, blank=True)
    coupler_size = models.CharField(max_length=255, null=True, blank=True)

    sale_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    year = models.CharField(max_length=45, null=True, blank=True)
    model = models.CharField(max_length=45, null=True, blank=True)

    pictures = ArrayField(JSONField(), verbose_name="Pictures list", null=True)

    def __str__(self):
        return self.vin

    class Meta:
        ordering = ['sale_price']


class TrailerTranslation(SecondDbBase):
    trailer = models.ForeignKey(
        Trailer, on_delete=models.CASCADE, verbose_name="Related trailer"
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH)

    actual_color = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    axle_warranty = models.CharField(max_length=255, null=True, blank=True)
    roof_warranty = models.CharField(max_length=255, null=True, blank=True)
    warranty = models.CharField(max_length=255, null=True, blank=True)
    tires = models.CharField(max_length=255, null=True, blank=True)
    wheels = models.CharField(max_length=255, null=True, blank=True)
    doors = models.CharField(max_length=75, null=True, blank=True)
    stabilizer_jacks = models.CharField(max_length=255, null=True, blank=True)
    side_door = models.CharField(max_length=255, null=True, blank=True)
    rear_door = models.CharField(max_length=255, null=True, blank=True)
    side_walls = models.CharField(max_length=255, null=True, blank=True)
    suspension = models.CharField(max_length=255, null=True, blank=True)
    frame = models.CharField(max_length=255, null=True, blank=True)
    brakes = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)
    clearance_lights = models.CharField(max_length=255, null=True, blank=True)
    tail_lights = models.CharField(max_length=255, null=True, blank=True)
    protected_undercarriage = models.CharField(max_length=255, null=True, blank=True)

    long_description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=50, blank=True, null=True)
    package = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language} {self.trailer.vin}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["language", "trailer_id"], name="unique_translation"
            )
        ]
        verbose_name = "Trailer's translation"
        verbose_name_plural = "Trailers' translations"


class Location(SecondDbBase):
    STATE_CHOICES = [
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
        ("DC", "District of Columbia"),
        ("MH", "Marshall Islands"),
    ]
    store_id = models.CharField(max_length=100, primary_key=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    active = models.BooleanField(default=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_city = models.CharField(max_length=100, null=True, blank=True)
    store_address = models.CharField(max_length=500, null=True, blank=True)
    store_zip = models.IntegerField(null=True, blank=True)
    store_directions = models.TextField(null=True, blank=True)
    store_spanish_directions = models.TextField(null=True, blank=True)
    store_email = models.EmailField(max_length=255, null=True, blank=True)
    store_map_url = models.URLField(max_length=500, null=True, blank=True)
    store_phone = models.CharField(max_length=45, null=True, blank=True)
    store_keywords = ArrayField(models.CharField(max_length=45))
    store_lat = models.CharField(max_length=45, null=True, blank=True)
    store_long = models.CharField(max_length=45, null=True, blank=True)
    store_description = models.CharField(max_length=255, null=True, blank=True)
    store_title = models.CharField(max_length=255, null=True, blank=True)
    work_hours = JSONField(default=DEFAULT_WORK_HOURS)

    def get_city_name(self):
        return self.store_name.replace('TrailersPlus ', '')

    def get_slug(self):
        try:
            return self.pages.first().get_slug()
        except (ObjectDoesNotExist, AttributeError):
            return ''

    def __str__(self):
        return f'{self.get_city_name()}({self.store_city}), {self.state}'


class CategoryFilter(models.Model):
    FILTER_CHOICES = [
        ("exact", "Exact"),
        ("contains", "Contains"),
        ("startswith", "Starts With"),
        ("endswith", "Ends With"),
        ("regex", "Regex"),
    ]
    FIELDS_CHOICES = [
        ("category__web_category", "Web Category"),
        ("coupler", "Coupler"),
    ]
    case_sensitive = models.BooleanField('Case Sensitive?')
    type = models.CharField(max_length=15, choices=FILTER_CHOICES, help_text="SQL Regex https://dataschool.com/how-to-teach-people-sql/how-regex-works-in-sql/")
    field_name = models.CharField(max_length=25, choices=FIELDS_CHOICES, null=False, blank=False, default='category__web_category__')
    filter = models.CharField(max_length=25)

    def __str__(self):
        name = f"{self.get_type_display()} {self.filter}"
        if self.case_sensitive:
            name += " | CS"
        return name

    class Meta:
        verbose_name = "Category Filter"
        verbose_name_plural = "Category Filters"


class CategoryMap(models.Model):
    name_en = models.CharField(max_length=25)
    name_es = models.CharField(max_length=30)
    slug = models.SlugField(max_length=25, unique=True)
    include = models.ManyToManyField(CategoryFilter, related_name='include', blank=True)
    exclude = models.ManyToManyField(CategoryFilter, related_name='exclude', blank=True)
    order = models.IntegerField('Position in product list filter')
    translations = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.order} {self.name_en}"

    class Meta:
        verbose_name = "Category Map"
        verbose_name_plural = "Category Maps"
        ordering = ['order', 'slug']


class Category(SecondDbBase):
    web_category = models.CharField(max_length=25)
    base_type = models.CharField(max_length=255)


    primary = models.BooleanField("Is primary?", default=False)
    slug = models.CharField(max_length=255, null=True, blank=True)
    category_map = models.ForeignKey(CategoryMap, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Global Category")
    description = models.TextField(null=True, blank=True)
    keywords = ArrayField(models.CharField(max_length=25), null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["web_category", "base_type"], name="unique_category"
            )
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
