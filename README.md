# Django Product Inventory API

A scalable REST API for managing product inventory with flexible schema support.

## Tech Stack

**Django + DRF**: Production-proven framework with built-in ORM, security, and REST capabilities

**PostgreSQL with JSONB**: Native JSON support with indexing capabilities - provides flexibility without sacrificing queryability

**JSONField for Product Schema**: Products have diverse attributes (electronics vs clothing). Using JSON avoids constant schema migrations while maintaining query capabilities.

## API Endpoints

```
GET    /api/products/              List/filter products (?name=text&price_gte=100&price_lte=500&order=asc&page=1&limit=10)
POST   /api/products/              Create product
GET    /api/products/{id}/         Get product by ID
PUT    /api/products/{id}/         Update product (partial update supported)
DELETE /api/products/{id}/         Delete product
```

**Query Parameters:**
- `name` - Partial text search (case-insensitive)
- `price_gte`/`price_lte` - Price range filtering 
- `order` - Sort by price: `asc` or `desc`
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 10)

## Key Architecture Decisions

### 1. Database Indexing Strategy
```python
indexes = [
    GinIndex(fields=['fields']),  # For name text search
    models.Index(Func(..., function='jsonb_extract_path_text'))  # For price range queries
]
```

**Why two different index types:**
- **GIN Index**: Optimizes JSON text queries (name filtering with `icontains`)
- **B-tree Functional Index**: Optimizes numeric range queries (price `gte`/`lte`)

### 2. Pagination
**Default: 10 items per page**

**Reasoning:**
- Prevents large payload responses
- Reduces database load
- Essential for scalability as catalog grows

### 3. API Parameter Design
- `price_gte`/`price_lte`: Inclusive ranges match e-commerce conventions ("under $100" = ≤100)
- `order` instead of `sort_by`: Only price sorting supported, parameter indicates direction
- `name` uses `icontains`: Better UX for product search

## Scalability

**Current Implementation**
- ✅ Database Indexes (GIN + B-tree)
- ✅ Offset-based Pagination
- ✅ Database-side Filtering

## Setup

**Requirements:**
- Python 3.10+
- PostgreSQL 13+

**Installation:**

```bash
# Install dependencies
pip install django==5.1.4 djangorestframework==3.15.2 psycopg2-binary==2.9.10

# Create database
createdb products_db

# Update config/settings.py with your database credentials

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```