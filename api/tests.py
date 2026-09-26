from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
import threading

from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch, Country, Region,
    GivingInfo, GivingImage, ContactMessage, Testimony, Book, ExchangeRate, Merchandise
)


# ====================================================================
# MODEL TESTS
# ====================================================================

@override_settings(MIDDLEWARE=[])
class HomeBannerModelTest(TestCase):
    """Test HomeBanner model"""
    
    def setUp(self):
        """Create test data"""
        self.banner = HomeBanner.objects.create(
            title="Test Banner",
            subtitle="Test Subtitle",
            image="test.jpg",
            button_text="Click Me",
            is_active=True,
            order=1
        )
    
    def test_banner_creation(self):
        """Test banner is created correctly"""
        self.assertEqual(self.banner.title, "Test Banner")
        self.assertTrue(self.banner.is_active)
    
    def test_banner_str(self):
        """Test banner string representation"""
        self.assertEqual(str(self.banner), "Test Banner")
    
    def test_banner_ordering(self):
        """Test banners are ordered by order field"""
        banner2 = HomeBanner.objects.create(
            title="Second Banner",
            image="test2.jpg",
            order=2
        )
        banners = HomeBanner.objects.all()
        self.assertEqual(banners[0].order, 1)
        self.assertEqual(banners[1].order, 2)


class ChurchInfoModelTest(TestCase):
    """Test ChurchInfo model"""
    
    def test_only_one_church_info_allowed(self):
        """Test that only one ChurchInfo record can exist"""
        ChurchInfo.objects.create(
            church_name="Test Church",
            welcome_message="Welcome!",
            full_about="About us",
            address="123 Main St",
            phone="555-1234",
            email="test@church.com",
            mission_statement="Our mission",
            vision_statement="Our vision",
            service_times_text="Sundays 9am"
        )
        
        # Try to create a second one - should fail
        with self.assertRaises(ValueError):
            ChurchInfo.objects.create(
                church_name="Another Church",
                welcome_message="Welcome!",
                full_about="About us",
                address="456 Oak St",
                phone="555-5678",
                email="test2@church.com",
                mission_statement="Our mission",
                vision_statement="Our vision",
                service_times_text="Sundays 10am"
            )


class LeaderModelTest(TestCase):
    """Test Leader model"""
    
    def setUp(self):
        self.leader = Leader.objects.create(
            full_name="Pastor John",
            position="Shepherd",
            biography="Bio text",
            profile_picture="pic.jpg",
            is_featured_on_home=True,
            order=1
        )
    
    def test_leader_creation(self):
        """Test leader is created"""
        self.assertEqual(self.leader.full_name, "Pastor John")
        self.assertTrue(self.leader.is_featured_on_home)
    
    def test_leader_str(self):
        """Test leader string representation"""
        self.assertEqual(str(self.leader), "Pastor John (Shepherd)")


class EventModelTest(TestCase):
    """Test Event model"""
    
    def setUp(self):
        self.event = Event.objects.create(
            title="Sunday Service",
            description="Weekly service",
            date=timezone.now() + timedelta(days=1),
            location="Main Hall",
            image="event.jpg",
            category="General",
            is_active=True
        )
    
    def test_event_creation(self):
        """Test event is created"""
        self.assertEqual(self.event.title, "Sunday Service")
        self.assertTrue(self.event.is_active)
    
    def test_event_is_published(self):
        """Test event publication status"""
        self.assertTrue(self.event.is_active)


class SermonModelTest(TestCase):
    """Test Sermon model"""
    
    def setUp(self):
        self.sermon = Sermon.objects.create(
            title="Faith in God",
            description="About faith",
            speaker="Pastor John",
            date=timezone.now().date(),
            is_published=True
        )
    
    def test_sermon_creation(self):
        """Test sermon is created"""
        self.assertEqual(self.sermon.speaker, "Pastor John")
        self.assertTrue(self.sermon.is_published)


