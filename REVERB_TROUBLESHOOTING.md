# Reverb Server Troubleshooting

## Server Shows "Starting" But Never Completes

If you see `INFO Starting server on 0.0.0.0:8080 (localhost).` and it stays there, this usually means:

### ✅ **This is Normal!**
The server IS running! The message "Starting" is misleading - it actually means "Server is running and ready". Reverb keeps running until you stop it (Ctrl+C).

### How to Verify It's Working:

1. **Check if server is listening on port 8080:**
   ```powershell
   netstat -an | findstr :8080
   ```
   You should see the port in LISTENING state.

2. **Test the connection from browser:**
   - Open browser console (F12)
   - You should see connection messages:
     - `🚀 Laravel Echo initialized`
     - `📡 Connecting to: localhost:8080`
     - `✅ Laravel Echo connected successfully`

3. **Check Reverb logs:**
   - The Reverb terminal should show connection attempts
   - When browser connects, you'll see activity

### Common Issues:

#### Issue 1: Echo Not Connecting
**Symptoms:** Browser console shows connection errors

**Fix:**
1. Make sure `.env` in `backend-laravel` has:
   ```env
   BROADCAST_DRIVER=reverb
   REVERB_APP_KEY=<your-key>
   REVERB_APP_SECRET=<your-secret>
   REVERB_HOST=localhost
   REVERB_PORT=8080
   ```

2. Make sure `frontend-vue/.env` (or environment variables) has:
   ```env
   VITE_PUSHER_APP_KEY=<same-as-REVERB_APP_KEY>
   VITE_PUSHER_HOST=localhost
   VITE_PUSHER_PORT=8080
   ```

3. Restart Reverb server after changing .env:
   ```bash
   # Stop Reverb (Ctrl+C)
   php artisan reverb:start
   ```

#### Issue 2: Port Already in Use
**Symptoms:** Error about port 8080 being in use

**Fix:**
1. Change port in `.env`:
   ```env
   REVERB_PORT=8081
   ```

2. Update frontend `.env`:
   ```env
   VITE_PUSHER_PORT=8081
   ```

3. Restart Reverb

#### Issue 3: CORS Errors
**Symptoms:** Browser shows CORS errors in console

**Fix:**
1. Add frontend URL to `config/cors.php`:
   ```php
   'allowed_origins' => ['http://localhost:5174', 'http://localhost:8080'],
   ```

2. Clear config cache:
   ```bash
   php artisan config:clear
   ```

### Testing Real-Time Updates:

1. **Start all services:**
   ```bash
   # Terminal 1: Laravel
   cd backend-laravel
   php artisan serve

   # Terminal 2: Reverb (keep running)
   php artisan reverb:start

   # Terminal 3: Frontend
   cd frontend-vue
   npm run dev
   ```

2. **Open browser:**
   - Go to Inventory page
   - Open Console (F12)
   - Look for: `✅ Laravel Echo connected successfully`

3. **Test from mobile app:**
   - Borrow an item
   - Check browser console for: `📦 Item updated via Echo:`
   - Inventory should update automatically!

### Expected Console Output:

**When Reverb starts:**
```
INFO  Starting server on 0.0.0.0:8080 (localhost).
```
(This is OK - it means it's running!)

**When browser connects:**
You'll see connection logs in Reverb terminal.

**When event is broadcast:**
You'll see the event being sent in Reverb terminal.

### Quick Diagnostic:

Run this in browser console:
```javascript
// Check Echo status
console.log('Echo:', window.Echo)
console.log('Connection:', window.Echo?.connector?.pusher?.connection?.state)
```

Should show: `"connected"` if working!

