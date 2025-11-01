# Testing Real-Time Inventory Updates

## What Should Happen

When you call `POST /api/v1/items/{uuid}/borrow`, the inventory on the web app should update **instantly** without refreshing the page.

## Step-by-Step Test

### 1. Verify Backend Configuration

**Check `backend-laravel/.env`:**
```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=your-app-id
REVERB_APP_KEY=your-app-key
REVERB_APP_SECRET=your-app-secret
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http
```

**Clear config cache:**
```bash
cd backend-laravel
php artisan config:clear
```

### 2. Verify Frontend Configuration

**Check `frontend-vue/.env` (create if it doesn't exist):**
```env
VITE_PUSHER_APP_KEY=your-app-key  # Must match REVERB_APP_KEY exactly!
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
VITE_API_BASE_URL=http://localhost:8000
```

**Restart frontend dev server** after adding/changing `.env`:
```bash
cd frontend-vue
# Stop (Ctrl+C) and restart
npm run dev
```

### 3. Start Reverb Server

**In a separate terminal:**
```bash
cd backend-laravel
php artisan reverb:start
```

**Keep this terminal open!** You should see:
```
INFO Starting server on 0.0.0.0:8080 (localhost).
```

This means Reverb is running and waiting for connections.

### 4. Open Web App and Check Console

1. Open your web app in browser
2. Navigate to Inventory page
3. Open Developer Console (F12)
4. Look for these messages:
   - `🚀 Laravel Echo initialized`
   - `📡 Connecting to: localhost:8080`
   - `✅ Laravel Echo connected successfully`
   - `👂 Listening on channel: inventory`
   - `📡 Waiting for ItemUpdated events...`

### 5. Test the Borrow API

**From your mobile app or Postman:**

```bash
POST http://localhost:8000/api/v1/items/{uuid}/borrow
Content-Type: application/json

{
  "quantity": 1,
  "borrowed_by": "Test User"
}
```

### 6. Verify Real-Time Update

**In browser console, you should see:**
```
📦 Item updated via Echo: {item: {...}}
✅ Updated item {id} in real-time. New quantity: {new-quantity}
```

**In Inventory page:**
- Item quantity should update **instantly** without page refresh!

### 7. Check Backend Logs

**In `backend-laravel/storage/logs/laravel.log`, you should see:**
```
[INFO] Broadcasting ItemUpdated event for item: {id} (UUID: {uuid}), New quantity: {quantity}
[INFO] ItemUpdated event dispatched successfully for item: {id}
[INFO] ItemUpdated event will broadcast on driver: reverb
[INFO] ItemUpdated event broadcasting on 'inventory' channel for item: {id}
[INFO] ItemUpdated broadcast data prepared for item: {id}, Quantity: {quantity}
```

## Troubleshooting

### Issue: Console shows "Echo is not connected"

**Fix:**
1. Check that `REVERB_APP_KEY` (backend) equals `VITE_PUSHER_APP_KEY` (frontend)
2. Verify Reverb server is running
3. Check browser console for connection errors
4. See `CHECK_ECHO_CONNECTION.md` for detailed troubleshooting

### Issue: Event fires but no update in UI

**Fix:**
1. Check browser console for `📦 Item updated via Echo:` message
2. Verify the item ID/UUID matches what's in the inventory list
3. Check if item is filtered out or on a different page

### Issue: No broadcast logs in backend

**Fix:**
1. Check `BROADCAST_DRIVER=reverb` in `.env`
2. Run `php artisan config:clear`
3. Verify `shouldBroadcast()` returns `true` in `ItemUpdated.php`

### Issue: Reverb server not connecting

**Fix:**
1. Check port 8080 is not blocked
2. Verify firewall allows WebSocket connections
3. Try changing port to 8081 in both `.env` files
4. Restart Reverb server

## Expected Flow

```
Mobile App
   ↓
POST /api/v1/items/{uuid}/borrow
   ↓
ItemController::borrowItem()
   ↓
Update item quantity
   ↓
event(new ItemUpdated($item))
   ↓
ItemUpdated::shouldBroadcast() → true
   ↓
ItemUpdated::broadcastOn() → Channel('inventory')
   ↓
Laravel Reverb Server
   ↓
WebSocket → Browser
   ↓
Laravel Echo receives event
   ↓
Inventory.vue listener triggers
   ↓
UI updates in real-time! ✨
```

