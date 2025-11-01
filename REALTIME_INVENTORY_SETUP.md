# Real-Time Inventory Updates Setup Guide

## Overview
The system now uses Laravel Echo for real-time inventory updates. When an item is borrowed via the API (mobile app), all users viewing the Inventory page on the web application will see the updated quantity immediately without refreshing the page.

## What Was Implemented

### Backend
1. **Created `ItemUpdated` Event** (`app/Events/ItemUpdated.php`)
   - Broadcasts on the public `inventory` channel
   - Includes complete item data with all relationships

2. **Updated `borrowItem` Method** (`app/Http/Controllers/Api/V1/ItemController.php`)
   - Fires `ItemUpdated` event after successful borrow transaction
   - All connected clients receive the update instantly

3. **Broadcasting Configuration**
   - Added `routes/channels.php` for channel authorization
   - Updated `bootstrap/app.php` to include broadcasting routes

### Frontend
1. **Laravel Echo Bootstrap** (`frontend-vue/src/bootstrap.js`)
   - Initializes Echo with Pusher protocol
   - Configured for both Pusher.com and Laravel Reverb

2. **Inventory.vue Real-Time Listener**
   - Listens for `ItemUpdated` events on the `inventory` channel
   - Automatically updates item quantity in the UI when received
   - No page refresh required

## Configuration Required

### Option 1: Laravel Reverb (Recommended - Native Laravel Solution)

1. **Install Laravel Reverb**:
   ```bash
   cd backend-laravel
   composer require laravel/reverb
   php artisan reverb:install
   php artisan migrate
   ```

2. **Configure Environment Variables** (`.env`):
   ```env
   BROADCAST_DRIVER=reverb
   REVERB_APP_ID=your-app-id
   REVERB_APP_KEY=your-app-key
   REVERB_APP_SECRET=your-app-secret
   REVERB_HOST=localhost
   REVERB_PORT=8080
   REVERB_SCHEME=http
   ```

3. **Configure Frontend** (`frontend-vue/.env` or `frontend-vue/.env.local`):
   ```env
   VITE_PUSHER_APP_KEY=your-app-key
   VITE_PUSHER_HOST=localhost
   VITE_PUSHER_PORT=8080
   VITE_PUSHER_SCHEME=http
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start Reverb Server**:
   ```bash
   php artisan reverb:start
   ```

### Option 2: Pusher.com (Cloud Service)

1. **Install Pusher PHP SDK**:
   ```bash
   cd backend-laravel
   composer require pusher/pusher-php-server
   ```

2. **Configure Environment Variables** (`.env`):
   ```env
   BROADCAST_DRIVER=pusher
   PUSHER_APP_ID=your-app-id
   PUSHER_APP_KEY=your-app-key
   PUSHER_APP_SECRET=your-app-secret
   PUSHER_APP_CLUSTER=mt1
   ```

3. **Configure Frontend** (`frontend-vue/.env`):
   ```env
   VITE_PUSHER_APP_KEY=your-app-key
   VITE_PUSHER_APP_CLUSTER=mt1
   VITE_API_BASE_URL=http://localhost:8000
   ```

## How It Works

1. **Mobile App** borrows an item via API endpoint: `POST /api/items/{uuid}/borrow`
2. **Backend** processes the borrow, updates quantity, and fires `ItemUpdated` event
3. **Laravel** broadcasts the event to the `inventory` channel
4. **All Connected Clients** (web app users viewing Inventory page) receive the update instantly
5. **Frontend** automatically updates the item quantity in the UI without page refresh

## Testing

1. **Start Laravel Server**:
   ```bash
   cd backend-laravel
   php artisan serve
   ```

2. **Start Reverb Server** (if using Reverb):
   ```bash
   php artisan reverb:start
   ```

3. **Start Frontend Dev Server**:
   ```bash
   cd frontend-vue
   npm run dev
   ```

4. **Test Real-Time Updates**:
   - Open Inventory page in browser
   - Borrow an item via mobile app or API tool (Postman)
   - Watch the quantity update automatically on the web app

## Troubleshooting

### Echo Not Connecting
- **Check**: Is Reverb/Pusher server running?
- **Check**: Are environment variables correctly set?
- **Check**: Browser console for connection errors

### No Real-Time Updates
- **Check**: Browser console for Echo connection logs
- **Check**: Network tab for WebSocket connection
- **Check**: Backend logs for broadcast events

### Authentication Issues
- **Check**: Token is set in localStorage
- **Check**: Auth headers are configured in `bootstrap.js`

### Channel Subscription Failed
- **Check**: `routes/channels.php` authorization
- **Check**: Channel name matches (should be `inventory`)

## Benefits

✅ **Real-Time Updates**: No page refresh needed  
✅ **Better UX**: Users always see current inventory  
✅ **Reduced Server Load**: No polling required  
✅ **Instant Feedback**: Changes visible immediately  
✅ **Scalable**: Works with multiple concurrent users  

## Additional Notes

- The `inventory` channel is currently public (no auth required)
- To make it private, update `routes/channels.php` to use `PrivateChannel`
- You can extend this to broadcast on item updates, creates, and deletes
- Consider adding error handling and reconnection logic for production

