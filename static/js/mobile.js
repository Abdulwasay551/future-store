// Mobile Corner - Mobile App JavaScript
// This file enhances your Django app with mobile-specific features

(function() {
    'use strict';
    
    // Mobile detection
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const isAndroid = /Android/.test(navigator.userAgent);
    
    // Mobile app initialization
    function initMobileApp() {
        if (isMobile) {
            document.body.classList.add('mobile-device');
            
            // Add mobile-specific classes
            if (isIOS) {
                document.body.classList.add('ios-device');
            } else if (isAndroid) {
                document.body.classList.add('android-device');
            }
            
            // Initialize mobile features
            initMobileNavigation();
            initTouchGestures();
            initMobileOptimizations();
            initPullToRefresh();
            initMobileNotifications();
        }
    }
    
    // Mobile navigation
    function initMobileNavigation() {
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        const mobileMenu = document.querySelector('.mobile-menu');
        const nav = document.querySelector('nav, .navbar');
        
        if (menuToggle && mobileMenu) {
            menuToggle.addEventListener('click', function() {
                mobileMenu.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', function(e) {
                if (!mobileMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                    mobileMenu.classList.remove('active');
                    menuToggle.classList.remove('active');
                }
            });
            
            // Close menu when clicking on a link
            const menuLinks = mobileMenu.querySelectorAll('a');
            menuLinks.forEach(link => {
                link.addEventListener('click', function() {
                    mobileMenu.classList.remove('active');
                    menuToggle.classList.remove('active');
                });
            });
        }
        
        // Hide/show navigation on scroll
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (nav) {
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    // Scrolling down
                    nav.style.transform = 'translateY(-100%)';
                } else {
                    // Scrolling up
                    nav.style.transform = 'translateY(0)';
                }
            }
            
            lastScrollTop = scrollTop;
        });
    }
    
    // Touch gestures
    function initTouchGestures() {
        let startX, startY, endX, endY;
        
        document.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', function(e) {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const diffX = startX - endX;
            const diffY = startY - endY;
            
            // Swipe left/right detection
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe left
                    handleSwipeLeft();
                } else {
                    // Swipe right
                    handleSwipeRight();
                }
            }
            
            // Swipe up/down detection
            if (Math.abs(diffY) > Math.abs(diffX) && Math.abs(diffY) > 50) {
                if (diffY > 0) {
                    // Swipe up
                    handleSwipeUp();
                } else {
                    // Swipe down
                    handleSwipeDown();
                }
            }
        });
    }
    
    // Swipe handlers
    function handleSwipeLeft() {
        // Navigate forward or next item
        const nextButton = document.querySelector('.next, .carousel-next');
        if (nextButton) {
            nextButton.click();
        }
    }
    
    function handleSwipeRight() {
        // Navigate back or previous item
        const prevButton = document.querySelector('.prev, .carousel-prev');
        if (prevButton) {
            prevButton.click();
        } else if (window.history.length > 1) {
            window.history.back();
        }
    }
    
    function handleSwipeUp() {
        // Scroll to top or expand content
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    function handleSwipeDown() {
        // Refresh or collapse content
        if (window.scrollY === 0) {
            location.reload();
        }
    }
    
    // Mobile optimizations
    function initMobileOptimizations() {
        // Optimize images for mobile
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.complete) {
                img.addEventListener('load', function() {
                    this.classList.add('loaded');
                });
            } else {
                img.classList.add('loaded');
            }
        });
        
        // Optimize forms for mobile
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            // Prevent zoom on iOS
            if (isIOS) {
                input.style.fontSize = '16px';
            }
            
            // Add mobile-friendly focus states
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        });
        
        // Optimize buttons for touch
        const buttons = document.querySelectorAll('button, .btn, a[role="button"]');
        buttons.forEach(button => {
            button.addEventListener('touchstart', function() {
                this.classList.add('touch-active');
            });
            
            button.addEventListener('touchend', function() {
                this.classList.remove('touch-active');
            });
        });
    }
    
    // Pull to refresh
    function initPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const threshold = 80;
        
        const pullIndicator = document.createElement('div');
        pullIndicator.className = 'pull-to-refresh';
        pullIndicator.innerHTML = 'Pull to refresh';
        pullIndicator.style.display = 'none';
        document.body.insertBefore(pullIndicator, document.body.firstChild);
        
        document.addEventListener('touchstart', function(e) {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
            }
        });
        
        document.addEventListener('touchmove', function(e) {
            if (window.scrollY === 0 && startY > 0) {
                currentY = e.touches[0].clientY;
                pullDistance = currentY - startY;
                
                if (pullDistance > 0) {
                    e.preventDefault();
                    pullIndicator.style.display = 'block';
                    pullIndicator.style.transform = `translateY(${Math.min(pullDistance, threshold)}px)`;
                    
                    if (pullDistance > threshold) {
                        pullIndicator.innerHTML = 'Release to refresh';
                        pullIndicator.classList.add('ready');
                    } else {
                        pullIndicator.innerHTML = 'Pull to refresh';
                        pullIndicator.classList.remove('ready');
                    }
                }
            }
        });
        
        document.addEventListener('touchend', function() {
            if (pullDistance > threshold) {
                // Trigger refresh
                location.reload();
            }
            
            // Reset
            startY = 0;
            pullDistance = 0;
            pullIndicator.style.display = 'none';
            pullIndicator.style.transform = '';
            pullIndicator.classList.remove('ready');
        });
    }
    
    // Mobile notifications
    function initMobileNotifications() {
        // Show toast notifications
        window.showToast = function(message, duration = 3000) {
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = message;
            document.body.appendChild(toast);
            
            // Show toast
            setTimeout(() => {
                toast.classList.add('show');
            }, 100);
            
            // Hide toast
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => {
                    document.body.removeChild(toast);
                }, 300);
            }, duration);
        };
        
        // Show loading indicator
        window.showLoading = function(message = 'Loading...') {
            const loading = document.createElement('div');
            loading.className = 'loading-overlay';
            loading.innerHTML = `
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <div class="loading-text">${message}</div>
                </div>
            `;
            document.body.appendChild(loading);
            
            return {
                hide: function() {
                    loading.classList.add('fade-out');
                    setTimeout(() => {
                        if (document.body.contains(loading)) {
                            document.body.removeChild(loading);
                        }
                    }, 300);
                }
            };
        };
    }
    
    // Mobile-specific utilities
    const MobileUtils = {
        // Vibrate device (if supported)
        vibrate: function(pattern) {
            if ('vibrate' in navigator) {
                navigator.vibrate(pattern);
            }
        },
        
        // Share content
        share: function(data) {
            if ('share' in navigator) {
                navigator.share(data);
            } else {
                // Fallback: copy to clipboard
                this.copyToClipboard(data.url || data.text);
                window.showToast('Link copied to clipboard');
            }
        },
        
        // Copy to clipboard
        copyToClipboard: function(text) {
            if ('clipboard' in navigator) {
                navigator.clipboard.writeText(text);
            } else {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
            }
        },
        
        // Get device info
        getDeviceInfo: function() {
            return {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                cookieEnabled: navigator.cookieEnabled,
                onLine: navigator.onLine,
                screenWidth: screen.width,
                screenHeight: screen.height,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight,
                pixelRatio: window.devicePixelRatio
            };
        },
        
        // Check network status
        isOnline: function() {
            return navigator.onLine;
        },
        
        // Add network status listener
        onNetworkChange: function(callback) {
            window.addEventListener('online', () => callback(true));
            window.addEventListener('offline', () => callback(false));
        }
    };
    
    // Expose utilities globally
    window.MobileUtils = MobileUtils;
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileApp);
    } else {
        initMobileApp();
    }
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            document.body.classList.add('page-hidden');
        } else {
            document.body.classList.remove('page-hidden');
        }
    });
    
    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            // Recalculate layouts after orientation change
            window.dispatchEvent(new Event('resize'));
        }, 100);
    });
    
    // Handle app state changes (for Capacitor)
    if (window.Capacitor) {
        window.Capacitor.Plugins.App.addListener('appStateChange', function(state) {
            if (state.isActive) {
                document.body.classList.remove('app-background');
            } else {
                document.body.classList.add('app-background');
            }
        });
        
        window.Capacitor.Plugins.App.addListener('appUrlOpen', function(data) {
            // Handle deep links
            console.log('App opened with URL:', data.url);
        });
    }
    
})(); 