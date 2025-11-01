# 🔍 Debugging Real-Time Borrow Updates

## Quick Diagnostic Steps

### Step 1: Check Browser Console

Open Inventory page → Press F12 → Check Console

**Expected to see:**
```
🚀 Laravel Echo initialized
📡 Connecting to: localhost:8080
✅ Laravel Echo connected successfully
👂 Listening for ItemBorrowed events on inventory channel
🔍 DEBUG: Echo Status Check
  - window.Echo exists: true
  - Connection state: connected
  - Items count: X
```

**If you see errors:**
- `⚠️ Laravel Echo is not available` → Bootstrap.js not imported
- `❌ Connection failed` → Reverb server not running
- `Connection state: disconnected` → Check Reverb configuration

### Step 2: Check Reverb Server

**Open terminal and verify Reverb is running:**
```bash
cd backend-laravel
php artisan reverb:start
```

**Keep this terminal open!** The server must run continuously.

**Verify port is open (PowerShell):**
```powershell
Test-NetConnection -ComputerName localhost -Port 8080
```

Should show: `TcpTestSucceeded : True`

### Step 3: Check Backend Logs After Borrowing

**After borrowing an item, check logs:**
```powershell
Get-Content backend-laravel\storage\logs\laravel.log -Tail 50 | Select-String -Pattern "ItemBorrowed|Broadcasting"
```

**Expected logs:**
```
[INFO] ItemBorrowed event fired for item: X, Quantity: Y, Borrowed by: Z
[INFO] ItemBorrowed::shouldBroadcast() called. Driver: reverb
[INFO] ItemBorrowed event broadcasting on 'inventory' channel for item: X
[INFO] ItemBorrowed broadcast data prepared for item: X, New Quantity: Y
```

**If logs are missing:**
- Event might not be firing
- Check if `borrowItem` method is being called
- Check for errors in the try-catch block

### Step 4: Test Event Reception

**After borrowing, check browser console for:**
```
📦 ItemBorrowed event received: {item: {...}, borrowed_quantity: X, borrowed_by: "..."}
🔍 Event data details: {...}
🔍 Search results: {...}
```

**If event is received but item not found:**
- UUID might not match
- Item might be on different page
- Check console logs for UUID comparison

**If no event received:**
- Check Reverb server is running
- Check browser console for connection errors
- Check backend logs for event firing
- Verify `BROADCAST_DRIVER=reverb` in `.env`

### Step 5: Verify Configuration

**Check backend `.env`:**
```env
BROADCAST_DRIVER=reverb
REVERB_APP_KEY=your-key-here
REVERB_APP_SECRET=your-secret-here
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http
```

**Check frontend `.env` (or Vite config):**
```env
VITE_PUSHER_APP_KEY=your-key-here (same as REVERB_APP_KEY)
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
```

**Clear config cache:**
```bash
cd backend-laravel
php artisan config:clear
php artisan cache:clear
```

## Common Issues & Solutions

### Issue 1: Event Not Received

**Symptoms:** No `📦 ItemBorrowed event received` in console

**Solutions:**
1. Verify Reverb server is running
2. Check Echo connection state in console
3. Verify channel subscription:
   ```javascript
   // In browser console:
   console.log(window.Echo.channel('inventory'))
   ```
4. Check backend logs to confirm event is fired
5. Verify `BROADCAST_DRIVER=reverb` is set

### Issue 2: Event Received But Quantity Not Updating

**Symptoms:** Console shows event received but UI doesn't update

**Solutions:**
1. Check console for UUID match:
   - Event UUID vs items UUID
   - Make sure they match exactly
2. Check if item is on current page (not paginated/filtered)
3. Check Vue reactivity:
   - Try manually updating `items.value[0].quantity = 999`
   - If it doesn't update, reactivity issue
4. Force refresh: The code now auto-refreshes if item not found

### Issue 3: Connection Issues

**Symptoms:** Echo not connecting or disconnecting

**Solutions:**
1. Restart Reverb server
2. Check firewall isn't blocking port 8080
3. Verify `.env` keys match between frontend and backend
4. Check for CORS issues in console
5. Try different port if 8080 is blocked

### Issue 4: Event Fired But Not Broadcasting

**Symptoms:** Backend logs show event fired but no broadcast

**Solutions:**
1. Check `BROADCAST_DRIVER=reverb` is set
2. Clear config cache: `php artisan config:clear`
3. Verify Reverb is configured in `config/broadcasting.php`
4. Check if using queue (events might be queued)
   ```bash
   php artisan queue:work
   ```

## Testing Manually

### Test 1: Check Echo Connection

**In browser console on Inventory page:**
```javascript
// Check if Echo exists
console.log('Echo exists:', !!window.Echo)

// Check connection state
if (window.Echo?.connector?.pusher) {
  console.log('State:', window.Echo.connector.pusher.connection.state)
  console.log('Socket ID:', window.Echo.connector.pusher.connection.socket_id)
}

// Check channel
const channel = window.Echo?.channel('inventory')
console.log('Channel:', channel)
```

### Test 2: Listen to All Events

The code now listens to all events (`*`) for debugging. Check console for:
```
📡 Received event on inventory channel: ItemBorrowed {...}
```

### Test 3: Verify Item UUIDs

**In browser console:**
```javascript
// Get all item UUIDs
window.itemsUUIDs = items.value.map(i => ({uuid: i.uuid, quantity: i.quantity}))
console.table(window.itemsUUIDs)
```

Then compare with the UUID in the event when it arrives.

## Next Steps If Still Not Working

1. **Share browser console output** (F12 → Console)
2. **Share backend logs** after borrowing:
   ```powershell
   Get-Content backend-laravel\storage\logs\laravel.log -Tail 100
   ```
3. **Verify Reverb server output** (the terminal running `php artisan reverb:start`)
4. **Check network tab** in browser for WebSocket connections

## Expected Complete Flow

1. ✅ Mobile app calls `/api/v1/items/{uuid}/borrow`
2. ✅ Backend updates quantity in database
3. ✅ Backend fires `ItemBorrowed` event
4. ✅ Backend logs: "ItemBorrowed event fired..."
5. ✅ Reverb server receives broadcast
6. ✅ Browser Echo receives event
7. ✅ Browser console shows: "📦 ItemBorrowed event received"
8. ✅ Vue updates item quantity
9. ✅ UI updates automatically (no refresh)

If any step fails, check the logs/output for that step.

