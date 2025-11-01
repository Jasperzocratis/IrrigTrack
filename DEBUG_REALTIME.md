# Debug Real-Time Updates

## Quick Checks

### 1. Check Browser Console
Open browser console (F12) and look for:
- ❓ **Is Echo connected?** Look for: `✅ Laravel Echo connected successfully`
- ❓ **Is listener active?** Look for: `👂 Listening on channel: inventory`

### 2. Check Backend Logs
After borrowing, check `backend-laravel/storage/logs/laravel.log` for:
```
[INFO] Broadcasting ItemUpdated event for item: X
[INFO] ItemUpdated event will broadcast on driver: reverb
[INFO] ItemUpdated event broadcasting on 'inventory' channel
```

If you see warnings instead, broadcasting isn't configured.

### 3. Check Event Data Format
The frontend expects: `event.item.id` or `event.item.uuid`
Let's verify the broadcast data structure matches.

