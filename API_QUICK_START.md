# API Quick Start Guide

## **1. Start the Server**
```bash
python manage.py runserver
```

---

## **2. Test in Browser (Easiest!)**

Visit: `http://127.0.0.1:8000/api/`

You'll see a beautiful browsable API with:
- List of all endpoints
- Forms to create/edit/delete
- Live documentation

---

## **3. Test via Command Line**

### **Get All Events**
```bash
curl http://127.0.0.1:8000/api/events/
```

### **Search Events**
```bash
curl http://127.0.0.1:8000/api/events/?search=sunday
```

### **Get Banners (Active Only)**
```bash
curl http://127.0.0.1:8000/api/banners/?is_active=true
```

### **Get Upcoming Events**
```bash
curl http://127.0.0.1:8000/api/events/upcoming/
```

### **Get Featured Sermons**
```bash
curl http://127.0.0.1:8000/api/sermons/featured/
```

---

## **4. Authentication (For Admin Operations)**

### **Get Your Admin Token**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get(username='admin')
token, created = Token.objects.get_or_create(user=user)
print(f"Your token: {token.key}")
```

### **Create New Event (As Admin)**
```bash
TOKEN="your-token-here"

curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Youth Retreat",
    "description": "Exciting youth program",
    "date": "2026-03-15T14:00:00Z",
    "location": "Conference Center",
    "category": "General",
    "image": null
  }'
```

### **Update Sermon (As Admin)**
```bash
TOKEN="your-token-here"

curl -X PUT http://127.0.0.1:8000/api/sermons/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title",
    "is_featured": true
  }'
```

---

## **5. All Available Endpoints**

### **Home Page**
- `GET /api/banners/` - All banners
- `GET /api/church-info/` - Church details
- `GET /api/head-pastor/` - Pastor info

### **About Page**
- `GET /api/leaders/` - Leadership team
- `GET /api/gallery/` - Photo gallery

### **Sermons**
- `GET /api/sermons/` - All sermons
- `GET /api/sermons/featured/` - Featured only
- `GET /api/sermons/latest/` - Latest sermon

### **Events**
- `GET /api/events/` - All events
- `GET /api/events/upcoming/` - Future events only
- `GET /api/events/featured/` - Featured events

### **Branches**
- `GET /api/branches/` - All branches
- `GET /api/service-times/` - Service times

### **Giving**
- `GET /api/giving-info/` - Giving page info
- `GET /api/giving-images/` - Donation images

### **Shop**
- `GET /api/books/` - Available books
- `GET /api/merchandise/` - Merchandise
- `GET /api/exchange-rates/` - Currency rates

### **Contact**
- `GET /api/contact-messages/` - Messages (admin only)
- `GET /api/contact-messages/unread/` - Unread (admin only)
- `POST /api/contact-messages/` - Submit form (public!)
- `GET /api/testimonies/` - All testimonies
- `GET /api/testimonies/carousel/` - Display testimonies

---

## **6. Query Parameters**

### **Pagination**
```bash
curl http://127.0.0.1:8000/api/events/?page=2&page_size=20
```

### **Search**
```bash
curl http://127.0.0.1:8000/api/sermons/?search=faith
curl http://127.0.0.1:8000/api/leaders/?search=pastor
```

### **Filter**
```bash
curl http://127.0.0.1:8000/api/events/?category=Outreach
curl http://127.0.0.1:8000/api/events/?active=true
curl http://127.0.0.1:8000/api/banners/?is_active=true
```

### **Order**
```bash
curl http://127.0.0.1:8000/api/events/?ordering=-date
curl http://127.0.0.1:8000/api/sermons/?ordering=-created_at
```

---

## **7. Response Format**

### **Success (200 OK)**
```json
{
  "count": 15,
  "next": "http://127.0.0.1:8000/api/events/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Sunday Service",
      "date": "2026-02-08T09:00:00Z",
      "location": "Main Hall",
      ...
    }
  ]
}
```

### **Error (401 Unauthorized)**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### **Error (404 Not Found)**
```json
{
  "detail": "Not found."
}
```

---

## **8. Testing Checklist**

- [ ] Can view `/api/` in browser
- [ ] Can get events without auth
- [ ] Can get banners without auth
- [ ] Can submit contact form without auth
- [ ] Can POST event WITH token (shows success)
- [ ] Can POST event WITHOUT token (shows 401 error)
- [ ] Pagination works (add `?page=2`)
- [ ] Search works (add `?search=text`)
- [ ] Rate limiting works

---

## **9. JavaScript Example**

```javascript
// Get events (public)
async function getEvents() {
  const res = await fetch('http://127.0.0.1:8000/api/events/');
  const data = await res.json();
  console.log(data.results);
}

// Create event (authenticated)
async function createEvent(title, date, location, token) {
  const res = await fetch('http://127.0.0.1:8000/api/events/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title,
      date,
      location,
      category: 'General',
      description: 'New event'
    })
  });
  return res.json();
}

// Call it
getEvents();
// createEvent('Easter Service', '2026-04-12T10:00:00Z', 'Main Hall', 'TOKEN');
```

---

**Happy API testing! 🎉**
