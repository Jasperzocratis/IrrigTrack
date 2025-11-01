# Quick Start: Real-Time Inventory Updates

## The Problem
Real-time updates aren't working because **broadcasting isn't configured**. The backend is firing events, but there's no broadcasting server to deliver them.

## Quick Fix: Use Log Driver (For Testing)

If you just want to test that events are firing, you can use the log driver:

### Step 1: Update `.env` file in `backend-laravel`
```env
BROADCAST_DRIVER=log
```

This will log broadcast events to `storage/logs/laravel.log` instead of broadcasting them.

## Proper Fix: Set Up Laravel Reverb (Recommended)

### Step 1: Install Reverb
```bash
cd backend-laravel
composer require laravel/reverb
php artisan reverb:install
```

### Step 2: Generate Reverb Credentials
```bash
php artisan reverb:install
```

This will add to your `.env`:
```
REVERB_APP_ID=your-app-id
REVERB_APP_KEY=your-app-key
REVERB_APP_SECRET=your-app-secret
REVERB_HOST=localhost
REVERB_PORT=8080
```

### Step 3: Update `.env` in `backend-laravel`
```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=your-app-id
REVERB_APP_KEY=your-app-key
REVERB_APP_SECRET=your-app-secret
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http
```

### Step 4: Update `.env` in `frontend-vue` (or create it)
```env
VITE_PUSHER_APP_KEY=your-app-key (same as REVERB_APP_KEY)
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
VITE_API_BASE_URL=http://localhost:8000
```

### Step 5: Start Reverb Server
```bash
cd backend-laravel
php artisan reverb:start
```

**Keep this terminal open!** Reverb needs to run continuously.

### Step 6: Test
1. Open browser console (F12)
2. Look for: `✅ Laravel Echo connected successfully`
3. Borrow an item from mobile app
4. Watch console for: `📦 Item updated via Echo:`
5. Inventory should update automatically!

## Alternative: Use Pusher.com (Cloud Service)

### Step 1: Create Pusher Account
Go to https://pusher.com and create a free account

### Step 2: Create App and Get Credentials
- App ID
- Key
- Secret
- Cluster

### Step 3: Update `.env` in `backend-laravel`
```env
BROADCAST_DRIVER=pusher
PUSHER_APP_ID=your-app-id
PUSHER_APP_KEY=your-app-key
PUSHER_APP_SECRET=your-app-secret
PUSHER_APP_CLUSTER=mt1
```

### Step 4: Update `.env` in `frontend-vue`
```env
VITE_PUSHER_APP_KEY=your-app-key
VITE_PUSHER_APP_CLUSTER=mt1
VITE_API_BASE_URL=http://localhost:8000
```

### Step 5: Install Pusher PHP SDK
```bash
cd backend-laravel
composer require pusher/pusher-php-server
```

## Debugging

### Check if Echo is Connected
Open browser console and look for:
- ✅ `Laravel Echo connected successfully` = Working!
- ❌ `Laravel Echo connection error` = Not configured
- ⚠️ `Echo is not connected` = Server not running

### Check if Events are Firing
1. Check Laravel logs: `storage/logs/laravel.log`
2. Look for: `Failed to broadcast ItemUpdated event`
3. If you see warnings, broadcasting isn't configured

### Check Browser Console
After borrowing an item, you should see:
- `📦 Item updated via Echo:` = Event received!
- `Updated item X in real-time. New quantity: Y` = Working!

## Current Status

The code is ready! You just need to:
1. ✅ Install Reverb (or configure Pusher)
2. ✅ Start the broadcasting server
3. ✅ Test it

The frontend will now show detailed connection status in the console to help you debug.

