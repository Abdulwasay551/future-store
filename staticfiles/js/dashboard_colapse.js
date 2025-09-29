// Module collapse/expand functionality
function toggleApp(header, event) {
    if (event.target.tagName.toLowerCase() === 'a') return;
    
    const modelList = header.nextElementSibling;
    const icon = header.querySelector('.app-icon');
    
    const isCollapsed = modelList.classList.toggle('collapsed');
    icon.classList.toggle('rotated');
    
    const appName = header.querySelector('a').textContent.trim();
    localStorage.setItem(`app-${appName}-collapsed`, isCollapsed);
    
    // Add smooth animation
    if (!isCollapsed) {
        modelList.style.display = 'block';
        setTimeout(() => {
            modelList.style.maxHeight = `${modelList.scrollHeight}px`;
            modelList.style.opacity = '1';
        }, 10);
    } else {
        modelList.style.maxHeight = '0';
        modelList.style.opacity = '0';
    }
}

// Initialize collapse states
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.app-header').forEach(header => {
        const appName = header.querySelector('a').textContent.trim();
        const modelList = header.nextElementSibling;
        const icon = header.querySelector('.app-icon');
        
        if (localStorage.getItem(`app-${appName}-collapsed`) === 'true') {
            modelList.classList.add('collapsed');
            icon.classList.add('rotated');
        }
    });
});