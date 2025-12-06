document.addEventListener('DOMContentLoaded', function () {
  // Sidebar functionality
  const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
  const mobileSidebar = document.getElementById('mobileSidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const closeSidebarBtn = document.getElementById('closeSidebarBtn');

  // Open sidebar
  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener('click', function () {
      mobileSidebar.classList.add('active');
      sidebarOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  }

  // Close sidebar
  function closeSidebar() {
    mobileSidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  if (closeSidebarBtn) {
    closeSidebarBtn.addEventListener('click', closeSidebar);
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }

  // Close sidebar when clicking on links
  const sidebarLinks = document.querySelectorAll('.sidebar-nav-link');
  sidebarLinks.forEach(link => {
    link.addEventListener('click', closeSidebar);
  });

  // Avatar dropdown
  const avatarContainer = document.getElementById('avatarContainer');
  const dropdownMenu = document.getElementById('dropdownMenu');

  if (avatarContainer && dropdownMenu) {
    avatarContainer.addEventListener('click', function (e) {
      e.stopPropagation();
      avatarContainer.classList.toggle('active');
      dropdownMenu.classList.toggle('show');
    });

    document.addEventListener('click', function (e) {
      if (!avatarContainer.contains(e.target) && !dropdownMenu.contains(e.target)) {
        avatarContainer.classList.remove('active');
        dropdownMenu.classList.remove('show');
      }
    });
  }

  // Navbar scroll effect
  window.addEventListener('scroll', function () {
    const navbar = document.getElementById('mainNav');
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(255, 255, 255, 0.25)';
      navbar.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.12)';
    } else {
      navbar.style.background = 'rgba(255, 255, 255, 0.15)';
      navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.08)';
    }
  });

  // Feed dropdown
  const feedToggle = document.getElementById("feedDropdown");
  const feedMenu = document.getElementById("feedDropdownMenu");

  if (feedToggle && feedMenu) {
    feedToggle.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      feedMenu.classList.toggle("show");
    });

    document.addEventListener("click", function (e) {
      if (!feedToggle.contains(e.target) && !feedMenu.contains(e.target)) {
        feedMenu.classList.remove("show");
      }
    });
  }

  // Auto-dismiss alerts
  const alerts = document.querySelectorAll('.alert-message');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.animation = 'slideUp 0.3s ease-out forwards';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });
});