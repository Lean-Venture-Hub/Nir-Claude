# Yad2 Internal API — Deep Brief

**TL;DR:** Yad2 exposes two active API surfaces for real estate. The primary one is `gw.yad2.co.il/feed-search-legacy/{category}` which mirrors the frontend URL structure. A newer endpoint `gw.yad2.co.il/realestate-feed/{dealType}` exists for direct map/list queries with explicit params. Both return the same JSON shape: `response.data.feed.feed_items[]`.

---

## 1. API Endpoints

### Endpoint A — feed-search-legacy (primary, mirrors frontend URL)

```
GET https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?{params}
GET https://gw.yad2.co.il/feed-search-legacy/realestate/rent?{params}
```

**How it works:** Take any `www.yad2.co.il` search URL, replace the host with `gw.yad2.co.il` and prepend `/feed-search-legacy` to the path. The query string passes through unchanged.

Example transformation:
- Frontend: `https://www.yad2.co.il/realestate/forsale?city=5000&rooms=3-4`
- API: `https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?city=5000&rooms=3-4&page=1`

---

### Endpoint B — realestate-feed (newer, explicit params)

```
GET https://gw.yad2.co.il/realestate-feed/rent/map?city=5000&neighborhood=1520&area=1&topArea=2&minPrice=6000&maxPrice=14000&minRooms=3&maxRooms=4&zoom=15
GET https://gw.yad2.co.il/realestate-feed/forsale/map?city=5000&...
```

---

### Endpoint C — address/city lookup

```
GET https://gw.yad2.co.il/address-master/house-number?result_type=extended&city_id={id}&street_id={id}&house_number={n}&limit=10&page=1
GET https://gw.yad2.co.il/?text={settlement_name}   ← city code lookup
```

City code for Tel Aviv = **5000**

---

## 2. Query Parameters

### Endpoint A (feed-search-legacy) — for forsale/rent

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `city` | int | `5000` | Tel Aviv = 5000 |
| `neighborhood` | int | `1520` | neighborhood code |
| `topArea` | int | `2` | top-level area |
| `area` | int | `1` | sub-area |
| `rooms` | string | `3-4` | range, e.g. "2-5" |
| `minRooms` / `maxRooms` | float | `3` / `4` | alt form |
| `price` | string | `0-5000000` | range |
| `minPrice` / `maxPrice` | int | `1000000` / `5000000` | alt form |
| `propertyGroup` | string | `apartments,houses` | comma-separated |
| `forceLdLoad` | bool | `true` | include LD+JSON |
| `page` | int | `1` | 1-indexed |
| `dealType` | string | `forsale` / `rent` | path segment, not param |

### MaorBezalel project URL pattern (confirmed working):
```
{BASE_URL}/forsale?city={cityCode}&propertyGroup=apartments,houses&price={min}-{max}&page={n}&forceLdLoad=true
```

---

## 3. Required Headers

Two header sets confirmed from real working scrapers:

### Minimal (works for basic access):
```
Accept: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15
```

### Full headers (from MaorBezalel NestJS project — most complete, used in production):
```
accept: application/json, text/plain, */*
accept-language: he,en-US;q=0.9,en;q=0.8,he-IL;q=0.7
cache-control: no-cache
mainsite_version_commit: 7df239aaf60e32e2d821d103c72f454dee720ab2
mobile-app: false
pragma: no-cache
sec-ch-ua: "Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-site
Referer: https://www.yad2.co.il/
Referrer-Policy: strict-origin-when-cross-origin
cookie: guest_token=eyJ...   ← a guest JWT, needed for some responses
```

Key custom header: `mainsite_version_commit` — this is a commit SHA from Yad2's frontend deploy. It may need updating but is not always enforced.

Anti-bot note: Yad2 uses ShieldSquare/PerimeterX. Identifier in response body: `"Are you for real"`. Also watch for `noscript=1` cookie which disables JS-only content.

---

## 4. JSON Response Structure

```json
{
  "data": {
    "feed": {
      "feed_items": [ ... ],
      "total_items": 342,
      "total_pages": 18,
      "current_page": 1
    }
  }
}
```

**Path to listings array:** `response.data.feed.feed_items`

### Each listing item (`Yad2RealEstateItem`) contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Listing ID — also used as URL token: `yad2.co.il/item/{id}` |
| `title_1` | string | Street address |
| `neighborhood` | string | Neighborhood name |
| `city` | string | City name |
| `title_2` | string | Property type (apartment, house, etc.) |
| `price` | string | Price in ILS, formatted |
| `date` | string | Last updated: `"YYYY-MM-DD HH:MM:SS"` |
| `date_added` | string | When listed: `"YYYY-MM-DD HH:MM:SS"` |
| `row_4` | array | `[{value: rooms}, {value: floor}, {value: sqm}]` |
| `highlight_text` | string | `"תיווך"` = brokerage listing |

Note: `feed_items` array also contains advertisement/junk objects — filter by checking `'id' in item`.

---

## 5. Contradictions / Gotchas

- **Two active endpoints:** `feed-search-legacy` (path-mirroring) vs `realestate-feed` (explicit). The latter is newer but less documented. Both return same shape.
- **`mainsite_version_commit` header:** Some scrapers include it, others don't. Not always validated server-side.
- **Cookie / guest_token:** Required for some requests. Can be obtained by visiting `www.yad2.co.il` once without credentials.
- **Anti-bot:** ShieldSquare blocks scrapers aggressively. Rotating User-Agents + delays (4-8s) + residential proxies are recommended.
- **Old API (pre-2020):** `http://www.yad2.co.il/Nadlan/business.php?AreaID=&City=&Sale=&HomeTypeID=...` — dead, HTML-based, do not use.

---

## 6. Minimal Working Request (Python)

```python
import requests

url = "https://gw.yad2.co.il/feed-search-legacy/realestate/forsale"
params = {
    "city": "5000",          # Tel Aviv
    "propertyGroup": "apartments,houses",
    "price": "0-5000000",
    "page": 1,
    "forceLdLoad": "true"
}
headers = {
    "Accept": "application/json",
    "Referer": "https://www.yad2.co.il/",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118 Safari/537.36"
}

resp = requests.get(url, params=params, headers=headers)
listings = resp.json()["data"]["feed"]["feed_items"]
real_listings = [item for item in listings if "id" in item]
```

---

## Sources

| Repo | Key finding |
|------|-------------|
| [sagirub/Yad2NotificationBot](https://github.com/sagirub/Yad2NotificationBot) | Confirms `gw.yad2.co.il` host + `feed-search-legacy` path prefix; URL transformation logic |
| [MaorBezalel/real-estate-smart-agent](https://github.com/MaorBezalel/real-estate-smart-agent) | Full production TypeScript types: response shape, request params, headers, city code lookup |
| [SnirShnitzer/yad2-tracker](https://github.com/SnirShnitzer/yad2-tracker) | `realestate-feed` endpoint with map params, filter words, headers |
| [DavOstx7/yad2-scraper](https://github.com/DavOstx7/yad2-scraper) | Default headers, anti-bot detection identifiers |
| [ron-levi/yad2-analyzer](https://github.com/ron-levi/yad2-analyzer) | `gw.yad2.co.il/address-master/house-number` address lookup endpoint |
| [zahidadeel/yad2scrapper](https://github.com/zahidadeel/yad2scrapper) | Legacy param names (AreaID, City, Sale, HomeTypeID, etc.) — historical reference |
