// Get the canvas element
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions with device pixel ratio for crisp rendering
function resizeCanvas() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = window.innerWidth * dpr;
  canvas.height = window.innerHeight * dpr;
  
  // Scale context according to dpr for sharp rendering
  ctx.scale(dpr, dpr);
  
  // Set canvas CSS size
  canvas.style.width = window.innerWidth + 'px';
  canvas.style.height = window.innerHeight + 'px';
  
  // Reinitialize particles when canvas is resized
  if (particlesArray && particlesArray.length > 0) {
    particlesArray.length = 0;
    init();
  }
}

// Track dark mode to adjust particle colors
let isDarkMode = document.documentElement.classList.contains('dark');

// Watch for theme changes to update particle colors
const themeObserver = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    if (mutation.attributeName === 'class') {
      isDarkMode = document.documentElement.classList.contains('dark');
      updateParticleColors();
    }
  });
});

themeObserver.observe(document.documentElement, { attributes: true });

// Particles configuration
let particlesArray = [];
const baseParticleCount = Math.min(Math.floor(window.innerWidth / 10), 150); // Responsive particle count
let numberOfParticles = baseParticleCount;

// Color palettes for light and dark modes
const lightModeColors2 = {
  particles: [
    'rgba(59, 130, 246, 0.5)', // Blue
    'rgba(255, 165, 0, 0.5)',  // Orange
    'rgba(99, 102, 241, 0.5)'  // Indigo
  ],
  connections: 'rgba(59, 130, 246, 0.2)'
};

const darkModeColors2 = {
  particles: [
    'rgba(96, 165, 250, 0.5)',   // Light blue
    'rgba(147, 112, 219, 0.5)',  // Purple
    'rgba(138, 43, 226, 0.5)'    // Violet
  ],
  connections: 'rgba(147, 112, 219, 0.2)'
};

// Enhanced Particle class
class Particle {
  constructor(x, y, isMouseParticle = false) {
    this.x = x || Math.random() * window.innerWidth;
    this.y = y || Math.random() * window.innerHeight;
    this.size = isMouseParticle ? Math.random() * 4 + 1 : Math.random() * 3 + 0.5;
    this.baseSize = this.size;
    this.speedX = (Math.random() - 0.5) * 0.8;
    this.speedY = (Math.random() - 0.5) * 0.8;
    this.isMouseParticle = isMouseParticle;
    
    // Assign color based on theme
    const colors = isDarkMode ? darkModeColors2.particles : lightModeColors2.particles;
    this.color = colors[Math.floor(Math.random() * colors.length)];
    
    // Add properties for animations
    this.angle = Math.random() * Math.PI * 2;
    this.angleSpeed = Math.random() * 0.01 - 0.005;
    this.pulseFactor = 0;
    this.pulseSpeed = Math.random() * 0.04 + 0.01;
    this.lifetime = isMouseParticle ? 100 : Infinity;
  }
  
  update() {
    // Update position
    this.x += this.speedX;
    this.y += this.speedY;
    
    // Add gentle oscillation
    if (!this.isMouseParticle) {
      this.x += Math.sin(this.angle) * 0.2;
      this.y += Math.cos(this.angle) * 0.2;
      this.angle += this.angleSpeed;
    }
    
    // Pulse size animation
    this.pulseFactor += this.pulseSpeed;
    const pulseMagnitude = Math.sin(this.pulseFactor) * 0.5 + 1;
    this.size = this.baseSize * pulseMagnitude;
    
    // Decrease lifetime for mouse particles
    if (this.isMouseParticle) {
      this.lifetime--;
      if (this.lifetime <= 0) {
        return false;
      }
      
      // Fade out as lifetime decreases
      this.color = this.color.replace(/[\d.]+\)$/, (Math.min(this.lifetime / 100, 1) * 0.7) + ')');
    }
    
    // Bounce off edges with damping
    if (this.x > window.innerWidth || this.x < 0) {
      this.speedX = -this.speedX * 0.9;
      if (this.x > window.innerWidth) this.x = window.innerWidth;
      if (this.x < 0) this.x = 0;
    }
    
    if (this.y > window.innerHeight || this.y < 0) {
      this.speedY = -this.speedY * 0.9;
      if (this.y > window.innerHeight) this.y = window.innerHeight;
      if (this.y < 0) this.y = 0;
    }
    
    return true;
  }
  
  draw() {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
    
    // Add glow effect
    ctx.shadowColor = this.color;
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.shadowBlur = 0;
  }
}

