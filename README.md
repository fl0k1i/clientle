# Product Search API — Getting Started

Search millions of products across thousands of stores with a single API call.

---

## Requirements

- Docker installed on your machine
- Your API key (provided after purchase)

> Don't have Docker? Download it at https://docs.docker.com/get-docker/

---

## Step 1 — Start the API

Run this one command. Replace `YOUR_LICENSE_KEY` with the key you received after purchase:

```bash
docker run -d \
  --name product-search-api \
  --restart unless-stopped \
  -p 8000:8000 \
  -e API_LICENSE_KEY=YOUR_LICENSE_KEY \
  napeir/product-search-api:latest
```

Your API is now running at `http://localhost:8000`

Verify it's up:

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## Step 2 — Create your account and get your API key

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'
```

Response:

```json
{
  "message": "Account created",
  "email": "you@example.com",
  "api_key": "sk-abc123...",
  "hint": "Pass your api_key as the x-api-key header on all requests"
}
```

**Save your `api_key`. You will need it for every request.**

If you ever lose it, retrieve it with:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'
```

---

## Step 3 — Make your first search

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"query": "nike running shoes", "limit": 5}'
```

That's it. You're searching millions of products.

---

## All Endpoints

### Search products

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"query": "white sneakers", "limit": 10}'
```

### Search with filters

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "query": "running shoes",
    "limit": 10,
    "filters": {
      "availability": ["InStock"],
      "price": {"min_price": 50, "max_price": 150},
      "gender": "male"
    }
  }'
```

### Search by image URL

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"image_url": "https://example.com/shoe.jpg"}'
```

### Get product detail

Take a product `id` from any search result and fetch full details:

```bash
curl http://localhost:8000/products/PRODUCT_ID \
  -H "x-api-key: YOUR_API_KEY"
```

### Get similar products

```bash
curl http://localhost:8000/products/PRODUCT_ID/similar \
  -H "x-api-key: YOUR_API_KEY"
```

### Lookup product by URL

Have a product page URL? Get structured data for it:

```bash
curl "http://localhost:8000/lookup?url=https://www.nike.com/t/air-max-90" \
  -H "x-api-key: YOUR_API_KEY"
```

---

## Search Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | one of these three | Text search |
| `image_url` | string | one of these three | Search by image URL |
| `base64_image` | string | one of these three | Search by base64 image |
| `limit` | integer | No | Results per page, max 30. Default 20 |
| `page_token` | string | No | Pass `next_page_token` from previous response to get next page |
| `filters` | object | No | See filters below |
| `config` | object | No | See config below |

### Filters

| Field | Type | Example |
|---|---|---|
| `availability` | list | `["InStock"]` or `["InStock", "OutOfStock"]` |
| `price` | object | `{"min_price": 50, "max_price": 200}` |
| `gender` | string | `"male"` or `"female"` |
| `brand_ids` | list | `["nike", "adidas"]` |
| `website_ids` | list | `["nike.com", "adidas.com"]` |
| `category_ids` | list | `["shoes", "sneakers"]` |
| `condition` | string | `"new"` or `"used"` |

### Config

| Field | Type | Example |
|---|---|---|
| `country` | string | `"US"`, `"GB"`, `"DE"` |
| `currency` | string | `"USD"`, `"GBP"`, `"EUR"` |
| `language` | string | `"en"`, `"de"`, `"fr"` |

---

## Pagination

Search responses include a `next_page_token` field. Pass it in your next request to get the next page:

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"query": "shoes", "limit": 20, "page_token": "TOKEN_FROM_PREVIOUS_RESPONSE"}'
```

When `next_page_token` is `null`, you have reached the last page.

---

## Example Response

```json
{
  "products": [
    {
      "id": "VIpe8QG",
      "title": "Gazelle Shoes",
      "description": "Classic sneakers with suede upper...",
      "brands": [{"id": "wTC7", "name": "Adidas"}],
      "images": [
        {
          "url": "https://cdn.example.com/shoe.jpg",
          "is_main_image": true,
          "shot_type": "hero",
          "alt_text": "Side view of Gazelle shoe"
        }
      ],
      "category": {"slug": "shoes", "title": "Shoes"},
      "gender": "male",
      "materials": ["suede"],
      "key_features": ["suede upper", "gum rubber sole"],
      "offers": [
        {
          "url": "https://www.adidas.com/...",
          "domain": "adidas.com",
          "price": {"price": 100.0, "currency": "USD"},
          "availability": "InStock"
        }
      ],
      "structured_attributes": {
        "color": ["Blue", "Pink"],
        "closure-type": ["Lace-up"],
        "shoe-size": ["7", "8", "9", "10"]
      }
    }
  ],
  "next_page_token": "eyJjYWNoZV9rZXki..."
}
```

---

## Useful Tips

**Only show in-stock products** — add `"availability": ["InStock"]` to your filters to exclude sold-out items.

**Use `is_main_image: true`** to pick the primary product image for display.

**Multiple offers per product** — each product can have offers from several stores. Sort by price to show the cheapest option.

---

## Interactive Docs

Your running API includes a full interactive documentation page. Open in your browser:

```
http://localhost:8000/docs
```

---

## Managing the Container

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
docker run -d --name product-search-api --restart unless-stopped -p 8000:8000 -e API_LICENSE_KEY=YOUR_KEY napeir/product-search-api:latest
```

---

## Error Reference

| Code | Meaning | Fix |
|---|---|---|
| 401 | Invalid API key | Check your `x-api-key` header |
| 422 | Bad request | Provide at least one of: query, image_url, base64_image |
| 504 | Timeout | Retry the request |
| 502 | Server error | Retry in a few seconds |

---

## Support

Questions or issues? Email: **your@email.com**