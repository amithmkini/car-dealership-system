from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files import File
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .models import Car, TestDrive, Order


# Create your tests here.
class RegistrationTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(RegistrationTestCase, self).setUp()
        self.url = self.live_server_url + reverse('web:register')

    def tearDown(self):
        self.selenium.quit()
        super(RegistrationTestCase, self).tearDown()

    # With correct details
    def test_register(self):
        selenium = self.selenium
        selenium.get(self.url)
        print("\nTesting the registration system")

        # Now open the link for registration
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        email = selenium.find_element_by_id('id_email')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('register')

        first_name.send_keys('Test')
        last_name.send_keys('User')
        username.send_keys('testuser')
        email.send_keys('test@user.com')
        password.send_keys('testuser')

        # submitting the form
        submit.click()

        assert "Dashboard" in selenium.title

    # With existing username
    def test_register_blankuser(self):
        selenium = self.selenium

        # Do the registration
        user = User.objects.create_user(username="testuser", email="test@user.com", password="testuser")

        # Logout and repeat the test
        selenium.get(self.live_server_url + reverse('web:logout'))
        selenium.get(self.url)
        print("\nTesting with repeated user name")

        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        email = selenium.find_element_by_id('id_email')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('register')

        first_name.send_keys('Test')
        last_name.send_keys('User')
        username.send_keys('testuser')
        email.send_keys('test@user.com')
        password.send_keys('testuser')

        # submitting the form
        submit.click()

        self.assertInHTML("A user with that username already exists.", selenium.page_source)


class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(LoginTestCase, self).setUp()
        self.url = self.live_server_url + reverse('web:login')
        self.user = User.objects.create_user(username="testuser", email="test@user.com", password="testuser")

    def tearDown(self):
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_login(self): 
        print("\nRunning login test")
        selenium = self.selenium

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('testuser')
        submit.click()

        assert "Cars" in selenium.title
        self.assertInHTML(self.user.last_name, selenium.page_source)

    def test_invalid_login(self):
        print("\nTesting invalid logins")
        selenium = self.selenium

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        # Wrong username

        username.send_keys('wrong')
        password.send_keys('testuser')
        submit.click()

        self.assertEqual("Invalid login", selenium.find_element_by_id("error").text)

        # Wrong password

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('wrong')
        submit.click()

        self.assertEqual("Invalid login", selenium.find_element_by_id("error").text)

        # Blank details

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        username.send_keys('')
        password.send_keys('')
        submit.click()

        self.assertEqual("Invalid login", selenium.find_element_by_id("error").text)


class AdminCarTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', email='admin@admin.com', password='djangoadmin')
        self.user.is_active = True
        self.user.save()

    def tearDown(self):
        super(AdminCarTest, self).tearDown()

    def test_car_add(self):
        print("\nAdd car test...")
        user = self.user
        car = Car(
            picture=File(open(settings.BASE_DIR + '/web' + settings.STATIC_URL + 'images/car.jpg', 'r')),
            brand='Brand',
            name='Name',
            car_make='hatchback',
            price='65000',
            fuel='petrol',
            dimensions='100 x 100 x 100',
            transmission='Automatic',
            gears=5,
            seats=5,
            power=100,
            tank_capacity=100,
            engine_displacement=2000,
            added_by=user,
            description='Test car'
        )

        self.assertEqual(car.__str__(), "Brand Name")


class TestDriveTest(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.su = User.objects.create_superuser(username='admin', email='admin@admin.com', password='djangoadmin')
        self.su.is_active = True
        self.su.save()
        self.user = User.objects.create_superuser(username='testuser', email='test@user.com', password='testuser')
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.is_active = True
        self.user.save()
        super(TestDriveTest, self).setUp()
        # Create a car so that a view will be available
        car = Car.objects.create(
            picture=File(open(settings.BASE_DIR + '/media/car.jpg', 'rb')),
            brand='Brand',
            name='Name',
            car_make='hatchback',
            price='65000',
            fuel='petrol',
            dimensions='100 x 100 x 100',
            transmission='Automatic',
            gears=5,
            seats=5,
            power=100,
            tank_capacity=100,
            engine_displacement=2000,
            added_by=self.su,
            description='Test car',
        )

        self.pk = car.id
        self.url = self.live_server_url + reverse("web:details", args=[self.pk])
        # Login with the account
        self.selenium.get(self.live_server_url + reverse("web:login"))
        username = self.selenium.find_element_by_id('id_username')
        password = self.selenium.find_element_by_id('id_password')
        submit = self.selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('testuser')
        submit.click()

    def tearDown(self):
        self.selenium.quit()
        super(TestDriveTest, self).tearDown()

    def test_testdrive(self):
        print("\nTest drive button test...")
        selenium = self.selenium
        selenium.get(self.url)

        testdrive_btn = selenium.find_element_by_id("testdriveBtn")
        date_input = selenium.find_element_by_id("date-input")
        submit = selenium.find_element_by_id("regisBtn")

        testdrive_btn.click()
        date_input.send_keys("22/04/1997")
        submit.send_keys(Keys.ENTER)
        time.sleep(1)
        alert = selenium.switch_to.alert
        # self.assertEqual("Your testdrive has been booked!", alert.text)
        time.sleep(1)
        td = TestDrive.objects.get(user=self.user)
        self.assertEqual(td.__str__(), "Test User - Name")


class OrderTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.su = User.objects.create_superuser(username='admin', email='admin@admin.com', password='djangoadmin')
        self.su.is_active = True
        self.su.save()
        self.user = User.objects.create_superuser(username='testuser', email='test@user.com', password='testuser')
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.is_active = True
        self.user.save()
        super(OrderTest, self).setUp()
        # Create a car so that a view will be available
        car = Car.objects.create(
            picture=File(open(settings.BASE_DIR + '/media/car.jpg', 'rb')),
            brand='Brand',
            name='Name',
            car_make='hatchback',
            price='65000',
            fuel='petrol',
            dimensions='100 x 100 x 100',
            transmission='Automatic',
            gears=5,
            seats=5,
            power=100,
            tank_capacity=100,
            engine_displacement=2000,
            added_by=self.su,
            description='Test car',
        )

        self.pk = car.id
        self.url = self.live_server_url + reverse("web:details", args=[self.pk])
        # Login with the account
        self.selenium.get(self.live_server_url + reverse("web:login"))
        username = self.selenium.find_element_by_id('id_username')
        password = self.selenium.find_element_by_id('id_password')
        submit = self.selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('testuser')
        submit.click()

    def tearDown(self):
        self.selenium.quit()
        super(OrderTest, self).tearDown()

    def test_order(self):
        print("\nOrder button test...")
        selenium = self.selenium

        selenium.get(self.url)

        order_btn = selenium.find_element_by_id("orderBtn")
        address = selenium.find_element_by_id("address")
        submit = selenium.find_element_by_id("clickBtn")

        order_btn.click()
        address.send_keys("Address...")
        submit.send_keys(Keys.ENTER)
        time.sleep(1)
        alert = selenium.switch_to.alert
        time.sleep(1)
        td = Order.objects.get(user=self.user)
        self.assertEqual(td.__str__(), "Test User - Name")
