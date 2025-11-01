# Quick Fix: Echo Connection Issues

## Problem: "Echo is not connected. State: disconnected"

This means Echo can't connect to Reverb. Here's how to fix it:

## Step 1: Verify Reverb Keys Match

### Backend `.env` file (`backend-laravel/.env`):
```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=your-app-id-here
REVERB_APP_KEY=your-app-key-here
REVERB_APP_SECRET=your-app-secret-here
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http
```

### Frontend `.env` file (`frontend-vue/.env`):
Create this file if it doesn't exist!

```env
VITE_PUSHER_APP_KEY=your-app-key-here
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
VITE_API_BASE_URL=http://localhost:8000
```

**CRITICAL:** `VITE_PUSHER_APP_KEY` must exactly match `REVERB_APP_KEY`!

## Step 2: Check if Keys Match

Run this in PowerShell to compare:
```powershell
# Get backend key
$backendKey = (Get-Content backend-laravel\.env | Select-String "REVERB_APP_KEY").ToString()
Write-Host "Backend Key: $backendKey"

# Get frontend key (if .env exists)
if (Test-Path frontend-vue\.env) {
    $frontendKey = (Get-Content frontend-vue\.env | Select-String "VITE_PUSHER_APP_KEY").ToString()
    Write-Host "Frontend Key: $frontendKey"
} else {
    Write-Host "Frontend .env not found!"
}
```

## Step 3: Copy Key from Backend to Frontend

1. Open `backend-laravel/.env`
2. Copy the value of `REVERB_APP_KEY=...`
3. Create or edit `frontend-vue/.env`
4. Add: `VITE_PUSHER_APP_KEY=<paste-the-same-value>`

Example:
```
Backend:  REVERB_APP_KEY=abc123xyz
Frontend: VITE_PUSHER_APP_KEY=abc123xyz  ← Must be identical!
```

## Step 4: Restart Everything

1. **Stop Reverb server** (Ctrl+C in the Reverb terminal)
2. **Stop frontend dev server** (Ctrl+C in frontend terminal)
3. **Clear Laravel config cache:**
   ```bash
   cd backend-laravel
   php artisan config:clear
   ```
4. **Start Reverb:**
   ```bash
   php artisan reverb:start
   ```
   (Keep this terminal open - you should see "INFO Starting server on 0.0.0.0:8080")
5. **Start frontend:**
   ```bash
   cd frontend-vue
   npm run dev
   ```

## Step 5: Check Browser Console

Open your web app and check console (F12). You should see:

✅ **Success:**
- `🚀 Laravel Echo initialized`
- `📡 Connecting to: localhost:8080`
- `🔄 Echo connection state changed: connecting -> connected`
- `✅ Laravel Echo connected successfully`

❌ **If still failing:**
- `❌ Laravel Echo connection error:`
- Check the error message for clues

## Common Issues:

### Issue 1: "Invalid key"
**Solution:** Keys don't match - recheck Step 3

### Issue 2: "Connection refused"
**Solution:** Reverb isn't running - start it with `php artisan reverb:start`

### Issue 3: "WebSocket connection failed"
**Solution:** 
- Check if port 8080 is blocked
- Try changing port in both `.env` files to `8081`
- Restart Reverb and frontend

### Issue 4: CORS errors
**Solution:** Add to `backend-laravel/config/reverb.php`:
```php
'allowed_origins' => ['http://localhost:5174', '*'],
```

## Quick Test:

After fixing keys and restarting, borrow an item from mobile app. You should see:
- Browser console: `📦 Item updated via Echo:`
- Inventory updates automatically!

