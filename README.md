# Product Search API

Search millions of products across thousands of stores instantly.

---

## Requirements

Docker must be installed on your machine.
- Mac / Windows → https://www.docker.com/products/docker-desktop
- Linux → `sudo apt install docker.io`

---

## Step 1 — Start the API

Replace `YOUR_LICENSE_KEY` with the key provided after purchase:

```bash
docker run -d --name product-search-api --restart unless-stopped -p 8000:8000 -e CHANNEL3_API_KEY=YOUR_LICENSE_KEY napeir/product-search-api:latest
```

Confirm it's running:

```bash
curl http://localhost:8000/health
```

Expected response: `{"status":"ok"}`

---

## Step 2 — Create Your Account

Run this once with your own email and password:

```bash
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"email": "you@example.com", "password": "yourpassword"}'
```

Response:

```json
{
  "message": "Account created",
  "email": "you@example.com",
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

**Save your `api_key`. You need it for every request.**

---

## Step 3 — Retrieve Your Key (if lost)

```bash
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email": "you@example.com", "password": "yourpassword"}'
```

---

## Step 4 — Make Your First Search

Replace `YOUR_API_KEY` with the key from Step 2:

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "nike shoes", "limit": 5}'
```

---

## All Search Commands

**Basic search**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "white sneakers", "limit": 10}'
```

**In stock only**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "white sneakers", "filters": {"availability": ["InStock"]}}'
```

**With price range**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "running shoes", "filters": {"availability": ["InStock"], "price": {"min_price": 50, "max_price": 150}}}'
```

**Filter by gender**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "sneakers", "filters": {"gender": "male"}}'
```

**Filter by specific stores**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "nike shoes", "filters": {"website_ids": ["nike.com", "adidas.com"]}}'
```

**Filter by brand**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "shoes", "filters": {"brand_ids": ["nike", "adidas"]}}'
```

**Search by image URL**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"image_url": "https://example.com/shoe.jpg"}'
```

**Set country and currency**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "shoes", "config": {"country": "GB", "currency": "GBP"}}'
```

**Next page of results**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "shoes", "page_token": "TOKEN_FROM_PREVIOUS_RESPONSE"}'
```

---

## Product Endpoints

**Get full product detail** (use an `id` from any search result)
```bash
curl http://localhost:8000/products/PRODUCT_ID -H "x-api-key: YOUR_API_KEY"
```

**Get similar products**
```bash
curl http://localhost:8000/products/PRODUCT_ID/similar -H "x-api-key: YOUR_API_KEY"
```

**Lookup any product page URL**
```bash
curl "http://localhost:8000/lookup?url=https://www.nike.com/t/air-max-90" -H "x-api-key: YOUR_API_KEY"
```

---

## Filter & Config Reference

| Filter | Type | Example |
|---|---|---|
| `availability` | list | `["InStock"]` |
| `price` | object | `{"min_price": 50, "max_price": 200}` |
| `gender` | string | `"male"` or `"female"` |
| `brand_ids` | list | `["nike", "adidas"]` |
| `website_ids` | list | `["nike.com", "zappos.com"]` |
| `condition` | string | `"new"` or `"used"` |

| Config | Type | Example |
|---|---|---|
| `country` | string | `"US"`, `"GB"`, `"DE"` |
| `currency` | string | `"USD"`, `"GBP"`, `"EUR"` |
| `language` | string | `"en"`, `"de"`, `"fr"` |

---

## Example Response

```json
{
  "products": [
    {
      "id": "VIpe8QG",
      "title": "Gazelle Shoes",
      "description": "Classic sneakers with suede upper...",
      "brands": [{"name": "Adidas"}],
      "images": [
        {
          "url": "https://cdn.example.com/shoe.jpg",
          "is_main_image": true,
          "shot_type": "hero"
        }
      ],
      "gender": "male",
      "key_features": ["suede upper", "gum rubber sole"],
      "offers": [
        {
          "domain": "adidas.com",
          "url": "https://www.adidas.com/...",
          "price": {"price": 100.0, "currency": "USD"},
          "availability": "InStock"
        }
      ],
      "structured_attributes": {
        "color": ["Blue", "Pink"],
        "shoe-size": ["7", "8", "9", "10"],
        "closure-type": ["Lace-up"]
      }
    }
  ],
  "next_page_token": "eyJjYWNoZV9rZXki..."
}
```

**Tips:**
- Use `is_main_image: true` to get the primary product image
- `offers` lists every store selling the product — sort by price to show the cheapest
- `next_page_token` is `null` when there are no more pages

---

## Interactive Docs

Open in your browser to explore and test every endpoint visually:

```
http://localhost:8000/docs
```

---

## Managing Docker

```bash
# Stop the API
docker stop product-search-api

# Start it again
docker start product-search-api

# View logs
docker logs product-search-api

# Update to latest version
docker pull napeir/product-search-api:latest
docker stop product-search-api
docker rm product-search-api
docker run -d --name product-search-api --restart unless-stopped -p 8000:8000 -e CHANNEL3_API_KEY=YOUR_LICENSE_KEY napeir/product-search-api:latest
```

---

## Error Reference

| Code | Meaning | Fix |
|---|---|---|
| `401` | Missing or invalid API key | Check your `x-api-key` header |
| `409` | Email already registered | Login instead to retrieve your key |
| `422` | Bad request | Include `query`, `image_url`, or `base64_image` |
| `504` | Timeout | Retry the request |
| `502` | Server error | Retry in a few seconds |

---

## Support

Email: **your@email.com**