from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from advertisement.models import Advertisement, Heading


class AdvertisementCreationTest(TestCase):
    def setUp(self) -> None:
        # url = reverse('advertisement_detail')
        # self.response = self.client.get(url)
        self.head = Heading.objects.create(
            name='Food booth'
        )
        self.adv_good = Advertisement.objects.create(
            title='Booth',
            content='Naukova street, great price',
            price=24_000_0.5,
            advertisements=self.head,
        )

    def test_creation(self):
        self.assertEqual(self.adv_good.title, 'Booth')

    def test_adv_dont_have_negative_price(self):
        adv = Advertisement(title='Joe', content='Helol', price=2444.0, advertisements=self.head)
        adv.full_clean()

        adv.price = -2324324.0
        self.assertRaises(ValidationError, adv.full_clean)

    def test_adv_with_empty_title(self):
        self.adv_good.full_clean()
        self.adv_good.title = ''
        self.assertRaises(ValidationError, self.adv_good.full_clean)