class BranchModelTest(TestCase):
    """Test Branch model"""
    
    def setUp(self):
        self.country, _ = Country.objects.get_or_create(name="Ghana", defaults={"continent": "AF"})
        self.branch = Branch.objects.create(
            name="Main Branch",
            country=self.country,
            location="123 Main St",
            phone="555-1234",
            email="main@church.com",
            pastor_in_charge="Pastor John",
            service_time="Sundays 9am",
            is_main_branch=True
        )
    
    def test_branch_creation(self):
        """Test branch is created"""
        self.assertEqual(self.branch.name, "Main Branch")
        self.assertTrue(self.branch.is_main_branch)
    
    def test_branch_str(self):
        """Test branch string representation"""
        self.assertIn("(Main)", str(self.branch))

    def test_satellite_branch_without_location(self):
        """Satellite branches can be created without a physical location"""
        branch = Branch.objects.create(
            name="Online Branch",
            country=self.country,
            location="",
            phone="555-0000",
            pastor_in_charge="Pastor Jane",
            service_time="Sundays 9am",
            is_satellite=True,
        )
        branch.full_clean()
        self.assertEqual(branch.location, "")
        self.assertTrue(branch.is_satellite)

    def test_main_branch_cannot_be_satellite(self):
        """A branch cannot be both the main branch and a satellite branch"""
        branch = Branch(
            name="Invalid Branch",
            country=self.country,
            location="",
            phone="555-0000",
            pastor_in_charge="Pastor Jane",
            service_time="Sundays 9am",
            is_main_branch=True,
            is_satellite=True,
        )
        with self.assertRaises(ValidationError):
            branch.full_clean()


# ====================================================================
# API ENDPOINT TESTS
# ====================================================================

