# Debug Real-Time Updates - Step by Step

## Current Status

From the logs, I can see:
✅ Events ARE being dispatched: `Broadcasting ItemUpdated event for item: X`
✅ Events ARE being logged: `ItemUpdated event dispatched successfully`

But we need to verify:
1. Is Reverb server running?
2. Is Echo connected on frontend?
3. Are events actually being received?

## Step 1: Check Reverb Server

**In a terminal, run:**
```bash
cd backend-laravel
php artisan reverb:start
```

**You should see:**
```
INFO Starting server on 0.0.0.0:8080 (localhost).
```

**Keep this terminal open!** Reverb must run continuously.

## Step 2: Check Browser Console

1. **Open your web app** in browser
2. **Navigate to Inventory page**
3. **Open Developer Console** (F12)

**Look for these messages:**
- `✅ Laravel Echo connected successfully` (MUST see this!)
- `✅ Successfully subscribed to inventory channel`
- `🎧 Echo channel setup complete. Ready to receive events.`

**If you see:**
- `❌ Laravel Echo connection error` → Reverb not running or keys don't match
- `⚠️ Echo is not connected` → Connection failed

## Step 3: Test Real-Time Update

1. **Keep browser console open**
2. **Borrow an item from mobile app** (scan QR and borrow)
3. **Watch browser console immediately**

**You should see:**
```
📦 Item updated via Echo - Full event: {...}
📦 Event data structure: {...}
🔍 Looking for item with: {...}
✅ Updated item X in real-time. New quantity: Y
```

**If you DON'T see `📦 Item updated via Echo`**, then:
- Event isn't being received → Check Reverb server
- Echo isn't connected → Check connection status
- Channel isn't subscribed → Check subscription logs

## Step 4: Check Backend Logs

After borrowing, check `backend-laravel/storage/logs/laravel.log`:

**Should see:**
```
[INFO] Broadcasting ItemUpdated event for item: X
[INFO] ItemUpdated::shouldBroadcast() called. Driver: reverb
[INFO] ItemUpdated event broadcasting on 'inventory' channel
[INFO] ItemUpdated broadcast data prepared for item: X, Quantity: Y
```

**If you see warnings:**
- Driver is not 'reverb' → Run `php artisan config:clear`

## Step 5: Verify Keys Match

```powershell
# Backend key
(Get-Content backend-laravel\.env | Select-String "REVERB_APP_KEY").ToString()

# Frontend key (must match!)
(Get-Content frontend-vue\.env | Select-String "VITE_PUSHER_APP_KEY").ToString()
```

## Common Issues

### Issue: Events dispatched but not received
**Cause:** Reverb server not running or Echo not connected
**Fix:** Start Reverb and verify Echo connection in console

### Issue: Echo not connecting
**Cause:** Keys don't match or Reverb not running
**Fix:** Check keys match, restart Reverb, restart frontend server

### Issue: Events received but inventory not updating
**Cause:** Item matching logic not finding the item
**Fix:** Check console logs for item matching details

## What I Just Fixed

1. ✅ Changed `shouldBroadcast()` to always return `true` (Laravel will handle driver check)
2. ✅ Added better connection waiting logic (waits for Echo to connect)
3. ✅ Added channel subscription monitoring
4. ✅ Added detailed event logging to see full event structure

## Next Steps

1. **Start Reverb server** (if not running)
2. **Clear config cache:** `php artisan config:clear`
3. **Restart frontend** (if you changed .env)
4. **Test borrowing** from mobile app
5. **Watch browser console** for detailed logs

The enhanced logging will show exactly what's happening!

