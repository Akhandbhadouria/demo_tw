 // Navbar scroll effect
    window.addEventListener('scroll', function () {
      const nav = document.getElementById('mainNav');
      if (window.scrollY > 50) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    });

    // Dropdown functionality
    document.addEventListener('DOMContentLoaded', function() {
      const avatarContainer = document.getElementById('avatarContainer');
      const userMenu = document.querySelector('.user-menu');
      
      if (avatarContainer) {
        avatarContainer.addEventListener('click', function(e) {
          e.stopPropagation();
          userMenu.classList.toggle('active');
        });
      }
      
      // Close dropdown when clicking outside
      document.addEventListener('click', function(e) {
        if (userMenu && !userMenu.contains(e.target)) {
          userMenu.classList.remove('active');
        }
      });
      
      // Close dropdown when pressing Escape key
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          userMenu.classList.remove('active');
        }
      });
    });

    // Scroll animations
    function animateOnScroll() {
      const elements = document.querySelectorAll('.scroll-animate');
      elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;

        if (elementTop < window.innerHeight - 100 && elementBottom > 0) {
          element.classList.add('active');
        }
      });
    }

    window.addEventListener('scroll', animateOnScroll);
    window.addEventListener('load', animateOnScroll);

    document.addEventListener('DOMContentLoaded', function () {
      const container = document.querySelector('.container');
      if (container) {
        const children = container.children;
        for (let i = 0; i < children.length; i++) {
          children[i].classList.add('scroll-animate');
          children[i].style.transitionDelay = (i * 0.1) + 's';
        }
      }
    });