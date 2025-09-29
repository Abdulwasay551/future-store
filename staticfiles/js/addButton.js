document.addEventListener('DOMContentLoaded', function() {
    const headerInner = document.getElementById('header-inner');
    if (headerInner) {
        const firstChildDiv = headerInner.children[0];
        if (firstChildDiv) {
            const secondChildDiv = firstChildDiv.children[1];
            if (secondChildDiv) {
                const buttonsContainer = document.createElement('div');
                buttonsContainer.className = 'flex items-center gap-2';
                buttonsContainer.style.display = 'flex';

                // First fetch the active config
                fetch('/get/active-config/')
                    .then(response => response.json())
                    .then(data => {
                        const configUrl = data.url;
                        buttonsContainer.innerHTML = `
                            <!-- Notification Bell -->
                            <div class="relative flex px-4" x-data="{ notificationsOpen: false }">
                                <button @click="notificationsOpen = !notificationsOpen" class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-100 
                                            focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-600 
                                            transition-colors duration-200 relative">
                                    <svg class="h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                                    </svg>
                                    <span id="notification-badge"
                                        style="top:-1%; right:-1%; border-radius:45%; width:50%; height:50%;font-size:60%;"
                                        class="hidden absolute  bg-red-500 text-white   flex items-center justify-center">
                                        0
                                    </span>
                                </button>

                                <!-- Notification Dropdown -->
                                <div x-show="notificationsOpen" x-transition:enter="transition ease-out duration-200"
                                    x-transition:enter-start="opacity-0 scale-95"
                                    x-transition:enter-end="opacity-100 scale-100"
                                    x-transition:leave="transition ease-in duration-150"
                                    x-transition:leave-start="opacity-100 scale-100"
                                    x-transition:leave-end="opacity-0 scale-95"
                                    class="absolute right-0 w-80 bg-white dark:bg-dark-200 rounded shadow-lg py-1 ring-1 ring-black ring-opacity-5"
                                    style="z-index: 50; margin-top:20px;">
                                    <div id="notification-list" class="max-h-96 px-1">
                                        <!-- Notifications will be inserted here -->
                                        <div class="text-center text-gray-500 dark:text-gray-400 py-4">
                                            Loading notifications...
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Settings Button -->
                            <div class="relative flex">
                                <a href="${configUrl}" class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-100 
                                            focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-600 
                                            transition-colors duration-200">
                                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    </svg>
                                </a>
                            </div>
                        `;
                        secondChildDiv.appendChild(buttonsContainer);
                    })
                    .catch(error => {
                        console.error('Error fetching config:', error);
                        // Fallback to default config URL if fetch fails
                        buttonsContainer.innerHTML = `
                            <!-- Notification Bell -->
                            <div class="relative flex px-4" x-data="{ notificationsOpen: false }">
                                <button @click="notificationsOpen = !notificationsOpen" class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-100 
                                            focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-600 
                                            transition-colors duration-200 relative">
                                    <svg class="h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                                    </svg>
                                    <span id="notification-badge"
                                        style="top:-1%; right:-1%; border-radius:45%; width:50%; height:50%;font-size:60%;"
                                        class="hidden absolute  bg-red-500 text-white   flex items-center justify-center">
                                        0
                                    </span>
                                </button>

                                <!-- Notification Dropdown -->
                                <div x-show="notificationsOpen" x-transition:enter="transition ease-out duration-200"
                                    x-transition:enter-start="opacity-0 scale-95"
                                    x-transition:enter-end="opacity-100 scale-100"
                                    x-transition:leave="transition ease-in duration-150"
                                    x-transition:leave-start="opacity-100 scale-100"
                                    x-transition:leave-end="opacity-0 scale-95"
                                    class="absolute right-0 w-80 bg-white dark:bg-dark-200 rounded shadow-lg py-1 ring-1 ring-black ring-opacity-5"
                                    style="z-index: 50; margin-top:20px;">
                                    <div id="notification-list" class="max-h-96 px-1">
                                        <!-- Notifications will be inserted here -->
                                        <div class="text-center text-gray-500 dark:text-gray-400 py-4">
                                            Loading notifications...
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Settings Button -->
                            <div class="relative flex px-4">
                                <a href="/admin/salary/config/" class="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-dark-100 
                                            focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-600 
                                            transition-colors duration-200">
                                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    </svg>
                                </a>
                            </div>
                        `;
                        secondChildDiv.appendChild(buttonsContainer);
                    });
            }
        }
    }
});
