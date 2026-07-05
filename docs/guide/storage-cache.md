# Storage & Cache

cdpwave provides full coverage of the `Storage`, `CacheStorage`, and
`IndexedDB` domains for managing cookies, quotas, IndexedDB, Cache API,
and other storage mechanisms.

## Browser storage overview

Modern browsers provide several storage mechanisms, each with
different lifetimes, capacities, and use cases:

| Mechanism | Domain | Lifetime | Capacity | Typical use |
|---|---|---|---|---|
| Cookies | `Network` / `Storage` | Per-expiry | ~4KB | Auth, tracking |
| LocalStorage | `Storage` | Permanent | ~5-10MB | UI state, preferences |
| SessionStorage | `Storage` | Tab lifetime | ~5-10MB | Per-tab state |
| IndexedDB | `IndexedDB` | Permanent | Large (quota) | Structured data |
| Cache API | `CacheStorage` | Permanent | Large (quota) | PWA offline assets |

All storage is **origin-scoped** — each origin (`https://example.com`)
has its own isolated storage. The `Storage` domain provides
origin-level operations, while `IndexedDB` and `CacheStorage` provide
fine-grained access to their respective stores.

## Storage domain

The `Storage` domain manages origin-level storage: clearing data,
checking quotas, and tracking changes.

### Clear data for an origin

Clear specific storage types for an origin:

```python
await session.storage.clear_data_for_origin(
    origin="https://example.com",
    storage_types="cookies,local_storage,indexeddb,cache_storage",
)
```

`storage_types` is a comma-separated list. Available types:
`cookies`, `local_storage`, `indexeddb`, `cache_storage`,
`file_systems`, `shader_cache`, `service_workers`, `websql`.

!!! warning "This is destructive"
    `clear_data_for_origin` permanently deletes all data of the
    specified types for the origin. Use with caution.

### Get usage and quota

Check how much storage an origin is using:

```python
result = await session.storage.get_usage_and_quota(
    origin="https://example.com",
)
print(f"Usage: {result['usage']} bytes")
print(f"Quota: {result['quota']} bytes")
for bucket in result["usageBreakdown"]:
    print(f"  {bucket['storageType']}: {bucket['usage']} bytes")
```

`usageBreakdown` shows per-type usage (cookies, local_storage,
indexeddb, etc.), helping identify which storage mechanism consumes
the most space.

### Track IndexedDB for an origin

Receive notifications when IndexedDB databases change:

```python
await session.storage.track_indexed_db_for_origin(
    origin="https://example.com",
)

async def on_idb_updated(event: dict) -> None:
    print(f"IndexedDB updated: {event['origin']}")

session.on("Storage.indexedDBListUpdated", on_idb_updated)
```

### Untrack IndexedDB

```python
await session.storage.untrack_indexed_db_for_origin(
    origin="https://example.com",
)
```

### Track Cache Storage for an origin

```python
await session.storage.track_cache_storage_for_origin(
    origin="https://example.com",
)

async def on_cache_updated(event: dict) -> None:
    print(f"Cache Storage updated: {event['origin']}")

session.on("Storage.cacheStorageListUpdated", on_cache_updated)
```

### Untrack Cache Storage

```python
await session.storage.untrack_cache_storage_for_origin(
    origin="https://example.com",
)
```

### Get storage key for a frame

Each frame has a storage key (similar to origin but includes
storage partitioning):

```python
result = await session.storage.get_storage_key_for_frame(
    frame_id="frame1",
)
print(f"Storage key: {result['storageKey']}")
```

### Trust tokens

Privacy Pass trust tokens allow anonymous access tokens:

```python
# Get trust token count
result = await session.storage.get_trust_tokens()
for token in result["tokens"]:
    print(f"{token['issuerOrigin']}: {token['count']} tokens")

# Clear trust tokens
await session.storage.clear_trust_tokens(issuer_origin="https://issuer.example.com")
```

### Shared storage

Track shared storage operations for an origin:

```python
await session.storage.set_shared_storage_tracking(
    tracking=True,
    host="example.com",
)
```

## CacheStorage domain

The `CacheStorage` domain inspects and manages the Cache API — the
storage used by service workers for offline assets.

### Request cache names

List all caches for an origin:

```python
await session.cache_storage.request_cache_names(
    security_origin="https://example.com",
)

async def on_caches_updated(event: dict) -> None:
    for cache in event["caches"]:
        print(f"Cache: {cache['cacheName']} (id: {cache['cacheId']})")

session.on("CacheStorage.cacheNamesUpdated", on_caches_updated)
```

