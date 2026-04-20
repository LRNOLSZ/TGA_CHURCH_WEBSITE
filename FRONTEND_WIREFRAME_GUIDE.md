# Frontend Wireframe Guide - TGA Church Website

## Overview
This guide details what content/components should appear on each page based on your Django models and API endpoints.

---

## 1. HOMEPAGE

### Hero Section (Top)
- **Rotating Banners Carousel** (HomeBanner model)
  - Display 3-5 active banners rotating automatically
  - Each banner has: image (1920x600px), title, subtitle, button with link
  - Auto-rotate every 5 seconds with navigation dots
  - Call-to-action button (e.g., "Join Us", "Give Now")

### Featured Events Section
- **Title:** "Upcoming Events"
- **Display:** 3-4 featured events in a grid/carousel
- **Per Event Card:**
  - Event image
  - Event title
  - Date & time
  - Location
  - "Learn More" button → links to event detail page
- **Data from:** Event model (filter: is_featured=True, date >= today)

### Featured Sermons Section
- **Title:** "Latest Messages"
- **Display:** 3 featured sermons in a row
- **Per Sermon Card:**
  - Video thumbnail (auto-generated from YouTube/Vimeo URL)
  - Sermon title
  - Speaker name
  - Date
  - "Watch Now" button → links to sermon detail page
- **Data from:** Sermon model (filter: is_featured=True, is_published=True)

### Head Pastor Section
- **Title:** "Meet Our Head Pastor"
- **Content:**
  - Large professional photo (HeadPastor model)
  - Name & title (e.g., "Senior Pastor & Founder")
  - Bio summary (first 200 chars of full_bio)
  - "Read Full Bio" button
  - Social links: WhatsApp, Instagram, TikTok (if available)
- **Data from:** HeadPastor model (only 1 record)

### Church Info Summary
- **Title:** "Welcome to [Church Name]"
- **Content:**
  - Church name & tagline (from ChurchInfo model)
  - Welcome message (first 300 chars)
  - 3-4 key service times
  - "View All Services" button → links to Branches page
- **Data from:** ChurchInfo model + ServiceTime model

### Call-to-Action Section
- 2-3 buttons in a row:
  - "Upcoming Events" → /events
  - "Give Online" → /giving
  - "Contact Us" → /contact

### Footer
- **Left Column:** Church info (address, phone, email)
- **Middle Columns:** Quick links (Events, Sermons, About, Contact, Giving)
- **Right Column:** Social media links (YouTube, Facebook, Instagram, Twitter, TikTok, WhatsApp)
- **Bottom:** Copyright notice & links (Privacy, Terms)

---

## 2. EVENTS PAGE

### Header
- **Title:** "Church Events"
- **Subtitle:** "Stay updated with our upcoming activities"

### Filter/Search Section
- **Search bar** - Search by event title
- **Category dropdown** - Filter by:
  - General Church Event
  - Conference/Convention
  - Outreach/Evangelism
  - Worship Night
  - Healing to the city
  - Other
- **Branch filter** - Show events for specific branch (if multiple branches)
- **Date range filter** - Optional (upcoming, past, all)

### Events Listing
- **Grid layout** (2-3 columns on desktop, 1 on mobile)
- **Per Event Card:**
  - Event image
  - Date badge (top-left)
  - Category badge (top-right)
  - Event title
  - Location with icon
  - Short description (first 150 chars)
  - "View Details" button
- **Pagination:** 10 events per page

### No Results State
- Show message if no events found
- Suggest clearing filters

### Data from:
- Event model (filter: is_active=True, ordered by date ASC)

---

## 3. EVENT DETAIL PAGE

### Header
- Large event image (banner at top)
- Event title

### Content Section
- **Event Details:**
  - Date & time (formatted clearly)
  - Location with Google Maps icon
  - Category badge
  - Full description (rich text)
  - Speaker/contact person name (if available)

- **Action Buttons:**
  - "Register" button → external link (if registration_link exists)
  - "Share on Social" button (optional)

### Related Events (Bottom)
- Show 3 similar events from same category
- Links to those event detail pages

### Data from:
- Event model (single record)

---

## 4. SERMONS PAGE

### Header
- **Title:** "Messages & Sermons"
- **Subtitle:** "Watch our latest sermons"

### Search/Filter Section
- **Search bar** - Search by sermon title or speaker name
- **Speaker filter dropdown** - Filter by speaker
- **Series filter dropdown** - Filter by sermon series (if part of series)

### Featured Sermons Section
- **Display:** Top 1-3 sermons with larger cards
- **Per Card:**
  - Large video thumbnail
  - Title
  - Speaker name
  - Date
  - "Watch Now" button