// Initialize particles
function init() {
  particlesArray = [];
  numberOfParticles = baseParticleCount;
  
  for (let i = 0; i < numberOfParticles; i++) {
    particlesArray.push(new Particle());
  }
}

// Update particle colors when theme changes
function updateParticleColors() {
  const colors = isDarkMode ? darkModeColors2.particles : lightModeColors2.particles;
  
  for (let i = 0; i < particlesArray.length; i++) {
    if (!particlesArray[i].isMouseParticle) {
      particlesArray[i].color = colors[Math.floor(Math.random() * colors.length)];
    }
  }
}

// Draw connections between particles
function connect() {
  const maxDistance = Math.min(window.innerWidth / 5, 150);
  const connectionColor = isDarkMode ? darkModeColors2.connections : lightModeColors2.connections;
  
  for (let a = 0; a < particlesArray.length; a++) {
    for (let b = a; b < particlesArray.length; b++) {
      const dx = particlesArray[a].x - particlesArray[b].x;
      const dy = particlesArray[a].y - particlesArray[b].y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < maxDistance) {
        const opacity = 1 - (distance / maxDistance);
        
        // Create gradient for connections
        const gradient = ctx.createLinearGradient(
          particlesArray[a].x, particlesArray[a].y, 
          particlesArray[b].x, particlesArray[b].y
        );
        
        gradient.addColorStop(0, particlesArray[a].color.replace(/[\d.]+\)$/, opacity * 0.5 + ')'));
        gradient.addColorStop(1, particlesArray[b].color.replace(/[\d.]+\)$/, opacity * 0.5 + ')'));
        
        ctx.strokeStyle = gradient;
        ctx.lineWidth = opacity * 1.5;
        ctx.beginPath();
        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
        ctx.stroke();
      }
    }
  }
}

// Animation loop
function animate() {
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
  
  // Update and filter out dead particles
  particlesArray = particlesArray.filter(particle => {
    particle.update();
    particle.draw();
    return particle.lifetime > 0;
  });
  
  // Draw connections
  connect();
  
  requestAnimationFrame(animate);
}

// Mouse interaction variables
let mouse = {
  x: null,
  y: null,
  radius: 100
};

// Add mouse interaction
window.addEventListener('mousemove', function(event) {
  mouse.x = event.x;
  mouse.y = event.y;
  
  // Create particles on mouse movement
  if (Math.random() < 0.3) {
    const colors = isDarkMode ? darkModeColors2.particles : lightModeColors2.particles;
    const mouseParticle = new Particle(
      mouse.x + (Math.random() - 0.5) * 20,
      mouse.y + (Math.random() - 0.5) * 20,
      true
    );
    
    // Assign random direction
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 2 + 1;
    mouseParticle.speedX = Math.cos(angle) * speed;
    mouseParticle.speedY = Math.sin(angle) * speed;
    
    particlesArray.push(mouseParticle);
  }
  
  // Influence nearby particles
  for (let i = 0; i < particlesArray.length; i++) {
    const dx = particlesArray[i].x - mouse.x;
    const dy = particlesArray[i].y - mouse.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < mouse.radius && !particlesArray[i].isMouseParticle) {
      const force = (mouse.radius - distance) / mouse.radius;
      const directionX = dx / distance || 0;
      const directionY = dy / distance || 0;
      
      // Push particles away from cursor
      particlesArray[i].speedX += directionX * force * 0.2;
      particlesArray[i].speedY += directionY * force * 0.2;
    }
  }
});

// Add click effect
window.addEventListener('click', function(event) {
  // Create a ripple effect
  const rippleCount = 12;
  const colors = isDarkMode ? darkModeColors2.particles : lightModeColors2.particles;
  
  for (let i = 0; i < rippleCount; i++) {
    const angle = (i / rippleCount) * Math.PI * 2;
    const speed = Math.random() * 3 + 2;
    
    const particle = new Particle(mouse.x, mouse.y, true);
    particle.speedX = Math.cos(angle) * speed;
    particle.speedY = Math.sin(angle) * speed;
    particle.lifetime = 120 + Math.random() * 60;
    particle.size = Math.random() * 5 + 2;
    particle.baseSize = particle.size;
    
    particlesArray.push(particle);
  }
});

// Initialize and start animation
resizeCanvas();
window.addEventListener('resize', resizeCanvas);
init();
animate();