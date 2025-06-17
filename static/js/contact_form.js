document.addEventListener('DOMContentLoaded', () => {
    // Contact form functionality
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const formData = new FormData(contactForm);
            const name = formData.get('name');
            const phone = formData.get('phone');
            const email = formData.get('email');
            const agreement = formData.get('agreement');

            // Basic validation
            if (!name || !phone || !email || !agreement) {
                alert('Пожалуйста, заполните все поля и подтвердите согласие на обработку данных.');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Пожалуйста, введите корректный email адрес.');
                return;
            }

            // Phone validation (basic)
            const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
            if (!phoneRegex.test(phone)) {
                alert('Пожалуйста, введите корректный номер телефона.');
                return;
            }

            // Simulate form submission
            const submitBtn = contactForm.querySelector('.submit_btn');
            const originalText = submitBtn.textContent;

            submitBtn.textContent = 'ОТПРАВЛЯЕМ...';
            submitBtn.disabled = true;

            setTimeout(() => {
                alert(`Спасибо, ${name}! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.`);
                contactForm.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });

        // Phone number formatting
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => {
                const target = e.target;
                let value = target.value.replace(/\D/g, '');

                if (value.length > 0) {
                    if (value.startsWith('8')) {
                        value = '7' + value.substring(1);
                    }
                    if (!value.startsWith('7')) {
                        value = '7' + value;
                    }

                    let formatted = '+7';
                    if (value.length > 1) {
                        formatted += ' (' + value.substring(1, 4);
                    }
                    if (value.length >= 4) {
                        formatted += ') ' + value.substring(4, 7);
                    }
                    if (value.length >= 7) {
                        formatted += '-' + value.substring(7, 9);
                    }
                    if (value.length >= 9) {
                        formatted += '-' + value.substring(9, 11);
                    }

                    target.value = formatted;
                }
            });
        }
    }
});
