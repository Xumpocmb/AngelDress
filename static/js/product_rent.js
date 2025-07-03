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

    const rentButton = document.getElementById('rent-button');
    if (rentButton) {
        rentButton.addEventListener('click', function () {
            const itemId = this.dataset.id;
            const itemIdsInput = document.getElementById('item_ids');
            if (itemIdsInput) {
                itemIdsInput.value = JSON.stringify([itemId]);
            }

            if (typeof window.openModal === 'function') {
                window.openModal();
            } else {
                console.error('Функция openModal не определена');
            }
        });
    }

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
            .then(async response => {
                const contentType = response.headers.get("content-type");

                let data;
                if (contentType && contentType.includes("application/json")) {
                    data = await response.json();
                } else {
                    const text = await response.text();
                    throw new Error(`Unexpected response format: ${text}`);
                }

                if (!response.ok) {
                    throw new Error(data.error || 'Server error');
                }

                return data;
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
