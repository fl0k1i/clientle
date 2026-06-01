# Product Search API

Search millions of products across thousands of stores.

---

## Before You Start

You need Docker. If you don't have it:
- Mac / Windows → https://www.docker.com/products/docker-desktop
- Linux → `sudo apt install docker.io`

---

## Step 1 — Start the API

Copy and run this command. Replace `YOUR_LICENSE_KEY` with the key you received after purchase:

```bash
docker run -d --name product-search-api --restart unless-stopped -p 8000:8000 -e CHANNEL3_API_KEY=YOUR_LICENSE_KEY napeir/product-search-api:latest
```

Check it's running:

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok"}`

---

## Step 2 — Generate Your API Key

Run this once. Use your own email and a password you choose:

```bash
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"email": "you@example.com", "password": "yourpassword"}'
```

Response:

```json
{
  "message": "Account created",
  "email": "you@example.com",
  "api_key": "sk-xxxxxxxxxxxxxxxx"
}
```

**Copy your `api_key`. You will use it in every request.**

Lost it? Get it back anytime:

```bash
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email": "you@example.com", "password": "yourpassword"}'
```

---

## Step 3 — Test It

Replace `YOUR_API_KEY` with the key from above:

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "nike shoes", "limit": 5}'
```

You should get back a list of products with titles, images, prices, and store links.

---

## All Commands

**Search by text**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "white sneakers", "limit": 10}'
```

**In stock only**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "white sneakers", "limit": 10, "filters": {"availability": ["InStock"]}}'
```

**With price range**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "running shoes", "filters": {"availability": ["InStock"], "price": {"min_price": 50, "max_price": 150}}}'
```

**By gender**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "sneakers", "filters": {"gender": "male"}}'
```

**By image URL**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"image_url": "https://example.com/shoe.jpg"}'
```

**Product detail** (use an `id` from any search result)
```bash
curl http://localhost:8000/products/PRODUCT_ID -H "x-api-key: YOUR_API_KEY"
```

**Similar products**
```bash
curl http://localhost:8000/products/PRODUCT_ID/similar -H "x-api-key: YOUR_API_KEY"
```

**Lookup by store URL**
```bash
curl "http://localhost:8000/lookup?url=https://www.nike.com/t/air-max-90" -H "x-api-key: YOUR_API_KEY"
```

**Next page of results**
```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "shoes", "page_token": "TOKEN_FROM_PREVIOUS_RESPONSE"}'
```

---

## Filter Options

| Filter | What it does | Example |
|---|---|---|
| `availability` | In stock or not | `["InStock"]` |
| `price` | Price range | `{"min_price": 50, "max_price": 200}` |
| `gender` | Filter by gender | `"male"` or `"female"` |
| `website_ids` | Specific stores only | `["nike.com", "adidas.com"]` |
| `brand_ids` | Specific brands only | `["nike", "adidas"]` |
| `condition` | New or used | `"new"` or `"used"` |

## Config Options

| Config | What it does | Example |
|---|---|---|
| `country` | Store region | `"US"`, `"GB"`, `"DE"` |
| `currency` | Price currency | `"USD"`, `"GBP"`, `"EUR"` |
| `language` | Result language | `"en"`, `"de"`, `"fr"` |

Example using config:

```bash
curl -X POST http://localhost:8000/search -H "Content-Type: application/json" -H "x-api-key: YOUR_API_KEY" -d '{"query": "shoes", "filters": {"availability": ["InStock"]}, "config": {"country": "GB", "currency": "GBP"}}'
```

---

## What a Response Looks Like

```json
{
  "products": [
    {
      "id": "VIpe8QG",
      "title": "Gazelle Shoes",
      "description": "Classic sneakers with suede upper and gum sole.",
      "brands": [{ "name": "Adidas" }],
      "images": [
        {
          "url": "https://cdn.example.com/shoe.jpg",
          "is_main_image": true
        }
      ],
      "gender": "male",
      "key_features": ["suede upper", "gum rubber sole"],
      "offers": [
        {
          "domain": "adidas.com",
          "url": "https://www.adidas.com/...",
          "price": { "price": 100.0, "currency": "USD" },
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

- Use `is_main_image: true` to get the primary product image
- `offers` lists every store selling the product with live price and availability
- `next_page_token` is `null` when there are no more results

---

## Interactive Docs

Your API has a built-in docs page where you can try every endpoint in the browser:

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

# See logs
docker logs product-search-api

# Update to latest version
docker pull napeir/product-search-api:latest
docker stop product-search-api
docker rm product-search-api
docker run -d --name product-search-api --restart unless-stopped -p 8000:8000 -e CHANNEL3_API_KEY=YOUR_LICENSE_KEY napeir/product-search-api:latest
```

---

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `401` | Missing or wrong API key | Check the `x-api-key` header |
| `409` | Email already registered | Use a different email or login instead |
| `422` | Bad request | Include `query`, `image_url`, or `base64_image` |
| `504` | Timeout | Retry the request |
| `502` | Server error | Retry in a few seconds |

---

## Support

Email: **your@email.com**