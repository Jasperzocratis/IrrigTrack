# Real-Time Borrow Updates - Complete Setup Verification

## 📋 System Architecture

```
Mobile App (QR Scan) 
    ↓
POST /api/v1/items/{uuid}/borrow
    ↓
ItemController::borrowItem()
    ↓
Update item quantity in database
    ↓
event(new ItemUpdated($item))
    ↓
ItemUpdated Event → Laravel Reverb (WebSocket)
    ↓
Laravel Echo (Frontend) → Inventory.vue
    ↓
Vue reactive update (No page refresh!)
```

## ✅ Current Implementation Status

### Backend (Laravel)

1. **API Endpoint**: ✅ `POST /api/v1/items/{uuid}/borrow`
   - Location: `routes/api.php` line 81
   - Controller: `ItemController::borrowItem()`

2. **Event Broadcasting**: ✅ `ItemUpdated` Event
   - Location: `app/Events/ItemUpdated.php`
   - Broadcasts on: `inventory` channel
   - Event name: `ItemUpdated`
   - Driver: `reverb` (via `BROADCAST_DRIVER`)

3. **Event Firing**: ✅ After successful borrow
   - Location: `ItemController::borrowItem()` line 406
   - Code: `event(new ItemUpdated($item))`
   - Fires after quantity is saved to database

### Frontend (Vue.js)

1. **Echo Initialization**: ✅ `bootstrap.js`
   - Connects to Reverb server
   - Listens on WebSocket port 8080

2. **Channel Subscription**: ✅ `Inventory.vue`
   - Subscribes to: `inventory` channel
   - Listens for: `.ItemUpdated` events

3. **Real-Time Update**: ✅ Reactive Vue update
   - Finds item by ID/UUID
   - Updates quantity in real-time
   - No page refresh needed

## 🔧 Configuration Required

### Backend `.env` (`backend-laravel/.env`)

```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=your-app-id
REVERB_APP_KEY=your-app-key
REVERB_APP_SECRET=your-app-secret
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http
```

### Frontend `.env` (`frontend-vue/.env`)

```env
VITE_PUSHER_APP_KEY=your-app-key  # Must match REVERB_APP_KEY!
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🚀 Step-by-Step Verification

### Step 1: Start Reverb Server

**Terminal 1:**
```bash
cd backend-laravel
php artisan reverb:start
```

**Expected output:**
```
INFO Starting server on 0.0.0.0:8080 (localhost).
```

**Keep this terminal open!** Reverb must run continuously.

### Step 2: Verify Frontend Connection

1. **Open web app** in browser
2. **Navigate to Inventory page**
3. **Open Developer Console** (F12)

**Look for:**
```
✅ Laravel Echo connected successfully
✅ Successfully subscribed to inventory channel
🎧 Echo channel setup complete. Ready to receive events.
```

**If you see connection errors:**
- Check Reverb server is running
- Verify `VITE_PUSHER_APP_KEY` matches `REVERB_APP_KEY`
- Restart frontend dev server after changing `.env`

### Step 3: Test Real-Time Update

1. **Keep browser console open** (showing Inventory page)
2. **From mobile app:** Scan QR code and borrow an item
3. **Watch browser console immediately**

**Expected console output:**
```
📦 Item updated via Echo - Full event: {...}
📦 Event data structure: {...}
🔍 Looking for item with: {eventId: X, eventUuid: "...", currentItemsCount: Y}
🔧 Updating item at index: Z
✅ Quantity updated: OLD -> NEW
✅ Updated item X in real-time. New quantity: NEW
```

**Expected UI behavior:**
- Item quantity changes **instantly** on screen
- **No page refresh** required
- Update is **reactive** (Vue handles it automatically)

### Step 4: Verify Backend Logs

**Check `backend-laravel/storage/logs/laravel.log`:**

**Expected log entries:**
```
[INFO] Broadcasting ItemUpdated event for item: X (UUID: ...), New quantity: Y
[INFO] ItemUpdated::shouldBroadcast() called. Driver: reverb
[INFO] ItemUpdated event broadcasting on 'inventory' channel for item: X
[INFO] ItemUpdated broadcast data prepared for item: X, Quantity: Y
[INFO] ItemUpdated event dispatched successfully for item: X
```

## 🐛 Troubleshooting

### Issue: Events dispatched but not received

**Symptoms:**
- Backend logs show "ItemUpdated event dispatched"
- Browser console shows no "📦 Item updated via Echo"

**Possible causes:**
1. Reverb server not running
2. Echo not connected (check connection status)
3. Channel not subscribed (check subscription logs)
4. Keys don't match between backend/frontend

**Fix:**
1. Start Reverb: `php artisan reverb:start`
2. Clear config: `php artisan config:clear`
3. Verify keys match: `REVERB_APP_KEY` = `VITE_PUSHER_APP_KEY`
4. Restart frontend dev server

### Issue: Echo not connecting

**Symptoms:**
- Browser console shows connection errors
- Connection state is "disconnected"

**Possible causes:**
1. Reverb server not running
2. Port 8080 blocked by firewall
3. Keys don't match

**Fix:**
1. Verify Reverb is running
2. Check port 8080 is accessible
3. Verify keys match exactly
4. Check browser console for specific error messages

### Issue: Events received but inventory not updating

**Symptoms:**
- Browser console shows "📦 Item updated via Echo"
- But UI doesn't change

**Possible causes:**
1. Item not found in list (filtered out or different page)
2. Item ID/UUID mismatch
3. Vue reactivity issue

**Fix:**
1. Check console logs for item matching details
2. Verify item ID/UUID in event matches items in list
3. Check if item is on current page (pagination)
4. Fallback: List will refresh automatically if item not found

## 📊 Event Flow Diagram

```
┌─────────────┐
│ Mobile App  │
│ (QR Scan)   │
└──────┬──────┘
       │ POST /api/v1/items/{uuid}/borrow
       ↓
