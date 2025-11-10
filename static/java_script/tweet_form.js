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

        const textArea = document.getElementById('id_text');
        const charCounter = document.getElementById('charCounter');

        if (textArea && charCounter) {
            charCounter.textContent = textArea.value.length + '/280';
            
            textArea.addEventListener('input', function() {
                const length = this.value.length;
                charCounter.textContent = length + '/280';
                
                charCounter.classList.remove('warning', 'error');
                if (length > 250) {
                    charCounter.classList.add('warning');
                }
                if (length > 280) {
                    charCounter.classList.add('error');
                }
            });
        }