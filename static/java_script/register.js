const starsContainer = document.getElementById('stars');
if (starsContainer) {
    const starCount = 100;
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        starsContainer.appendChild(star);
    }
}

// Password strength indicator
const password1Input = document.getElementById('id_password1');
const strengthIndicator = document.getElementById('strength-indicator');

if (password1Input && strengthIndicator) {
    const strengthBar = strengthIndicator.querySelector('.strength-bar');

    function calculatePasswordStrength(password) {
        let strength = 0;

        if (password.length >= 8) strength++;
        if (password.length >= 12) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;

        return strength;
    }

    password1Input.addEventListener('input', (e) => {
        const password = e.target.value;
        const strength = calculatePasswordStrength(password);

        if (password.length === 0) {
            strengthIndicator.classList.remove('show');
        } else {
            strengthIndicator.classList.add('show');
            strengthBar.className = 'strength-bar';

            if (strength < 2) {
                strengthBar.classList.add('strength-weak');
            } else if (strength < 4) {
                strengthBar.classList.add('strength-medium');
            } else {
                strengthBar.classList.add('strength-strong');
            }
        }
    });
}

// Form submission animation
const authForm = document.querySelector('.auth-form');
if (authForm) {
    authForm.addEventListener('submit', function (e) {
        const btn = this.querySelector('.btn-submit');
        if (btn) {
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = '';
            }, 100);
        }
    });
}

// Input focus animations
const formInputs = document.querySelectorAll('.form-input');
formInputs.forEach(input => {
    input.addEventListener('focus', function (e) {
        this.parentElement.classList.add('focused'); // Keep existing logic
        e.target.style.transform = 'scale(1.02)'; // Add new inline logic
    });

    input.addEventListener('blur', function (e) {
        this.parentElement.classList.remove('focused'); // Keep existing logic
        e.target.style.transform = 'scale(1)'; // Add new inline logic
    });
});