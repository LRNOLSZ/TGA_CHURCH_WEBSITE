# API Documentation

Complete reference for the TGA Church Management System REST API.

## Table of Contents

1. [Base URL & Authentication](#base-url--authentication)
2. [Response Format](#response-format)
3. [Error Handling](#error-handling)
4. [Endpoints Overview](#endpoints-overview)
5. [Detailed Endpoints](#detailed-endpoints)

## Base URL & Authentication

**Base URL:** `http://localhost:8000/api/`

**Authentication:** Token-based (if implemented) or Session-based

### Example Request

```bash
curl -X GET http://localhost:8000/api/events/ \
  -H "Content-Type: application/json"
```

## Response Format

### Success Response (200 OK)

```json
{
  "count": 10,
  "next": "http://localhost:8000/api/events/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Sunday Service",
      "description": "Weekly service",
      "event_date": "2026-02-01",
      "event_time": "09:00:00",
      "location": "Main Church Hall",
      "created_at": "2026-01-31T10:00:00Z",
      "updated_at": "2026-01-31T10:00:00Z"
    }
  ]
}
```

### Error Response (400/404/500)

```json
{
  "error": "Error message describing what went wrong",
  "status": 400
}
```

## Error Handling

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 404 | Not Found |
| 500 | Server Error |

## Endpoints Overview

### Content Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/banners/` | List all banners |
| POST | `/banners/` | Create banner |
| GET | `/banners/{id}/` | Get banner details |
| PUT | `/banners/{id}/` | Update banner |
| DELETE | `/banners/{id}/` | Delete banner |

### Ministry

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events/` | List all events |
| POST | `/events/` | Create event |
| GET | `/events/{id}/` | Get event details |
| PUT | `/events/{id}/` | Update event |
| DELETE | `/events/{id}/` | Delete event |
| GET | `/sermons/` | List sermons |
| GET | `/sermons/{id}/` | Get sermon details |

### Administration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/branches/` | List branches |
| GET | `/branches/{id}/` | Get branch details |
| GET | `/givinginfo/` | List giving options |
| GET | `/contactmessage/` | List contact messages |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List users |
| GET | `/users/{id}/` | Get user details |

## Detailed Endpoints

### Events

#### List Events

```
GET /api/events/
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `search` - Search by title
- `ordering` - Order by field (e.g., `-created_at`, `event_date`)

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Sunday Worship",
      "description": "Main weekly service",
      "event_date": "2026-02-01",
      "event_time": "09:00:00",
      "location": "Main Hall",
      "image": "http://localhost:8000/media/events/worship.jpg",
      "created_at": "2026-01-31T10:00:00Z",
      "updated_at": "2026-01-31T10:00:00Z"
    }
  ]
}
```

#### Create Event

```
POST /api/events/
```

**Request Body:**
```json
{
  "title": "Special Conference",
  "description": "Leadership conference",
  "event_date": "2026-02-15",
  "event_time": "14:00:00",
  "location": "Convention Center",
  "image": "< file upload >"
}
```

**Validation Rules:**
- `title` - Required, max 200 characters
- `event_date` - Required, valid date format (YYYY-MM-DD)
- `event_time` - Required, valid time format (HH:MM:SS)
- `image` - Optional, max 10MB, only JPEG/PNG/GIF/WebP

**Response (201 Created):**
```json
{
  "id": 10,
  "title": "Special Conference",
  "description": "Leadership conference",
  "event_date": "2026-02-15",
  "event_time": "14:00:00",
  "location": "Convention Center",
  "image": "http://localhost:8000/media/events/conference.jpg",
  "created_at": "2026-01-31T11:00:00Z",
  "updated_at": "2026-01-31T11:00:00Z"
}
```

#### Get Event Details

```
GET /api/events/{id}/
```

**Response:**
```json
{
  "id": 1,
  "title": "Sunday Worship",
  "description": "Main weekly service",
  "event_date": "2026-02-01",
  "event_time": "09:00:00",
  "location": "Main Hall",
  "image": "http://localhost:8000/media/events/worship.jpg",
  "created_at": "2026-01-31T10:00:00Z",
  "updated_at": "2026-01-31T10:00:00Z"
}
```

#### Update Event

```
PUT /api/events/{id}/
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "event_date": "2026-02-01",
  "event_time": "10:00:00"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Main weekly service",
  "event_date": "2026-02-01",
  "event_time": "10:00:00",
  "location": "Main Hall",
  "image": "http://localhost:8000/media/events/worship.jpg",
  "created_at": "2026-01-31T10:00:00Z",
  "updated_at": "2026-01-31T11:30:00Z"
}
```

#### Delete Event

```
DELETE /api/events/{id}/
```

**Response (204 No Content)**

### Sermons

#### List Sermons

```
GET /api/sermons/
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "title": "Faith in God",
      "description": "A message about faith",
      "preacher": "Pastor John",
      "date": "2026-01-26",
      "image": "http://localhost:8000/media/sermons/faith.jpg",
      "video_url": "https://www.youtube.com/embed/abc123",
      "created_at": "2026-01-31T10:00:00Z"
    }
  ]
}
```

### Gallery

#### List Gallery Images

```
GET /api/photogallery/
```

**Query Parameters:**
- `category` - Filter by category
- `search` - Search by title

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "title": "Sunday Service",
      "category": "Worship",
      "image": "http://localhost:8000/media/gallery/service.jpg",
      "created_at": "2026-01-31T10:00:00Z"
    }
  ]
}
```

### Branches

#### List Branches

```
GET /api/branches/
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "Main Branch",
      "location": "123 Church Street",
      "phone": "+1-234-567-8900",
      "email": "main@tga.church",
      "image": "http://localhost:8000/media/branches/main.jpg",
      "created_at": "2026-01-31T10:00:00Z"
    }
  ]
}
```

### Contact Messages

#### Submit Contact Message

```
POST /api/contactmessage/
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "subject": "Prayer Request",
  "message": "Please pray for my family"
}
```

**Validation Rules:**
- `name` - Required, max 100 characters
- `email` - Required, valid email format
- `phone` - Optional, max 20 characters
- `subject` - Required, max 200 characters
- `message` - Required, max 5000 characters

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "subject": "Prayer Request",
  "message": "Please pray for my family",
  "created_at": "2026-01-31T11:00:00Z"
}
```

