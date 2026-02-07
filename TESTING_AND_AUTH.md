# Testing & Authentication Guide

## **Part 1: Running Tests**

### **Run All Tests**
```bash
python manage.py test
```

### **Run Specific Test**
```bash
python manage.py test api.tests.HomeBannerAPITest.test_get_banners_list
```

### **Run with Verbosity**
```bash
python manage.py test --verbosity=2
```

### **Expected Output**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
Ran 20 tests in 0.234s

OK
```

---

## **Part 2: Token Authentication Setup**

### **1. Create Migration for Tokens**
```bash
python manage.py migrate
```

This creates the `authtoken_token` table automatically.

### **2. Generate Token for a User**

#### **Option A: Via Django Shell**
```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create or get a user
user = User.objects.get(username='admin')

# Generate/Get token
token, created = Token.objects.get_or_create(user=user)
print(token.key)
# Output: 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

#### **Option B: Via Django Admin**
1. Go to `/admin/authtoken/token/`
2. Click "Add Token"
3. Select user
4. Click Save
5. Copy the token key

---

## **Part 3: Using the API with Authentication**

### **Public Endpoints (No Auth Needed)**
```bash
# Get all events
curl http://127.0.0.1:8000/api/events/

# Get all banners
curl http://127.0.0.1:8000/api/banners/

# Get sermons
curl http://127.0.0.1:8000/api/sermons/
```

### **Protected Endpoints (Auth Required)**

#### **Create Event (Admin Only)**
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Event",
    "description": "Event description",
    "date": "2026-02-15T09:00:00Z",
    "location": "Main Hall",
    "category": "General"
  }'
```

#### **Update Sermon**
```bash
curl -X PUT http://127.0.0.1:8000/api/sermons/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "speaker": "Pastor John"
  }'
```

#### **Delete Banner**
```bash
curl -X DELETE http://127.0.0.1:8000/api/banners/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### **Submit Contact Form (Public)**
```bash
curl -X POST http://127.0.0.1:8000/api/contact-messages/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Prayer Request",
    "message": "Please pray for me"
  }'
```

---

## **Part 4: Using in JavaScript/Frontend**

### **Getting Events (Public)**
```javascript
fetch('http://127.0.0.1:8000/api/events/')
  .then(res => res.json())
  .then(data => console.log(data))
```

### **Creating Event (Authenticated)**
```javascript
const token = 'your-token-here';

fetch('http://127.0.0.1:8000/api/events/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'New Event',
    description: 'Event details',
    date: '2026-02-15T09:00:00Z',
    location: 'Main Hall',
    category: 'General'
  })
})
.then(res => res.json())
.then(data => console.log('Event created:', data))
```

---

## **Part 5: Browsable API in Browser**

1. **Go to:** `http://127.0.0.1:8000/api/`
2. **Login** (top-right corner) with your admin credentials
3. **You'll see:**
   - List of all endpoints
   - Clickable links to each endpoint
   - Forms to create/update records
   - API documentation

### **Testing Read-Only vs Protected:**
- **GET requests:** Work without login ✅
- **POST/PUT/DELETE:** Require login (shows form only after login) 🔒

---

## **Part 6: Permissions Summary**

| Operation | Public | Authenticated Admin |
|-----------|--------|-------------------|
| GET /api/events/ | ✅ Yes | ✅ Yes |
| POST /api/events/ | ❌ No | ✅ Yes |
| PUT /api/events/{id}/ | ❌ No | ✅ Yes |
| DELETE /api/events/{id}/ | ❌ No | ✅ Yes |

---

## **Part 7: Rate Limiting**

By default:
- **Unauthenticated users:** 100 requests/hour
- **Authenticated users:** 1000 requests/hour

If you hit the limit:
```
HTTP 429 Too Many Requests
```

---

## **Testing Checklist**

- [ ] Run `python manage.py test` - All tests pass
- [ ] Create user in `/admin/`
- [ ] Generate token for user
- [ ] Test public endpoint (works without token)
- [ ] Test protected endpoint without token (fails with 401)
- [ ] Test protected endpoint with token (works)
- [ ] Visit `/api/` in browser, login, test POST form
- [ ] Test rate limiting by making many requests

---

## **Troubleshooting**

### **Error: "401 Unauthorized"**
- Missing or invalid token
- Token format should be: `Token abc123...`
- Not: `Bearer abc123...`

### **Error: "403 Forbidden"**
- User is authenticated but doesn't have permission
- Make sure user is admin/staff

### **Error: "400 Bad Request"**
- Missing required fields
- Invalid field data
- Check response body for details

### **Tests won't run**
```bash
# Make sure migrations are applied
python manage.py migrate

# Then run tests
python manage.py test
```
