document.addEventListener('DOMContentLoaded', function () {
    const rentModal = document.getElementById('rentModal');
    const contactForm = document.getElementById('contactForm');
    const submitButton = contactForm.querySelector('.submit_btn');

    function openModal() {
        rentModal.style.display = 'block';
    }

    function closeModal(e) {
        if (!e ||
            e.target.classList.contains('modal-overlay') ||
            e.target.classList.contains('modal-close')) {
            rentModal.style.display = 'none';
            contactForm.reset();
            submitButton.textContent = 'ЗАБРОНИРОВАТЬ ПРИМЕРКУ';
            submitButton.disabled = false;
        }
    }

    window.openModal = openModal;
    window.closeModal = closeModal;

    document.querySelectorAll('.rent-button').forEach(button => {
        button.addEventListener('click', function () {
            const dressId = this.closest('.product-card').querySelector('.product-image').dataset.id;
            document.getElementById('dress_ids').value = JSON.stringify([dressId]);
            openModal();
        });
    });

    document.querySelector('.rent-all-button').addEventListener('click', function () {
        const dressIds = Array.from(document.querySelectorAll('.product-card')).map(card => {
            return card.querySelector('.product-image').dataset.id;
        });
        document.getElementById('dress_ids').value = JSON.stringify(dressIds);
        openModal();
    });

    contactForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const csrfToken = document.querySelector('[name=csrf-token]').content;

        submitButton.disabled = true;
        submitButton.textContent = 'Отправка заявки...';
        submitButton.classList.remove('success', 'error');

        fetch('/book/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Server error');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    submitButton.textContent = 'Заявка отправлена!';
                    submitButton.classList.add('success');
                    setTimeout(() => {
                        closeModal();
                        contactForm.reset();
                        submitButton.textContent = 'ЗАБРОНИРОВАТЬ ПРИМЕРКУ';
                        submitButton.disabled = false;
                        submitButton.classList.remove('success');
                    }, 2000);
                } else {
                    const errorMessage = data.error || (data.errors ? Object.values(data.errors).join(', ') : 'Произошла ошибка!');
                    submitButton.textContent = 'Ошибка: ' + errorMessage;
                    submitButton.classList.add('error');
                    submitButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                submitButton.textContent = 'Ошибка сети или сервера';
                submitButton.classList.add('error');
                submitButton.disabled = false;
            });
    });
});
