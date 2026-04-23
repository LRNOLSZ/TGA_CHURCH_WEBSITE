"""
Management command to populate the database with realistic dummy data.
Usage: python manage.py seed_data
       python manage.py seed_data --clear  (clears existing data first)
"""

import os
import io
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont


def make_image(width, height, color, label=""):
    """Generate a simple placeholder image as bytes."""
    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)
    if label:
        # Draw label text in white near centre
        draw.text((10, height // 2 - 10), label, fill="white")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return buf.read()


# Colour palette for placeholder images
COLORS = [
    "#3B5998", "#E1306C", "#1DA1F2", "#FF6B35",
    "#4CAF50", "#9C27B0", "#FF9800", "#00BCD4",
]


class Command(BaseCommand):
    help = "Seed the database with realistic dummy data for frontend testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing seeded data before inserting.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.clear_data()

        self.stdout.write(self.style.MIGRATE_HEADING("Starting database seed..."))

        self.seed_branches()
        self.seed_church_info()
        self.seed_head_pastor()
        self.seed_home_banners()
        self.seed_service_times()
        self.seed_leaders()
        self.seed_photo_gallery()
        self.seed_sermons()
        self.seed_events()
        self.seed_giving()
        self.seed_contact_messages()
        self.seed_testimonies()
        self.seed_books()
        self.seed_merchandise()

        self.stdout.write(self.style.SUCCESS("\n[OK] Database seeded successfully!"))

    # ------------------------------------------------------------------
    # CLEAR
    # ------------------------------------------------------------------
    def clear_data(self):
        from api.models import (
            HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
            Leader, PhotoGallery, Sermon, Event, Branch,
            GivingInfo, GivingImage, ContactMessage, Testimony,
            Book, Merchandise,
        )
        self.stdout.write("Clearing existing data...")
        for Model in [
            Testimony, ContactMessage, GivingImage, GivingInfo,
            ServiceTime, Event, Branch, PhotoGallery, Leader,
            Sermon, HomeBanner, HeadPastor, ChurchInfo,
            Book, Merchandise,
        ]:
            count, _ = Model.objects.all().delete()
            self.stdout.write(f"  Deleted {count} {Model.__name__} records")

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def _img_file(self, width, height, color_index, label=""):
        color = COLORS[color_index % len(COLORS)]
        data = make_image(width, height, color, label)
        return ContentFile(data, name=f"placeholder_{color_index}.jpg")

    def ok(self, name, count=None):
        msg = f"  [+] {name}"
        if count is not None:
            msg += f" ({count} records)"
        self.stdout.write(self.style.SUCCESS(msg))

    # ------------------------------------------------------------------
    # BRANCHES  (must be first — FK used by Event & ServiceTime)
    # ------------------------------------------------------------------
    def seed_branches(self):
        from api.models import Branch
        if Branch.objects.exists():
            self.stdout.write(f"  – Branches already exist, skipping.")
            return

        branches = [
            dict(
                name="TGA Accra Central",
                location="14 Liberation Road, Accra, Ghana",
                phone="+233 20 123 4567",
                email="accra@tgachurch.org",
                pastor_in_charge="Pastor Emmanuel Boateng",
                service_time="Sundays: 7AM & 9AM & 11AM\nWednesdays: 6PM",
                is_main_branch=True,
            ),
            dict(
                name="TGA Kumasi Branch",
                location="25 Adum Street, Kumasi, Ghana",
                phone="+233 24 765 4321",
                email="kumasi@tgachurch.org",
                pastor_in_charge="Pastor Abena Mensah",
                service_time="Sundays: 8AM & 10AM\nThursdays: 6PM",
                is_main_branch=False,
            ),
            dict(
                name="TGA Takoradi Branch",
                location="3 Harbour Road, Takoradi, Ghana",
                phone="+233 27 555 8888",
                email="takoradi@tgachurch.org",
                pastor_in_charge="Pastor Kwame Asante",
                service_time="Sundays: 9AM & 11AM\nFridays: 6PM",
                is_main_branch=False,
            ),
        ]

        created = []
        for i, data in enumerate(branches):
            b = Branch(**data)
            b.image.save(
                f"branch_{i}.jpg",
                self._img_file(800, 500, i, data["name"]),
                save=False,
            )
            b.save()
            created.append(b)

        self.ok("Branches", len(created))
        self._branches = created

    # ------------------------------------------------------------------
    # CHURCH INFO  (singleton)
    # ------------------------------------------------------------------
    def seed_church_info(self):
        from api.models import ChurchInfo
        if ChurchInfo.objects.exists():
            self.stdout.write("  – ChurchInfo already exists, skipping.")
            return

        ChurchInfo.objects.create(
            church_name="The Grace Assembly (TGA)",
            tagline="Building Faith, Transforming Lives",
            welcome_message=(
                "Welcome to The Grace Assembly — a place where every soul is celebrated "
                "and every life is transformed by the love of God. We are a Spirit-filled "
                "community committed to worship, discipleship, and impacting our world."
            ),
            full_about=(
                "Founded in 1998 by Bishop Daniel Owusu-Afriyie, The Grace Assembly began "
                "as a small prayer group of twelve believers in a single room in Accra. "
                "Over the decades God's grace has multiplied that seed into a thriving "
                "congregation with branches across Ghana. Our story is one of faith, "
                "perseverance and the miraculous hand of God. Today TGA stands as a beacon "
                "of hope, running schools, feeding programmes, medical outreaches and "
                "evangelism crusades that have touched hundreds of thousands of lives."
            ),
            address="14 Liberation Road, Accra, Ghana",
            phone="+233 20 123 4567",
            email="info@tgachurch.org",
            mission_statement=(
                "To preach the Gospel of Jesus Christ, make disciples of all nations, "
                "and demonstrate the Kingdom of God through signs, wonders and service."
            ),
            vision_statement=(
                "A church without walls — raising a generation of Spirit-filled believers "
                "who transform every sphere of society for God's glory."
            ),
            core_values=(
                "1. Grace & Truth\n"
                "2. Spirit-led Worship\n"
                "3. Discipleship & Growth\n"
                "4. Community & Fellowship\n"
                "5. Integrity & Excellence"
            ),
            service_times_text=(
                "Sunday First Service: 7:00 AM\n"
                "Sunday Second Service: 9:00 AM\n"
                "Sunday Third Service: 11:00 AM\n"
                "Midweek Service: Wednesday 6:00 PM\n"
                "Prayer & Fasting: Friday 5:00 AM"
            ),
            youtube_channel_url="https://www.youtube.com/@tgachurch",
            facebook_url="https://www.facebook.com/tgachurch",
            instagram_url="https://www.instagram.com/tgachurch",
            twitter_url="https://www.twitter.com/tgachurch",
            tiktok_url="https://www.tiktok.com/@tgachurch",
            whatsapp_url="https://chat.whatsapp.com/tgachurch",
        )
        self.ok("ChurchInfo", 1)

    # ------------------------------------------------------------------
    # HEAD PASTOR  (singleton)
    # ------------------------------------------------------------------
    def seed_head_pastor(self):
        from api.models import HeadPastor
        if HeadPastor.objects.exists():
            self.stdout.write("  – HeadPastor already exists, skipping.")
            return

        p = HeadPastor(
            name="Bishop Daniel Owusu-Afriyie",
            title="Senior Pastor & Founder",
            full_bio=(
                "Bishop Daniel Owusu-Afriyie is the founder and Senior Pastor of "
                "The Grace Assembly. Born in Kumasi, Ghana, he encountered the Lord "
                "at the age of nineteen and responded immediately to the call to ministry. "
                "He holds a Bachelor of Theology from the University of Ghana and a "
                "Master of Divinity from Regent University, Virginia. "
                "With over 25 years of pastoral experience, Bishop Daniel is renowned "
                "for his anointed teaching, his heart for the poor, and his passion "
                "for raising the next generation of leaders. He and his wife, "
                "Prophetess Grace Owusu-Afriyie, have four children."
            ),
            email="bishop@tgachurch.org",
            phone="+233 20 999 0000",
            whatsapp_url="https://whatsapp.com/channel/tgabp",
            instagram="https://instagram.com/bishopdanielofowafrica",
            tiktok="https://tiktok.com/@bishopdaniel",
        )
        p.image.save("head_pastor.jpg", self._img_file(600, 600, 0, "Bishop Daniel"), save=False)
        p.save()
        self.ok("HeadPastor", 1)

    # ------------------------------------------------------------------
    # HOME BANNERS
    # ------------------------------------------------------------------
    def seed_home_banners(self):
        from api.models import HomeBanner
        if HomeBanner.objects.exists():
            self.stdout.write("  – HomeBanners already exist, skipping.")
            return

        banners = [
            dict(
                title="Welcome to The Grace Assembly",
                subtitle="A place where faith meets destiny. Join us every Sunday.",
                button_text="Plan Your Visit",
                button_link="https://tgachurch.org/visit",
                is_active=True,
                order=1,
            ),
            dict(
                title="Arise & Shine Conference 2025",
                subtitle="Three days of worship, prayer and the Word. Register now!",
                button_text="Register Free",
                button_link="https://tgachurch.org/events/arise-shine",
                is_active=True,
                order=2,
            ),
            dict(
                title="New Here? We'd Love to Meet You",
                subtitle="Connect with our team and discover your place in the family.",
                button_text="Connect With Us",
                button_link="https://tgachurch.org/connect",
                is_active=True,
                order=3,
            ),
        ]

        for i, data in enumerate(banners):
            b = HomeBanner(**data)
            b.image.save(
                f"banner_{i}.jpg",
                self._img_file(1920, 600, i, data["title"][:30]),
                save=False,
            )
            b.save()

        self.ok("HomeBanners", len(banners))

    # ------------------------------------------------------------------
    # SERVICE TIMES
    # ------------------------------------------------------------------
    def seed_service_times(self):
        from api.models import ServiceTime, Branch
        if ServiceTime.objects.exists():
            self.stdout.write("  – ServiceTimes already exist, skipping.")
            return

        main = Branch.objects.filter(is_main_branch=True).first()

        services = [
            dict(day="Sunday", time="7:00 AM", service_type="First Sunday Service", branch=main),
            dict(day="Sunday", time="9:00 AM", service_type="Second Sunday Service", branch=main),
            dict(day="Sunday", time="11:00 AM", service_type="Third Sunday Service", branch=main, additional_info="With Holy Communion on first Sunday"),
            dict(day="Wednesday", time="6:00 PM", service_type="Midweek Bible Study", branch=main),
            dict(day="Friday", time="5:00 AM", service_type="Prayer & Fasting", branch=None, additional_info="All branches"),
        ]

        for s in services:
            ServiceTime.objects.create(**s)

        self.ok("ServiceTimes", len(services))

    # ------------------------------------------------------------------
    # LEADERS
    # ------------------------------------------------------------------
    def seed_leaders(self):
        from api.models import Leader
        if Leader.objects.exists():
            self.stdout.write("  – Leaders already exist, skipping.")
            return

        leaders = [
            dict(
                full_name="Pastor Grace Owusu-Afriyie",
                position="Ministry Leader",
                biography=(
                    "Prophetess Grace is the co-founder of TGA and leads the Women of Grace "
                    "ministry. She is a gifted prophetess and counsellor with a heart for "
                    "family restoration and women empowerment. She holds a degree in Psychology "
                    "from the University of Ghana."
                ),
                email="grace@tgachurch.org",
                phone="+233 24 111 2222",
                is_featured_on_home=True,
                order=1,
            ),
            dict(
                full_name="Elder Samuel Asante",
                position="Shepherd",
                biography=(
                    "Elder Samuel oversees the pastoral care department and coordinates "
                    "all home cell groups across Accra. With 15 years of service to TGA, "
                    "he is a pillar of the congregation known for his gentle spirit and wisdom."
                ),
                email="samuel@tgachurch.org",
                phone="+233 27 333 4444",
                is_featured_on_home=True,
                order=2,
            ),
            dict(
                full_name="Minister Joanna Boateng",
                position="Worship Leader",
                biography=(
                    "Minister Joanna leads the TGA Praise & Worship team. A classically "
                    "trained musician and songwriter, she has released two gospel albums "
                    "and leads the congregation into transformative encounters with God "
                    "each week."
                ),
                email="joanna@tgachurch.org",
                phone="+233 20 777 8888",
                is_featured_on_home=True,
                order=3,
            ),
        ]

        for i, data in enumerate(leaders):
            l = Leader(**data)
            l.profile_picture.save(
                f"leader_{i}.jpg",
                self._img_file(400, 400, i + 1, data["full_name"].split()[1]),
                save=False,
            )
            l.save()

        self.ok("Leaders", len(leaders))

    # ------------------------------------------------------------------
    # PHOTO GALLERY
    # ------------------------------------------------------------------
    def seed_photo_gallery(self):
        from api.models import PhotoGallery
        if PhotoGallery.objects.exists():
            self.stdout.write("  – PhotoGallery already exists, skipping.")
            return

        photos = [
            dict(title="Sunday Worship Service", category="Worship", caption="Congregation in worship during the second service"),
            dict(title="TGA Accra Main Auditorium", category="Church Building", caption="Our newly renovated main sanctuary"),
            dict(title="Arise & Shine Conference 2024", category="Events", caption="Over 2,000 attendees at last year's conference"),
            dict(title="Community Feeding Programme", category="Outreach", caption="Serving hot meals to over 500 families in Nima"),
        ]

        for i, data in enumerate(photos):
            p = PhotoGallery(**data)
            p.image.save(
                f"gallery_{i}.jpg",
                self._img_file(800, 600, i + 2, data["title"][:20]),
                save=False,
            )
            p.save()

        self.ok("PhotoGallery", len(photos))

    # ------------------------------------------------------------------
    # SERMONS
    # ------------------------------------------------------------------
    def seed_sermons(self):
        from api.models import Sermon
        if Sermon.objects.exists():
            self.stdout.write("  – Sermons already exist, skipping.")
            return

        sermons = [
            dict(
                title="The God Who Restores",
                description=(
                    "In this powerful message Bishop Daniel unpacks Joel 2:25 and reveals "
                    "God's promise to restore every lost year, every broken dream and every "
                    "stolen opportunity. No matter what you have been through, restoration is coming."
                ),
                speaker="Bishop Daniel Owusu-Afriyie",
                date=date.today() - timedelta(days=7),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                scripture_reference="Joel 2:25-27",
                series="Seasons of Restoration",
                duration="52 min",
                is_published=True,
                is_featured=True,
            ),
            dict(
                title="Walking in the Spirit",
                description=(
                    "Pastor Grace takes us through Galatians 5 and shows us practically "
                    "what it means to walk daily in step with the Holy Spirit — bearing fruit "
                    "and living in freedom."
                ),
                speaker="Pastor Grace Owusu-Afriyie",
                date=date.today() - timedelta(days=14),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                scripture_reference="Galatians 5:16-25",
                series="Life in the Spirit",
                duration="45 min",
                is_published=True,
                is_featured=True,
            ),
            dict(
                title="Faith That Moves Mountains",
                description=(
                    "Drawing from Matthew 17:20, Bishop Daniel challenges the congregation "
                    "to move beyond mustard-seed doubts into mountain-moving faith. Full of "
                    "testimonies and practical application."
                ),
                speaker="Bishop Daniel Owusu-Afriyie",
                date=date.today() - timedelta(days=21),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                scripture_reference="Matthew 17:20",
                series="Mountain-Moving Faith",
                duration="58 min",
                is_published=True,
                is_featured=True,
            ),
            dict(
                title="The Power of Prayer",
                description=(
                    "Elder Samuel leads a practical teaching on the discipline and power of "
                    "prayer. Drawing from the life of Daniel and the model prayer in Matthew 6, "
                    "this message will revolutionise your prayer life."
                ),
                speaker="Elder Samuel Asante",
                date=date.today() - timedelta(days=28),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                scripture_reference="Matthew 6:9-13",
                series="Foundations of Faith",
                duration="48 min",
                is_published=True,
                is_featured=True,
            ),
            dict(
                title="Living by Faith",
                description=(
                    "Bishop Daniel explores what it truly means to live by faith and not by "
                    "sight. Rooted in Hebrews 11, this message challenges believers to trust God "
                    "even when circumstances seem impossible."
                ),
                speaker="Bishop Daniel Owusu-Afriyie",
                date=date.today() - timedelta(days=35),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                scripture_reference="Hebrews 11:1-6",
                series="Foundations of Faith",
                duration="61 min",
                is_published=True,
                is_featured=True,
            ),
            dict(
                title="The Promise of the Holy Spirit",
                description=(
                    "Pastor Grace opens up the promise of Acts 1:8 and unpacks how the "
                    "baptism of the Holy Spirit empowers believers to be effective witnesses "
                    "and to live a supernatural life every single day."
                ),
                speaker="Pastor Grace Owusu-Afriyie",
                date=date.today() - timedelta(days=42),
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                scripture_reference="Acts 1:8",
                series="Life in the Spirit",
                duration="44 min",
                is_published=True,
                is_featured=True,
            ),
        ]

        for s in sermons:
            Sermon.objects.create(**s)

        self.ok("Sermons", len(sermons))

    # ------------------------------------------------------------------
    # EVENTS
    # ------------------------------------------------------------------
    def seed_events(self):
        from api.models import Event, Branch
        if Event.objects.exists():
            self.stdout.write("  – Events already exist, skipping.")
            return

        main = Branch.objects.filter(is_main_branch=True).first()
        kumasi = Branch.objects.filter(name__icontains="Kumasi").first()

        events_data = [
            dict(
                title="Arise & Shine Conference 2025",
                description=(
                    "Our flagship annual conference returns! Three days of intensive worship, "
                    "prophetic ministry and life-changing teaching from anointed speakers across Africa. "
                    "This is a must-attend event for every believer."
                ),
                date=timezone.now() + timedelta(days=30),
                location="TGA Accra Main Auditorium, Liberation Road",
                branch=main,
                category="Conference",
                contact_person="Elder Samuel Asante",
                is_active=True,
                is_featured=True,
            ),
            dict(
                title="Night of Worship — Glory Edition",
                description=(
                    "Join us for an extended evening of uninterrupted worship led by "
                    "Minister Joanna and the TGA Praise Team. Come expecting a fresh encounter "
                    "with the presence of God."
                ),
                date=timezone.now() + timedelta(days=14),
                location="TGA Accra Main Auditorium",
                branch=main,
                category="Worship Night",
                contact_person="Minister Joanna Boateng",
                is_active=True,
                is_featured=True,
            ),
            dict(
                title="Healing to the City — Kumasi",
                description=(
                    "Bishop Daniel brings the Healing to the City crusade to Kumasi. "
                    "Expect mass salvation, miraculous healings and deliverance. Open to all — "
                    "bring your unsaved friends and family!"
                ),
                date=timezone.now() + timedelta(days=60),
                location="Kumasi Sports Stadium, Kumasi",
                branch=kumasi,
                category="Healing to the city",
                contact_person="Pastor Abena Mensah",
                is_active=True,
                is_featured=True,
            ),
            dict(
                title="Youth Leadership Summit",
                description=(
                    "A transformative one-day summit designed for young leaders aged 16–30. "
                    "Featuring workshops on purpose, identity, entrepreneurship and spiritual growth. "
                    "Come equipped to lead your generation."
                ),
                date=timezone.now() + timedelta(days=21),
                location="TGA Accra Conference Hall",
                branch=main,
                category="General",
                contact_person="Minister Joanna Boateng",
                is_active=True,
                is_featured=True,
            ),
            dict(
                title="Women of Purpose Conference",
                description=(
                    "Pastor Grace hosts an empowering two-day conference for women of all ages. "
                    "Speakers from across Ghana will address topics of identity, family, "
                    "entrepreneurship and spiritual authority."
                ),
                date=timezone.now() + timedelta(days=45),
                location="TGA Accra Main Auditorium",
                branch=main,
                category="Conference",
                contact_person="Pastor Grace Owusu-Afriyie",
                is_active=True,
                is_featured=True,
            ),
            dict(
                title="Easter Sunday Celebration",
                description=(
                    "Celebrate the resurrection of our Lord Jesus Christ with the entire TGA "
                    "family. A morning of joyful worship, special ministration and the Word. "
                    "Bring a friend — all are welcome."
                ),
                date=timezone.now() + timedelta(days=90),
                location="TGA Accra Main Auditorium",
                branch=main,
                category="General",
                contact_person="Elder Samuel Asante",
                is_active=True,
                is_featured=True,
            ),
        ]

        for i, data in enumerate(events_data):
            e = Event(**data)
            e.image.save(
                f"event_{i}.jpg",
                self._img_file(800, 500, i + 3, data["title"][:25]),
                save=False,
            )
            e.save()

        self.ok("Events", len(events_data))

    # ------------------------------------------------------------------
    # GIVING
    # ------------------------------------------------------------------
    def seed_giving(self):
        from api.models import GivingInfo, GivingImage
        if GivingInfo.objects.exists():
            self.stdout.write("  – GivingInfo already exists, skipping.")
            return

        gi = GivingInfo.objects.create(
            flutterwave_link="https://flutterwave.com/pay/tgachurch",
            title="Give Online",
            instructions=(
                "You can give securely online using the button below. "
                "We accept all major cards, mobile money and bank transfers. "
                "All gifts support our local and international outreach programmes."
            ),
            why_give_message=(
                '"Each of you should give what you have decided in your heart to give, '
                'not reluctantly or under compulsion, for God loves a cheerful giver." '
                "— 2 Corinthians 9:7"
            ),
        )

        for i, caption in enumerate(["Mobile Money QR Code", "Bank Transfer Details"]):
            img = GivingImage(giving_info=gi, caption=caption, order=i)
            img.image.save(
                f"giving_{i}.jpg",
                self._img_file(400, 400, i + 4, caption[:20]),
                save=False,
            )
            img.save()

        self.ok("GivingInfo + GivingImages", 1)

    # ------------------------------------------------------------------
    # CONTACT MESSAGES
    # ------------------------------------------------------------------
    def seed_contact_messages(self):
        from api.models import ContactMessage
        if ContactMessage.objects.exists():
            self.stdout.write("  – ContactMessages already exist, skipping.")
            return

        messages = [
            dict(
                name="Kweku Mensah",
                email="kweku.mensah@gmail.com",
                phone="+233 24 987 6543",
                subject="General Inquiry",
                message="Good morning. I am new to Accra and looking for a Spirit-filled church to worship with. Could you tell me where I can find the Accra Central branch and what time the Sunday services start? Thank you.",
                is_read=False,
            ),
            dict(
                name="Ama Darkwah",
                email="ama.darkwah@yahoo.com",
                phone="+233 27 123 9876",
                subject="Prayer Request",
                message="Please I need the prayer team to stand with me. I have been waiting for a job for six months and I am trusting God for a breakthrough. My faith is strong but I need the support of the church family.",
                is_read=True,
            ),
            dict(
                name="Pastor John Acheampong",
                email="john.acheampong@gospellife.org",
                phone="+233 20 555 1212",
                subject="Partnership",
                message="Greetings in the name of Jesus. I pastor a small congregation in Tema and would love to explore a partnership with TGA for our upcoming outreach. Please let me know who I should speak to. God bless you.",
                is_read=False,
            ),
        ]

        for data in messages:
            ContactMessage.objects.create(**data)

        self.ok("ContactMessages", len(messages))

    # ------------------------------------------------------------------
    # TESTIMONIES
    # ------------------------------------------------------------------
    def seed_testimonies(self):
        from api.models import Testimony

        testimonies = [
            dict(
                name="Sister Abena Frimpong",
                testimony_text=(
                    "After three years of infertility, doctors had given up on me. "
                    "Bishop Daniel prayed over me at the Arise & Shine conference and "
                    "declared that God was opening my womb. Eight months later I gave "
                    "birth to a healthy baby boy. To God be all the glory!"
                ),
                location="Accra, Ghana",
                category="Healing",
                show_on_carousel=True,
                is_approved=True,
                order=1,
            ),
            dict(
                name="Brother Emmanuel Asiedu",
                testimony_text=(
                    "I lost my job and was on the verge of losing my home. I joined "
                    "the TGA prayer & fasting programme and God supernaturally opened a "
                    "door for me — a salary triple what I was earning before. "
                    "TGA is truly a house of miracles!"
                ),
                location="Kumasi, Ghana",
                category="Financial",
                show_on_carousel=True,
                is_approved=True,
                order=2,
            ),
            dict(
                name="Madam Felicia Owusu",
                testimony_text=(
                    "I came to TGA broken, addicted and without hope. Through the love "
                    "of this church family, counselling and the power of God's Word, "
                    "I am completely free today. It has been two years and I have never "
                    "looked back. Jesus saves!"
                ),
                location="Takoradi, Ghana",
                category="Salvation",
                show_on_carousel=True,
                is_approved=True,
                order=3,
            ),
            dict(
                name="Kofi Agyemang",
                testimony_text=(
                    "My marriage was on the brink of collapse. My wife and I had "
                    "separated for eight months and divorce papers were being prepared. "
                    "We both attended the TGA Marriage Restoration retreat and God "
                    "turned everything around in one weekend. We are now stronger than ever!"
                ),
                location="Accra, Ghana",
                category="Marriage",
                show_on_carousel=True,
                is_approved=True,
                order=4,
            ),
            dict(
                name="Akosua Mensah",
                testimony_text=(
                    "I failed my university entrance exams twice and was told I would "
                    "never make it into a top school. The TGA youth group prayed and "
                    "fasted with me for three days. I not only passed — I received a "
                    "scholarship. Nothing is impossible with God!"
                ),
                location="Kumasi, Ghana",
                category="Academic",
                show_on_carousel=True,
                is_approved=True,
                order=5,
            ),
            dict(
                name="Pastor David Kumi",
                testimony_text=(
                    "Our small congregation of 30 people was struggling financially "
                    "and spiritually. After connecting with TGA and sitting under the "
                    "teaching of Bishop Daniel, God breathed new life into our church. "
                    "We now have over 400 members and our own building. To God be the glory!"
                ),
                location="Takoradi, Ghana",
                category="Church Growth",
                show_on_carousel=True,
                is_approved=True,
                order=6,
            ),
        ]

        created = 0
        for i, data in enumerate(testimonies):
            if Testimony.objects.filter(name=data["name"]).exists():
                continue
            t = Testimony(**data)
            t.image.save(
                f"testimony_{i}.jpg",
                self._img_file(300, 300, i + 5, data["name"].split()[1]),
                save=False,
            )
            t.save()
            created += 1

        self.ok("Testimonies", created)

    # ------------------------------------------------------------------
    # BOOKS
    # ------------------------------------------------------------------
    def seed_books(self):
        from api.models import Book
        if Book.objects.exists():
            self.stdout.write("  – Books already exist, skipping.")
            return

        books = [
            dict(
                name="Grace Upon Grace",
                price=Decimal("19.99"),
                description=(
                    "Bishop Daniel's debut book unpacks the extravagant grace of God "
                    "and how it transforms every area of life — identity, relationships, "
                    "purpose and destiny. A must-read for every believer."
                ),
                whatsapp_link="https://wa.me/233209990000?text=I%20want%20to%20order%20Grace%20Upon%20Grace",
                email="books@tgachurch.org",
                amazon="https://amazon.com/dp/example1",
                is_available=True,
            ),
            dict(
                name="The Spirit-Filled Life",
                price=Decimal("15.00"),
                description=(
                    "A practical guide to living every day in the power and gifts of "
                    "the Holy Spirit. Includes study questions and personal activation exercises."
                ),
                whatsapp_link="https://wa.me/233209990000?text=I%20want%20to%20order%20Spirit-Filled%20Life",
                email="books@tgachurch.org",
                amazon="https://amazon.com/dp/example2",
                is_available=True,
            ),
            dict(
                name="Mountain-Moving Faith",
                price=Decimal("12.99"),
                description=(
                    "Based on his popular sermon series, Bishop Daniel shows you how to "
                    "develop a faith that refuses to be moved by circumstances and sees "
                    "the impossible become possible."
                ),
                whatsapp_link="https://wa.me/233209990000?text=I%20want%20to%20order%20Mountain%20Moving%20Faith",
                email="books@tgachurch.org",
                amazon="https://amazon.com/dp/example3",
                is_available=True,
            ),
        ]

        for i, data in enumerate(books):
            b = Book(**data)
            b.image.save(
                f"book_{i}.jpg",
                self._img_file(400, 550, i, data["name"][:15]),
                save=False,
            )
            b.save()

        self.ok("Books", len(books))

    # ------------------------------------------------------------------
    # MERCHANDISE
    # ------------------------------------------------------------------
    def seed_merchandise(self):
        from api.models import Merchandise
        if Merchandise.objects.exists():
            self.stdout.write("  – Merchandise already exists, skipping.")
            return

        items = [
            dict(
                name="TGA Church Hoodie",
                price=Decimal("35.00"),
                description=(
                    "Premium quality hoodie with embroidered TGA logo. "
                    "Available in Black, Navy Blue and White. Sizes: S, M, L, XL, XXL."
                ),
                whatsapp_link="https://wa.me/233209990000?text=I%20want%20to%20order%20a%20TGA%20Hoodie",
                email="store@tgachurch.org",
                is_available=True,
            ),
            dict(
                name="TGA Praise T-Shirt",
                price=Decimal("20.00"),
                description=(
                    "Comfortable cotton t-shirt with bold TGA praise print on the front. "
                    "Perfect for casual wear and outreach events. Sizes: S, M, L, XL."
                ),
                whatsapp_link="https://wa.me/233209990000?text=I%20want%20to%20order%20a%20TGA%20T-Shirt",
                jiji_link="https://jiji.com.gh/tgachurch/tshirt",
                email="store@tgachurch.org",
                is_available=True,
            ),
            dict(
                name="TGA Wristband (Pack of 5)",
                price=Decimal("5.00"),
                description=(
                    "Silicone wristbands with 'TGA — Building Faith' inscription. "
                    "Great for personal use or gifting. Available in mixed colours."
                ),
                whatsapp_link="https://wa.me/233209990000?text=I%20want%20to%20order%20TGA%20Wristbands",
                email="store@tgachurch.org",
                is_available=True,
            ),
        ]

        for i, data in enumerate(items):
            m = Merchandise(**data)
            m.image.save(
                f"merch_{i}.jpg",
                self._img_file(500, 500, i + 2, data["name"][:15]),
                save=False,
            )
            m.save()

        self.ok("Merchandise", len(items))