┌─────────────────────────┐
│ ItemController          │
│ borrowItem()            │
│ - Validate request      │
│ - Update quantity       │
│ - Save to database      │
│ - event(ItemUpdated)    │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│ ItemUpdated Event       │
│ - shouldBroadcast()      │
│ - broadcastOn('inventory')│
│ - broadcastWith(data)   │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│ Laravel Reverb          │
│ (WebSocket Server)      │
│ Port: 8080              │
└──────┬──────────────────┘
       │ WebSocket
       ↓
┌─────────────────────────┐
│ Laravel Echo            │
│ (Frontend)              │
│ - Connected to Reverb   │
│ - Subscribed to channel │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│ Inventory.vue           │
│ - Listens: .ItemUpdated │
│ - Finds item in array   │
│ - Updates quantity      │
│ - Vue reactive update   │
└─────────────────────────┘
```

## ✅ Verification Checklist

- [ ] Reverb server is running (`php artisan reverb:start`)
- [ ] Browser console shows "Echo connected successfully"
- [ ] Browser console shows "subscribed to inventory channel"
- [ ] Backend `.env` has `BROADCAST_DRIVER=reverb`
- [ ] Frontend `.env` has `VITE_PUSHER_APP_KEY` matching `REVERB_APP_KEY`
- [ ] Config cache cleared (`php artisan config:clear`)
- [ ] Test: Borrow item from mobile app
- [ ] Browser console shows "📦 Item updated via Echo"
- [ ] Inventory page updates quantity instantly (no refresh)

## 🎯 Expected Behavior

When a user borrows an item via mobile app:

1. ✅ Mobile app calls API: `POST /api/v1/items/{uuid}/borrow`
2. ✅ Backend updates database quantity
3. ✅ Backend fires `ItemUpdated` event
4. ✅ Event broadcasts via Reverb WebSocket
5. ✅ Frontend Echo receives event
6. ✅ Inventory.vue updates item quantity
7. ✅ **All users viewing Inventory page see update instantly**
8. ✅ **No page refresh required**

## 📝 Code Summary

### Backend Event Fire
```php
// ItemController::borrowItem()
event(new ItemUpdated($item));
```

### Frontend Event Listener
```javascript
// Inventory.vue
channel.listen('.ItemUpdated', (event) => {
  // Update item quantity reactively
  currentItem.quantity = updatedItem.quantity
});
```

Everything is properly configured! Just ensure Reverb is running and keys match.

