        const starsContainer = document.getElementById('stars');
        const starCount = 100;

        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 3 + 's';
            starsContainer.appendChild(star);
        }

        const formInputs = document.querySelectorAll('.form-input');
        formInputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        });

        const usernameField = document.getElementById('id_username');
        if (usernameField) {
            usernameField.focus();
        }

        function openGooglePopup(url) {
    const width = 600;
    const height = 600;
    const left = (screen.width / 2) - (width / 2);
    const top = (screen.height / 2) - (height / 2);

    const popup = window.open(
        url,
        "Google Login",
        `width=${width},height=${height},top=${top},left=${left},resizable=yes,scrollbars=yes`
    );

    // Optional: Poll the popup for closure to reload parent page
    const timer = setInterval(function() {
        if (popup.closed) {
            clearInterval(timer);
            window.location.reload(); // refresh page after login
        }
    }, 500);
}