### Sermons Listing
- **Grid layout** (3 columns on desktop, 1 on mobile)
- **Per Sermon Card:**
  - Video thumbnail
  - Title
  - Speaker name & date
  - Scripture reference (if available)
  - Series name (if part of series)
  - "Watch" button
- **Pagination:** 12 sermons per page

### Data from:
- Sermon model (filter: is_published=True, ordered by date DESC)

---

## 5. SERMON DETAIL PAGE

### Video Player (Top)
- Embedded video player (YouTube/Vimeo auto-embeds)
- Video plays in responsive container

### Sermon Information
- **Sermon title**
- **Speaker:** [Speaker name]
- **Date:** [Formatted date]
- **Duration:** [Video length]
- **Scripture Reference:** [Bible passage] (if available)
- **Series:** [Series name] (if part of series)

### Full Description
- Complete sermon description/notes

### Related Sermons (Bottom)
- Show 3-5 other sermons by same speaker or in same series
- Grid of sermon cards with video thumbnails

### Data from:
- Sermon model (single record)

---

## 6. BRANCHES/LOCATIONS PAGE

### Header
- **Title:** "Our Branches"
- **Subtitle:** "Find a location near you"

### Branches Listing
- **Highlight Main Branch** first with special styling
- **Per Branch Card:**
  - Branch image (if available)
  - Branch name
  - Location/address
  - Phone & email
  - Pastor in charge
  - Service times
  - "Get Directions" button → Google Maps link
  - "Contact" button → direct link to contact form pre-filled with branch

### Branch Details (Alternative Layout)
- If clicking "Learn More":
  - Full address details
  - Google Maps embedded (if link available)
  - Detailed service times
  - Pastor bio/contact
  - Events at this branch (filtered from Event model)

### Data from:
- Branch model (ordered: main branch first, then alphabetical)
- ServiceTime model (filtered by branch)
- Event model (filtered by branch)

---

## 7. LEADERS/STAFF PAGE (Optional Phase 1)

### Header
- **Title:** "Our Leadership Team"

### Featured Leaders (Top)
- Head pastor section (if not shown on homepage)
- Featured leaders (from Leader model where is_featured_on_home=True)

### All Leaders
- **Grid layout** (3-4 columns on desktop, 1-2 on mobile)
- **Per Leader Card:**
  - Professional photo
  - Full name
  - Position/title
  - Short bio summary
  - Contact: email, phone (if available)
  - Social links: Instagram, TikTok (if available)

### Data from:
- HeadPastor model (1 record)
- Leader model (ordered by order field, then by position)

---

## 8. CHURCH INFO PAGE (Optional Phase 1)

### Header
- Church name & tagline

### About Section
- Full about text (ChurchInfo.full_about)
- Church building/gallery photo

### Mission & Vision
- **Mission:** [ChurchInfo.mission_statement]
- **Vision:** [ChurchInfo.vision_statement]
- **Core Values:** [ChurchInfo.core_values] (displayed as list or cards)

### Photo Gallery
- Display church photos (PhotoGallery model)
- Organized by category:
  - Church Building
  - Worship Service
  - Special Events
  - Outreach & Missions
  - Other

### Service Times
- All service times from ServiceTime model
- Organized by day of week
- Show service type, time, and branch (if specific)

### Social Media Links Section
- Grid of social media links (YouTube, Facebook, Instagram, Twitter, TikTok, WhatsApp)
- Each with icon and link

### Data from:
- ChurchInfo model (1 record)
- PhotoGallery model (ordered by date)
- ServiceTime model (ordered by day)

---

## 9. GIVING/DONATIONS PAGE

### Header
- **Title:** "Give Online"
- Church info tagline or giving message

### Giving Information Section
- **Why Give Section:**
  - GivingInfo.why_give_message (biblical message about giving)
  - Nice icon/illustration

### Giving Methods Display
- **Display GivingImage model images:**
  - QR codes
  - Bank details
  - Mobile money instructions
  - Each image with caption
  - Organized by order field
  - Can be arranged in grid or carousel

### Main Call-to-Action
- **"Give Now" button** → links to GivingInfo.flutterwave_link
- Size: prominent, contrasting color

### Instructions Section
- GivingInfo.instructions (if provided)
- Step-by-step guide for different payment methods

### Footer Note
- Message about where funds go (optional)

### Data from:
- GivingInfo model (1 record)
- GivingImage model (related to GivingInfo, ordered by order field)

---

## 10. MERCHANDISE/STORE PAGE

### Header
- **Title:** "Church Store"
- **Subtitle:** "Support the ministry"

### Products Grid
- **2-3 columns on desktop, 1 on mobile**
- **Per Product Card (Books & Merchandise):**
  - Product image
  - Product name
  - Price (USD) - consider showing exchange rate for other currencies
  - Short description (if available)
  - "View Details" button

