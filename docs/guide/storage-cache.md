# Storage & Cache

cdpwave provides full coverage of the `Storage`, `CacheStorage`, and
`IndexedDB` domains for managing cookies, quotas, IndexedDB, Cache API,
and other storage mechanisms.

## Storage domain

### Clear data for an origin

```python
await session.storage.clear_data_for_origin(
    origin="https://example.com",
    storage_types="cookies,local_storage,indexeddb,cache_storage",
)
```

### Get usage and quota

```python
result = await session.storage.get_usage_and_quota(
    origin="https://example.com",
)
print(f"Usage: {result['usage']} bytes")
print(f"Quota: {result['quota']} bytes")
for bucket in result["usageBreakdown"]:
    print(f"  {bucket['storageType']}: {bucket['usage']} bytes")
```

### Track IndexedDB for an origin

```python
await session.storage.track_indexed_db_for_origin(
    origin="https://example.com",
)

# Listen for updates
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

```python
result = await session.storage.get_storage_key_for_frame(
    frame_id="frame1",
)
print(f"Storage key: {result['storageKey']}")
```

### Trust tokens

```python
# Get trust token count
result = await session.storage.get_trust_tokens()
for token in result["tokens"]:
    print(f"{token['issuerOrigin']}: {token['count']} tokens")

# Clear trust tokens
await session.storage.clear_trust_tokens(issuer_origin="https://issuer.example.com")
```

### Shared storage

```python
await session.storage.set_shared_storage_tracking(
    tracking=True,
    host="example.com",
)
```

---

## CacheStorage domain

### Request cache names

```python
await session.cache_storage.request_cache_names(
    security_origin="https://example.com",
)

async def on_caches_updated(event: dict) -> None:
    for cache in event["caches"]:
        print(f"Cache: {cache['cacheName']}")

session.on("CacheStorage.cacheNamesUpdated", on_caches_updated)
```

### Delete a cache

```python
await session.cache_storage.delete_cache(
    cache_id="cache1",
)
```

### Request cached responses

```python
await session.cache_storage.request_cached_response(
    cache_id="cache1",
    request_url="https://example.com/data.json",
)
```

---

## IndexedDB domain

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

### Request database

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

```python
await session.indexed_db.clear_object_store(
    security_origin="https://example.com",
    database_name="mydb",
    object_store_name="items",
)
```

---

## Network cookies

The `Network` domain also provides cookie management:

### Get all cookies (all contexts)

```python
cookies = await session.network.get_all_cookies()
for cookie in cookies["cookies"]:
    print(f"{cookie['name']}={cookie['value']} domain={cookie['domain']}")
```

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