## File Upload Guidelines

### Image Uploads

**Allowed Types:** JPEG, PNG, GIF, WebP
**Max Size:** 10 MB
**Dimensions:** Recommended 1920x1080 minimum

**Example:**
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: multipart/form-data" \
  -F "title=New Event" \
  -F "event_date=2026-02-15" \
  -F "event_time=14:00" \
  -F "location=Main Hall" \
  -F "image=@/path/to/image.jpg"
```

### Validation Error Response

```json
{
  "image": ["File size must be no more than 10MB"]
}
```

## Pagination

All list endpoints return paginated results (25 items per page by default).

### Pagination Response

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/events/?page=2",
  "previous": null,
  "results": [...]
}
```

### Getting Specific Page

```
GET /api/events/?page=2
```

## Search & Filtering

### Search Example

```
GET /api/events/?search=sunday
```

### Ordering Example

```
GET /api/events/?ordering=-created_at
```

Reverse order: `-created_at`
Forward order: `created_at`

## Rate Limiting

Currently not enforced. Recommended for production:
- 1000 requests per hour per IP
- 100 requests per minute per IP

## CORS

Allowed origins configured in `settings.py`:
- `http://localhost:3000` (React/Vue dev)
- `http://localhost:5173` (Vite dev)
- Add your frontend URL in production

## Testing Endpoints

### Using cURL

```bash
# Get all events
curl http://localhost:8000/api/events/

# Create event
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{"title":"New Event","event_date":"2026-02-15"}'
```

### Using Postman

1. Import collection: `docs/postman_collection.json` (if available)
2. Set `base_url` to `http://localhost:8000/api/`
3. Test each endpoint

## Troubleshooting

**401 Unauthorized:** Authentication required (if enforced)
**403 Forbidden:** Permission denied (check user role)
**404 Not Found:** Resource doesn't exist
**500 Internal Error:** Check `logs/django.log`

---

**Last Updated:** January 2026
