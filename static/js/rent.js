document.addEventListener('DOMContentLoaded', function () {
    function openModal() {
        document.getElementById('rentModal').style.display = 'block';
    }

    function closeModal(e) {
        if (!e ||
            e.target.classList.contains('modal-overlay') ||
            e.target.classList.contains('modal-close')) {
            document.getElementById('rentModal').style.display = 'none';
        }
    }

    window.openModal = openModal;
    window.closeModal = closeModal;

    // Вешаем на кнопки
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

    document.getElementById('contactForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const csrfToken = document.querySelector('[name=csrf-token]').content;

        fetch('/book/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    closeModal();
                    alert('Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
                } else {
                    alert('Ошибка: ' + (data.error || 'Пожалуйста, проверьте введенные данные'))
                }
            })
            .catch(error => {
                console.error('Error!', error);
                alert('Произошла ошибка при отправке заявки');
            });
    });
});