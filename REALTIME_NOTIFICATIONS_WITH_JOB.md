# Real-Time Notifications: Background Job + Laravel Echo Integration

## Overview

This document explains how the **CheckLowStockJob** background job works together with **Laravel Echo** and **Reverb/Pusher** to provide real-time notification updates.

## Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Background Job (CheckLowStockJob)                           │
│    - Runs every 30 seconds (or on schedule)                    │
│    - Checks for low stock items                                 │
│    - Creates notifications in database                         │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. NotificationCreated Event                                    │
│    - Implements ShouldBroadcast                                 │
│    - Broadcasts on 'notifications' channel                      │
│    - Includes notification data + unread_count                 │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Laravel Reverb/Pusher                                        │
│    - Receives broadcast event                                   │
│    - Sends to all connected clients via WebSocket              │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Frontend (Laravel Echo)                                      │
│    - Listens on 'notifications' channel                         │
│    - Receives .NotificationCreated events                       │
│    - Updates notification list in real-time                     │
│    - Updates badge count instantly                             │
└─────────────────────────────────────────────────────────────────┘
```

## How It Works

### Backend (Laravel)

#### 1. Background Job Setup

**File:** `backend-laravel/app/Jobs/CheckLowStockJob.php`

- Implements `ShouldQueue` but uses `sync` connection for immediate execution
- Runs on schedule (every 30 seconds) or manually
- Checks for low stock items (quantity < 50)
- Creates notifications in database

**Key Code:**
```php
// Job creates notification
$notification = Notification::create([
    'item_id' => $item->id,
    'message' => $message,
]);

// Refresh to load relationships
$notification->refresh();
$notification->load('item');

// Fire event for real-time broadcasting
event(new NotificationCreated($notification));
```

#### 2. Event Broadcasting

**File:** `backend-laravel/app/Events/NotificationCreated.php`

- Implements `ShouldBroadcast` interface
- Broadcasts on public `notifications` channel
- Includes notification data via `NotificationResource`
- Includes `unread_count` for badge updates

**Broadcast Data:**
```php
[
    'notification' => [
        'id' => ...,
        'message' => ...,
        'item' => ...,
        // ... full notification data
    ],
    'unread_count' => 5  // Current unread count
]
```

#### 3. Scheduled Execution

**File:** `backend-laravel/routes/console.php`

```php
Schedule::job(new CheckLowStockJob)->everyThirtySeconds();
```

**To run scheduler:**
```bash
php artisan schedule:work
```

### Frontend (Vue.js)

#### 1. Echo Listener Setup

**File:** `frontend-vue/src/composables/useNotifications.js`

- Sets up listener in `setupRealtimeListener()`
- Listens on `notifications` channel
- Listens for `.NotificationCreated` events

**Key Code:**
```javascript
const channel = window.Echo.channel('notifications')

channel.listen('.NotificationCreated', (data) => {
    // Add notification to list
    notifications.value.unshift(newNotification)
    
    // Update unread count
    unreadCount.value = data.unread_count
})
```

#### 2. Layout Integration

**File:** `frontend-vue/src/layouts/DefaultLayout.vue`

- Calls `setupRealtimeListener()` on mount
- Badge automatically updates when events received
- **No polling needed** - updates happen instantly

## Configuration

### Backend `.env`

```env
BROADCAST_DRIVER=reverb
REVERB_APP_ID=your-app-id
REVERB_APP_KEY=your-app-key
REVERB_APP_SECRET=your-app-secret
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http
```

### Frontend `.env`

```env
VITE_PUSHER_APP_KEY=your-app-key (same as REVERB_APP_KEY)
VITE_PUSHER_HOST=localhost
VITE_PUSHER_PORT=8080
```

## Running the System

### 1. Start Laravel Scheduler

```bash
cd backend-laravel
php artisan schedule:work
```

**Note:** This keeps running and executes scheduled jobs (CheckLowStockJob every 30 seconds)

### 2. Start Reverb Server

```bash
cd backend-laravel
php artisan reverb:start
```

**Note:** Keep this terminal open - Reverb must run continuously

### 3. Start Frontend Dev Server

```bash
cd frontend-vue
npm run dev
```

### 4. Verify Setup

**Check browser console for:**
```
🚀 Laravel Echo initialized
✅ Laravel Echo connected successfully
👂 Listening for NotificationCreated events on notifications channel
```

## Testing

### Test 1: Manual Job Execution

```bash
cd backend-laravel
php artisan tinker
```

```php
$job = new App\Jobs\CheckLowStockJob();
$job->handle();
```

**Expected:**
- Notification created in database
- Event broadcasted via Reverb
- Frontend receives event and updates badge

### Test 2: Scheduled Job

1. Start scheduler: `php artisan schedule:work`
2. Wait 30 seconds
3. Check logs: `storage/logs/laravel.log`
4. Check browser - badge should update automatically

### Test 3: Check Logs

**Backend logs should show:**
```
[INFO] Created low stock notification for item: ...
[INFO] Firing NotificationCreated event for notification: X
[INFO] Broadcast driver: reverb
[INFO] NotificationCreated::shouldBroadcast() called. Driver: reverb
[INFO] NotificationCreated event broadcasting on 'notifications' channel
[INFO] ✅ NotificationCreated event successfully fired and broadcasted
```

**Browser console should show:**
```
🔔 NotificationCreated event received: {...}
✅ New notification added: Low stock alert: ...
   Unread count: X
```

## Troubleshooting

### Issue 1: Events Not Broadcasting

**Symptoms:** Job creates notifications but frontend doesn't receive them

**Solutions:**
1. Check `BROADCAST_DRIVER=reverb` in `.env`
2. Verify Reverb server is running
3. Check backend logs for broadcast errors
4. Clear config cache: `php artisan config:clear`

### Issue 2: Job Not Running

**Symptoms:** No notifications being created

**Solutions:**
1. Start scheduler: `php artisan schedule:work`
2. Check schedule: `php artisan schedule:list`
3. Manually test: `php artisan tinker` → `$job = new CheckLowStockJob(); $job->handle();`

### Issue 3: Echo Not Connecting

**Symptoms:** Browser console shows connection errors

**Solutions:**
1. Check `bootstrap.js` is imported in `main.js`
2. Verify Reverb is running
3. Check `.env` keys match between frontend and backend
4. Restart dev server after `.env` changes

## Benefits

✅ **No Polling** - Real-time updates, no 30-second API calls
✅ **Instant Updates** - Badge updates immediately when notification created
✅ **Efficient** - Only sends data when notifications are actually created
✅ **Scalable** - Works with multiple connected clients
✅ **Reliable** - Job and broadcasting work independently (job doesn't fail if broadcast fails)

## Best Practices

1. **Always refresh notification** before broadcasting to ensure relationships are loaded
2. **Log broadcasting** for debugging purposes
3. **Handle errors gracefully** - don't fail job if broadcast fails
4. **Test with scheduler running** to simulate real-world usage
5. **Monitor logs** for both job execution and broadcasting

## Summary

The background job (CheckLowStockJob) and Laravel Echo work together seamlessly:

- **Job** creates notifications in the database
- **Event** broadcasts the notification via Reverb
- **Echo** receives the broadcast and updates the UI
- **Badge** updates instantly without polling

This creates a real-time notification system where users see updates immediately when low stock notifications are created by the scheduled job.