### Delete a cache

```python
await session.cache_storage.delete_cache(
    cache_id="cache1",
)
```

### Request cached responses

Retrieve a cached response by URL:

```python
await session.cache_storage.request_cached_response(
    cache_id="cache1",
    request_url="https://example.com/data.json",
)
```

## IndexedDB domain

The `IndexedDB` domain inspects and manipulates IndexedDB databases.
IndexedDB is a transactional object store for structured data.

### Request database names

```python
await session.indexed_db.request_database_names(
    security_origin="https://example.com",
)

async def on_databases(event: dict) -> None:
    for db in event["databasesNames"]:
        print(f"Database: {db}")

session.on("IndexedDB.databaseNamesUpdated", on_databases)
```

### Request database details

Get object stores, indexes, and key paths:

```python
await session.indexed_db.request_database(
    security_origin="https://example.com",
    database_name="mydb",
)
```

### Request data from object store

```python
await session.indexed_db.request_data(
    security_origin="https://example.com",
    database_name="mydb",
    object_store_name="items",
    index_name="",
    skip_count=0,
    page_size=100,
)
```

### Delete database

```python
await session.indexed_db.delete_database(
    security_origin="https://example.com",
    database_name="mydb",
)
```

### Clear object store

Remove all records from an object store without deleting the
database:

```python
await session.indexed_db.clear_object_store(
    security_origin="https://example.com",
    database_name="mydb",
    object_store_name="items",
)
```

## Network cookies

The `Network` domain provides cookie management. Cookies are shared
across all tabs for the same browser profile.

### Get all cookies (all contexts)

```python
cookies = await session.network.get_all_cookies()
for cookie in cookies["cookies"]:
    print(f"{cookie['name']}={cookie['value']} domain={cookie['domain']}")
```

### Cookie fields

| Field | Description |
|---|---|
| `name` | Cookie name |
| `value` | Cookie value |
| `domain` | Domain the cookie applies to |
| `path` | URL path prefix |
| `secure` | Only sent over HTTPS |
| `httpOnly` | Not accessible via JS |
| `sameSite` | `"Strict"`, `"Lax"`, or `"None"` |
| `expires` | Expiry as Unix timestamp (-1 = session cookie) |

### Set a cookie

```python
await session.network.set_cookie(
    name="session",
    value="abc123",
    domain="example.com",
    path="/",
    secure=True,
    http_only=True,
    same_site="Lax",
    expires=1893456000,  # Unix timestamp
)
```

!!! tip "SameSite defaults"
    Modern browsers require `SameSite=Lax` or `SameSite=None` with
    `Secure=True` for cross-site cookies. Session cookies
    (`expires=-1`) are deleted when the browser closes.

### Delete a cookie

```python
await session.network.delete_cookie(
    name="session",
    domain="example.com",
    path="/",
)
```

### Clear all browser cookies

```python
await session.network.clear_browser_cookies()
```

!!! warning "Global scope"
    `clear_browser_cookies()` clears cookies for **all** origins,
    not just the current page. This affects all tabs sharing the
    same browser profile.

## Full example

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page()
        await session.page.enable()
        await session.network.enable()

        # Navigate
        loaded = asyncio.Event()

        async def on_load(_: dict) -> None:
            loaded.set()

        session.on("Page.loadEventFired", on_load)
        await session.page.navigate("https://example.com")
        await asyncio.wait_for(loaded.wait(), timeout=10.0)

        # Check storage usage
        usage = await session.storage.get_usage_and_quota(
            origin="https://example.com",
        )
        print(f"Usage: {usage['usage']} / {usage['quota']} bytes")

        # List cookies
        cookies = await session.network.get_all_cookies()
        print(f"Cookies: {len(cookies['cookies'])}")
        for c in cookies["cookies"]:
            print(f"  {c['name']}={c['value'][:20]}... domain={c['domain']}")

        # Check IndexedDB
        await session.indexed_db.request_database_names(
            security_origin="https://example.com",
        )
        await asyncio.sleep(1)  # Wait for event

        # Clean up
        await session.storage.clear_data_for_origin(
            origin="https://example.com",
            storage_types="cookies,local_storage,indexeddb,cache_storage",
        )
        print("Storage cleared")

        await session.close()

asyncio.run(main())
```
