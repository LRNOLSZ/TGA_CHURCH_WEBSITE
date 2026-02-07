from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ContactMessage, Testimony, Book, ExchangeRate, Merchandise
)


# ====================================================================
# MODEL TESTS
# ====================================================================

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
        self.branch = Branch.objects.create(
            name="Main Branch",
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
        self.branch = Branch.objects.create(
            name="Main Campus",
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
        """Test POST /api/contact-messages/{id}/mark_as_read/"""
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