### Filter/Sort Options
- **Filter by type:**
  - Books
  - Merchandise
  - All
- **Sort by:**
  - Newest
  - Price: Low to High
  - Price: High to Low

### Product Detail (Modal/Page)
- Large product image
- Product name
- Price
- Full description
- **Purchase Options (as separate buttons/links):**
  - "Buy on WhatsApp" → whatsapp_link
  - "Email to Order" → mailto: email
  - "Buy on Amazon" → amazon_link
  - "Buy on Jiji" → jiji_link (for merchandise)
  - Based on what's available for each product

### Exchange Rate Display (Optional)
- Show price in multiple currencies
- Use ExchangeRate model for conversions
- Example: "$19.99 USD / GHS 245 / CUP 499"

### Data from:
- Book model (filter: is_available=True)
- Merchandise model (filter: is_available=True)
- ExchangeRate model (for currency conversion)

---

## 11. CONTACT US PAGE

### Header
- **Title:** "Get In Touch"
- **Subtitle:** "We'd love to hear from you"

### Contact Information Section
- **Church details:**
  - Address (ChurchInfo.address)
  - Phone (ChurchInfo.phone)
  - Email (ChurchInfo.email)
  - Icons for each

### Contact Form
- **Fields from ContactMessage model:**
  - Name (required)
  - Email (required)
  - Phone (optional)
  - Subject dropdown:
    - General Inquiry
    - Prayer Request
    - Event Information
    - Service Information
    - Counseling Request
    - Partnership/Collaboration
    - Feedback/Testimony
    - Volunteer Opportunity
    - Media/Press Request
    - Other
  - Message (large textarea, required)
  - Submit button
  - Confirmation message after submit

### Quick Links Section

- Links to:
  - Service times (→ Branches page)
  - Upcoming events (→ Events page)
  - Give online (→ Giving page)
  - View leadership (→ Leaders page)

### Map Section (Optional)
- Embedded Google Map showing church location
- If google_maps_url available in ChurchInfo

### Data from:
- ChurchInfo model (contact info)
- ContactMessage model (form submission endpoint)

---



## 13. 404/ERROR PAGE

### Layout
- Friendly message: "Page not found"
- Icon or illustration
- "Go Home" button
- "View Events" button
- "Contact Us" button

---

## RESPONSIVE DESIGN NOTES

### Breakpoints:
- **Mobile:** < 640px (1 column, full-width components)
- **Tablet:** 640px - 1024px (2 columns, flexible)
- **Desktop:** > 1024px (3+ columns, full layout)

### Key Responsive Elements:
- Hero banner scales responsively
- Event/sermon cards stack vertically on mobile
- Navigation menu becomes hamburger on mobile
- Footer becomes single column on mobile

---

## COLOR & BRANDING

**Define in Figma:**
- Primary color (church brand color)
- Secondary color (accents)
- Neutral colors (grays for text/backgrounds)
- Success/error colors (green for success, red for errors)

**Use consistently** across all pages.

---

## COMPONENT LIST FOR DEVELOPMENT

### Reusable Components:
1. **Navbar** - Header with logo & navigation
2. **Footer** - Global footer
3. **CardComponent** - Event/sermon/product card
4. **ButtonComponent** - Primary/secondary buttons
5. **FilterComponent** - Search/filter controls
6. **PaginationComponent** - Page numbers
7. **BannerCarousel** - Rotating banner
8. **VideoPlayer** - Embedded video
9. **ContactForm** - Reusable form
10. **ImageGallery** - Photo grid display
11. **SocialLinks** - Social media icons

---

## PRIORITY BUILD ORDER

### Phase 1 (MVP - Week 1):
1. Homepage
2. Events Page + Detail
3. Sermons Page + Detail
4. Contact Page
5. Giving Page
6. Footer & Navigation

### Phase 2 (Week 2):
7. Branches Page
8. Merchandise/Store Page
9. Church Info Page
10. Leaders Page

### Phase 3 (Future):
11. Testimonies Carousel (on homepage)
12. Gallery Page
13. User Authentication
14. Advanced features

---

## API ENDPOINTS TO USE

```
GET /api/banners/?is_active=true
GET /api/events/?is_featured=true&date__gte=today
GET /api/sermons/?is_featured=true
GET /api/branches/
GET /api/leaders/?is_featured_on_home=true
GET /api/church-info/
GET /api/sermons/
GET /api/events/
POST /api/contact-messages/
GET /api/giving-info/
GET /api/books/?is_available=true
GET /api/merchandise/?is_available=true
GET /api/exchange-rates/
```

---

**Next Step:** Design these wireframes in Figma, then I'll build the Next.js project with these components ready to go! 🎨
