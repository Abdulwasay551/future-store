document.addEventListener('DOMContentLoaded', function() {
    // Create background elements
    const techBackground = document.createElement('div');
    techBackground.className = 'tech-background';
    
    const hexGrid = document.createElement('div');
    hexGrid.className = 'hex-grid';
    
    // Add hex grid to tech background
    techBackground.appendChild(hexGrid);
    
    // Insert at the start of body
    const body = document.body;
    const sidbar = document.getElementById('nav-sidebar');
    if (body.firstChild) {
        body.insertBefore(techBackground, body.firstChild);
    } else {
        body.appendChild(techBackground);
    }
});
