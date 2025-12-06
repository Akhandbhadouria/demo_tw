// Theme Switching
const avatarItems = document.querySelectorAll('.avatars-item');
const body = document.body;

avatarItems.forEach(avatar => {
    avatar.addEventListener('click', function () {
        avatarItems.forEach(item => item.classList.remove('active'));
        this.classList.add('active');

        const theme = this.getAttribute('data-theme');
        body.classList.remove('theme-blue', 'theme-blue-purple');

        if (theme !== 'default') {
            body.classList.add(theme);
        }

        localStorage.setItem('selectedTheme', theme);
    });
});

// Load saved theme
window.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('selectedTheme') || 'default';
    const savedAvatar = document.querySelector(`[data-theme="${savedTheme}"]`);
    if (savedAvatar) {
        savedAvatar.click();
    }

    // Animate hero section immediately on load
    const heroSection = document.querySelector('.max-container');
    const heroLeft = document.querySelector('.hero-left');
    if (heroSection && heroLeft) {
        heroSection.classList.add('animate-in');
        heroLeft.classList.add('animate-in');
    }
});

// Enhanced Scroll Animations with Intersection Observer
const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe all scroll sections (except hero which animates on load)
document.querySelectorAll('.scroll-section').forEach(section => {
    if (!section.classList.contains('max-container')) {
        observer.observe(section);
    }
});

// Parallax effect on scroll
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const circles = document.querySelectorAll('.bg-circle');

    circles.forEach((circle, index) => {
        const speed = (index + 1) * 0.05;
        circle.style.transform = `translateY(${scrolled * speed}px)`;
    });

    lastScroll = scrolled;
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Add animated circles
const container = document.querySelector('.main-container');
if (container) {
    const circle1 = document.createElement('div');
    circle1.className = 'bg-circle circle1';
    const circle2 = document.createElement('div');
    circle2.className = 'bg-circle circle2';
    container.appendChild(circle1);
    container.appendChild(circle2);
}