// Fetch notifications
function fetchNotifications() {
    fetch('/api/notifications/')  // Update this URL if needed
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notification-badge');
            const list = document.getElementById('notification-list');

            if (data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }

            if (data.notifications && data.notifications.length > 0) {
                list.innerHTML = data.notifications.map(notification => `
                    <a href="${notification.link}" 
                       onclick="markNotificationRead(${notification.id})"
                       class="block px-4 py-3 hover:bg-gray-100  hover:bg-base-100  dark:hover:bg-dark-300 rounded-lg mb-1">
                        <p class="font-medium text-gray-900 text-base-900 dark:text-gray-100">
                            ${notification.title}
                        </p>
                        <p class="text-sm text-gray-500 dark:text-gray-400">
                            ${notification.message}
                        </p>
                        <p class="text-xs text-gray-400 mt-1">
                            ${notification.created_at}
                        </p>
                    </a>
                `).join('');
            } else {
                list.innerHTML = `
                    <div class="text-center text-gray-500 dark:text-gray-400 py-4">
                        No new notifications
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error fetching notifications:', error);
            document.getElementById('notification-list').innerHTML = `
                <div class="text-center text-red-500 dark:text-red-400 py-4">
                    Error loading notifications
                </div>
            `;
        });
}

function markNotificationRead(id) {
    fetch(`/api/notifications/${id}/read/`);
}

if (typeof checkElement === 'undefined') { 
    let checkElement = setInterval(() => {
        let l = document.getElementById('notification-badge');
        if (l) {
            clearInterval(checkElement); // Stop checking once found
            fetchNotifications(); // Execute function when element is ready
        }
    }, 1000);
}
// Poll for new notifications every 30 seconds

setInterval(fetchNotifications, 30000);