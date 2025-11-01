# 🔍 Complete Diagnostic Guide - Real-Time Updates Not Working

## Step 1: Check What You See in Browser Console

**Open Inventory page → Press F12 → Check Console**

### ✅ Good Signs (Working):
```
🚀 Laravel Echo initialized
📡 Connecting to: localhost:8080
✅ Laravel Echo connected successfully
🔄 Echo connection state changed: connecting -> connected
👂 Listening on channel: inventory
✅ Successfully subscribed to inventory channel
🎧 Echo channel setup complete. Ready to receive events.
```

### ❌ Bad Signs (Not Working):
```
❌ Laravel Echo connection error
⚠️ Laravel Echo disconnected
⚠️ Echo is not connected. State: disconnected
```

**If you see errors → Go to Step 2**

## Step 2: Check Reverb Server Status

### Check if Reverb is Running

**Open a terminal and run:**
```bash
cd backend-laravel
php artisan reverb:start
```

**Expected output:**
```
INFO Starting server on 0.0.0.0:8080 (localhost).
```

**If you get an error:**
- Port 8080 might be in use
- Reverb might not be installed

**Keep this terminal open!** Reverb must run continuously.

### Check if Port 8080 is Open

**In PowerShell:**
```powershell
Test-NetConnection -ComputerName localhost -Port 8080
```

**Should show:** `TcpTestSucceeded : True`

## Step 3: Test Broadcasting Manually

### Option A: Use Test Endpoint (Easiest)

**I've created a test endpoint. Check your browser console, then run:**

```bash
# In another terminal
curl http://localhost:8000/test-broadcast
```

**Or open in browser:**
```
http://localhost:8000/test-broadcast
```

**Expected response:**
```json
{
  "success": true,
  "message": "ItemUpdated event fired successfully",
  "broadcast_driver": "reverb"
}
```

**If you see `"broadcast_driver": null` → Config not loaded correctly**

### Option B: Check Backend Logs

**After borrowing from mobile app, check:**
```bash
Get-Content backend-laravel\storage\logs\laravel.log -Tail 30 | Select-String -Pattern "ItemUpdated|Broadcasting"
```

**Should see:**
```
[INFO] Broadcasting ItemUpdated event for item: X
[INFO] ItemUpdated::shouldBroadcast() called. Driver: reverb
[INFO] ItemUpdated event broadcasting on 'inventory' channel
```

**If you see `Driver: null` or `Driver: log` → Config issue**

## Step 4: Verify Configuration

### Backend `.env` Check

**Open `backend-laravel/.env` and verify:**

```env
BROADCAST_DRIVER=reverb
REVERB_APP_KEY=pjhxufuhuix3xhhln3pk
REVERB_HOST=localhost
REVERB_PORT=8080
```

**Important:** Should be `BROADCAST_DRIVER` (not `BROADCAST_CONNECTION`)

### Frontend `.env` Check

**Open `frontend-vue/.env` and verify:**

```env
VITE_PUSHER_APP_KEY=pjhxufuhuix3xhhln3pk
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
```

**Critical:** `VITE_PUSHER_APP_KEY` MUST match `REVERB_APP_KEY` exactly!

### Clear All Caches

```bash
cd backend-laravel
php artisan config:clear
php artisan cache:clear
php artisan route:clear
```

**Then restart:**
1. Reverb server (stop with Ctrl+C, then restart)
2. Frontend dev server (stop with Ctrl+C, then restart)
3. Laravel server if running (stop with Ctrl+C, then restart)

## Step 5: Test the Complete Flow

### 1. Start Reverb
```bash
cd backend-laravel
php artisan reverb:start
```
**Keep terminal open!**

### 2. Open Web App
- Open Inventory page
- Open browser console (F12)
- Verify you see "✅ Laravel Echo connected successfully"

### 3. Test Broadcast
**Option A: Use test endpoint**
```
http://localhost:8000/test-broadcast
```

**Option B: Borrow from mobile app**
- Scan QR code
- Borrow item
- Watch browser console immediately

### 4. Check Results

**Browser console should show:**
```
📦 Item updated via Echo - Full event: {...}
🔍 Looking for item with: {...}
✅ Updated item X in real-time. New quantity: Y
```

**If you see nothing:**
- Event isn't being received
- Check Reverb is running
- Check Echo is connected
- Check keys match

## Step 6: Common Issues & Fixes

### Issue 1: "broadcast_driver": null

**Problem:** Laravel isn't reading `.env`

**Fix:**
1. Check `.env` file has `BROADCAST_DRIVER=reverb` (no spaces!)
2. Run `php artisan config:clear`
3. Restart Laravel server

### Issue 2: Echo Not Connecting

**Problem:** Can't connect to Reverb

**Fix:**
1. Verify Reverb is running (`php artisan reverb:start`)
2. Check port 8080 is not blocked
3. Verify `VITE_PUSHER_APP_KEY` matches `REVERB_APP_KEY`
4. Restart frontend dev server after changing `.env`

### Issue 3: Events Fired But Not Received

**Problem:** Backend fires events, but frontend doesn't receive them

**Fix:**
1. Check Echo is connected (see Step 1)
2. Check channel is subscribed (should see "subscribed to inventory channel")
3. Verify Reverb server is still running
4. Check browser console for WebSocket errors

### Issue 4: Events Received But UI Not Updating

**Problem:** Console shows event received, but quantity doesn't change

**Fix:**
1. Check console logs for item matching
2. Verify item ID/UUID in event matches item in list
3. Check if item is filtered out or on different page
4. List should auto-refresh if item not found

## Step 7: Quick Test Script

**Run this PowerShell script to check everything:**

```powershell
# Check backend .env
Write-Host "=== Backend Config ===" -ForegroundColor Cyan
Get-Content backend-laravel\.env | Select-String -Pattern "BROADCAST|REVERB" | ForEach-Object { Write-Host $_ }

# Check frontend .env
Write-Host "`n=== Frontend Config ===" -ForegroundColor Cyan
if (Test-Path frontend-vue\.env) {
    Get-Content frontend-vue\.env | Select-String -Pattern "PUSHER" | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "frontend-vue/.env NOT FOUND!" -ForegroundColor Red
}

# Check if port is open
Write-Host "`n=== Port 8080 Check ===" -ForegroundColor Cyan
$port = Test-NetConnection -ComputerName localhost -Port 8080 -InformationLevel Quiet
if ($port) {
    Write-Host "Port 8080 is OPEN" -ForegroundColor Green
} else {
    Write-Host "Port 8080 is CLOSED - Reverb not running!" -ForegroundColor Red
}

# Check latest logs
Write-Host "`n=== Latest Broadcast Logs ===" -ForegroundColor Cyan
Get-Content backend-laravel\storage\logs\laravel.log -Tail 20 | Select-String -Pattern "ItemUpdated|Broadcasting" | ForEach-Object { Write-Host $_ }
```

## What to Report

If still not working, please provide:

1. **Browser Console Output** (screenshot or copy)
   - Connection status
   - Any errors
   - Event received messages (if any)

2. **Backend Logs** (last 20 lines)
   ```bash
   Get-Content backend-laravel\storage\logs\laravel.log -Tail 20
   ```

3. **Test Endpoint Response**
   ```
   http://localhost:8000/test-broadcast
   ```

4. **Reverb Server Status**
   - Is it running?
   - What port?

5. **Configuration**
   - `BROADCAST_DRIVER` value
   - `REVERB_APP_KEY` value (first 10 chars)
   - `VITE_PUSHER_APP_KEY` value (first 10 chars)

This will help identify the exact issue!