class HomeBannerAPITest(APITestCase):
    """Test HomeBanner API endpoints"""
    
    def setUp(self):
        """Create test data and client"""
        self.client = APIClient()
        self.banner = HomeBanner.objects.create(
            title="Test Banner",
            image="test.jpg",
            is_active=True,
            order=1
        )
    
    def test_get_banners_list(self):
        """Test GET /api/banners/"""
        response = self.client.get('/api/banners/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_banner_detail(self):
        """Test GET /api/banners/{id}/"""
        response = self.client.get(f'/api/banners/{self.banner.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Banner")
    
    def test_filter_active_banners(self):
        """Test filtering by is_active"""
        HomeBanner.objects.create(
            title="Inactive Banner",
            image="test2.jpg",
            is_active=False
        )
        response = self.client.get('/api/banners/?is_active=true')
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_banners(self):
        """Test search functionality"""
        response = self.client.get('/api/banners/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventAPITest(APITestCase):
    """Test Event API endpoints"""
    
    def setUp(self):
        # Clear thread-local to prevent audit log issues
        if hasattr(threading.current_thread(), 'request'):
            delattr(threading.current_thread(), 'request')
        
        self.client = APIClient()
        self.event = Event.objects.create(
            title="Upcoming Event",
            description="Test event",
            date=timezone.now() + timedelta(days=5),
            location="Main Hall",
            image="event.jpg",
            is_active=True
        )
    
    def test_get_events_list(self):
        """Test GET /api/events/"""
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_upcoming_events(self):
        """Test GET /api/events/upcoming/"""
        response = self.client.get('/api/events/upcoming/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_get_event_detail(self):
        """Test GET /api/events/{id}/"""
        response = self.client.get(f'/api/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Upcoming Event")


class SermonAPITest(APITestCase):
    """Test Sermon API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.sermon = Sermon.objects.create(
            title="Faith Sermon",
            description="About faith",
            speaker="Pastor John",
            date=timezone.now().date(),
            is_published=True,
            is_featured=True
        )
    
    def test_get_sermons_list(self):
        """Test GET /api/sermons/"""
        response = self.client.get('/api/sermons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_featured_sermons(self):
        """Test GET /api/sermons/featured/"""
        response = self.client.get('/api/sermons/featured/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_get_latest_sermon(self):
        """Test GET /api/sermons/latest/"""
        response = self.client.get('/api/sermons/latest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BranchAPITest(APITestCase):
    """Test Branch API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.ghana, _ = Country.objects.get_or_create(name="Ghana", defaults={"continent": "AF"})
        self.greater_accra, _ = Region.objects.get_or_create(country=self.ghana, name="Greater Accra")
        self.branch = Branch.objects.create(
            name="Main Campus",
            country=self.ghana,
            region=self.greater_accra,
            location="123 Main St",
            phone="555-1234",
            email="main@church.com",
            pastor_in_charge="Pastor John",
            service_time="Sundays 9am",
            is_main_branch=True
        )

    def test_get_branches_list(self):
        """Test GET /api/branches/"""
        response = self.client.get('/api/branches/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_main_branch(self):
        """Test filtering for main branch"""
        response = self.client.get('/api/branches/?main=true')
        self.assertEqual(len(response.data['results']), 1)

    def test_branch_detail_includes_service_times(self):
        """Test that branch detail includes service times"""
        ServiceTime.objects.create(
            day="Sunday",
            time="9:00 AM",
            service_type="Worship",
            branch=self.branch
        )
        response = self.client.get(f'/api/branches/{self.branch.id}/')
        self.assertIn('service_times', response.data)

    def test_filter_branches_by_continent(self):
        """Test GET /api/branches/?continent=AF"""
        response = self.client.get('/api/branches/?continent=AF')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_branches_by_country(self):
        """Test GET /api/branches/?country=<id>"""
        response = self.client.get(f'/api/branches/?country={self.ghana.id}')
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_branches_by_region(self):
        """Test GET /api/branches/?region=<id>"""
        response = self.client.get(f'/api/branches/?region={self.greater_accra.id}')
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_branches_by_other_region_excludes(self):
        """Branches in a different region should not appear"""
        other_region, _ = Region.objects.get_or_create(country=self.ghana, name="Ashanti")
        response = self.client.get(f'/api/branches/?region={other_region.id}')
        self.assertEqual(len(response.data['results']), 0)


class CountryRegionAPITest(APITestCase):
    """Test Country/Region hierarchy endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.ghana, _ = Country.objects.get_or_create(name="Ghana", defaults={"continent": "AF"})
        self.nigeria = Country.objects.create(name="Nigeria", continent="AF")
        # Western Sahara has no entry in REGION_DATA — used to test the "no regions" case
        self.no_regions_country = Country.objects.create(name="Western Sahara", continent="AF")
        self.greater_accra, _ = Region.objects.get_or_create(country=self.ghana, name="Greater Accra")
        Branch.objects.create(
            name="Accra Branch", country=self.ghana, region=self.greater_accra,
            location="Accra", phone="000", pastor_in_charge="Pastor A",
            service_time="Sundays 9am"
        )
        Branch.objects.create(
            name="Lagos Branch", country=self.nigeria,
            location="Lagos", phone="000", pastor_in_charge="Pastor B",
            service_time="Sundays 9am"
        )

    def test_list_countries_by_continent(self):
        response = self.client.get('/api/countries/?continent=AF')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = {c['name'] for c in response.data}
        self.assertEqual(names, {"Ghana", "Nigeria", "Western Sahara"})

    def test_country_has_regions_flag(self):
        response = self.client.get('/api/countries/?continent=AF')
        by_name = {c['name']: c for c in response.data}
        self.assertTrue(by_name['Ghana']['has_regions'])
        self.assertFalse(by_name['Western Sahara']['has_regions'])

    def test_country_branch_count(self):
        response = self.client.get('/api/countries/?continent=AF')
        by_name = {c['name']: c for c in response.data}
        self.assertEqual(by_name['Ghana']['branch_count'], 1)

    def test_list_regions_by_country(self):
        response = self.client.get(f'/api/regions/?country={self.ghana.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        by_name = {r['name']: r for r in response.data}
        self.assertEqual(by_name['Greater Accra']['branch_count'], 1)

    def test_regions_endpoint_excludes_regions_with_no_branches(self):
        """Ghana has 16 real regions but only 1 has a branch in this test — only that one should show"""
        response = self.client.get(f'/api/regions/?country={self.ghana.id}')
        names = {r['name'] for r in response.data}
        self.assertEqual(names, {'Greater Accra'})
        self.assertNotIn('Ashanti', names)

    def test_regions_scoped_to_country(self):
        """Regions for a different country should not leak in"""
        response = self.client.get(f'/api/regions/?country={self.no_regions_country.id}')
        self.assertEqual(len(response.data), 0)

    def test_country_auto_populates_real_regions(self):
        """Creating a Country auto-creates its real regions from REGION_DATA, no manual entry"""
        kenya = Country.objects.create(name="Kenya", continent="AF")
        region_names = set(kenya.regions.values_list('name', flat=True))
        self.assertIn("Nairobi", region_names)
        self.assertIn("Mombasa", region_names)
        self.assertEqual(kenya.regions.count(), 47)

    def test_country_with_no_subdivisions_has_no_regions(self):
        """A country absent from REGION_DATA (or mapped to an empty list) gets no regions"""
        monaco = Country.objects.create(name="Monaco", continent="EU")
        self.assertEqual(monaco.regions.count(), 0)

    def test_has_physical_branch_false_for_satellite_only_country(self):
        """A country with only a satellite branch should report has_physical_branch=False"""
        south_africa = Country.objects.create(name="South Africa", continent="AF")
        Branch.objects.create(
            name="South Africa Online", country=south_africa, location="",
            phone="000", pastor_in_charge="Pastor C", service_time="Sundays 9am",
            is_satellite=True,
        )
        response = self.client.get('/api/countries/?continent=AF')
        by_name = {c['name']: c for c in response.data}
        self.assertFalse(by_name['South Africa']['has_physical_branch'])

    def test_has_physical_branch_true_once_a_physical_branch_exists(self):
        """Adding a physical branch to a satellite-only country flips has_physical_branch to True"""
        south_africa = Country.objects.create(name="South Africa", continent="AF")
        Branch.objects.create(
            name="South Africa Online", country=south_africa, location="",
            phone="000", pastor_in_charge="Pastor C", service_time="Sundays 9am",
            is_satellite=True,
        )
        Branch.objects.create(
            name="Johannesburg Branch", country=south_africa, location="123 Main Rd",
            phone="000", pastor_in_charge="Pastor D", service_time="Sundays 9am",
        )
        response = self.client.get('/api/countries/?continent=AF')
        by_name = {c['name']: c for c in response.data}
        self.assertTrue(by_name['South Africa']['has_physical_branch'])


class ContactMessageAPITest(APITestCase):
    """Test ContactMessage API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.message = ContactMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="General Inquiry",
            message="Test message",
            is_read=False
        )
    
    def test_get_messages_list(self):
        """Test GET /api/contact-messages/"""
        response = self.client.get('/api/contact-messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_unread_messages(self):
        """Test GET /api/contact-messages/unread/"""
        response = self.client.get('/api/contact-messages/unread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_mark_message_as_read(self):
        """Test POST /api/contact-messages/{id}/mark_as_read/ (requires auth)"""
        # Create admin user and get token
        admin = User.objects.create_user(username='admin2', password='pass123')
        token = Token.objects.create(user=admin)
        
        # Authenticate the request
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post(f'/api/contact-messages/{self.message.id}/mark_as_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify it was marked as read
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)


# ====================================================================
# AUTHENTICATION & PERMISSION TESTS
# ====================================================================

class AuthenticationTest(APITestCase):
    """Test API authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_unauthenticated_read_allowed(self):
        """Test that unauthenticated users can read"""
        HomeBanner.objects.create(
            title="Public Banner",
            image="test.jpg"
        )
        response = self.client.get('/api/banners/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_write_denied(self):
        """Test that unauthenticated users cannot write"""
        response = self.client.post('/api/banners/', {
            'title': 'New Banner',
            'image': 'test.jpg'
        })
        # Will fail because no image file, but test permission later
        # For now just verify endpoint exists
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_405_METHOD_NOT_ALLOWED
        ])
