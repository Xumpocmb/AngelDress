document.addEventListener('DOMContentLoaded', function () {
    const rentModal = document.getElementById('rentModal');
    const contactForm = document.getElementById('contactForm');
    const submitButton = contactForm.querySelector('.submit_btn'); // Get the submit button

    function openModal() {
        rentModal.style.display = 'block';
    }

    function closeModal(e) {
        if (!e ||
            e.target.classList.contains('modal-overlay') ||
            e.target.classList.contains('modal-close')) {
            rentModal.style.display = 'none';
            // Optionally reset the form and button state when closing
            contactForm.reset();
            submitButton.textContent = 'ЗАБРОНИРОВАТЬ ПРИМЕРКУ';
            submitButton.disabled = false;
        }
    }

    // Expose to global scope for onclick attributes in HTML
    window.openModal = openModal;
    window.closeModal = closeModal;

    // Attach click listeners to individual rent buttons
    document.querySelectorAll('.rent-button').forEach(button => {
        button.addEventListener('click', function () {
            const dressId = this.closest('.product-card').querySelector('.product-image').dataset.id;
            document.getElementById('dress_ids').value = JSON.stringify([dressId]);
            openModal();
        });
    });

    // Attach click listener to the "Rent All" button
    document.querySelector('.rent-all-button').addEventListener('click', function () {
        const dressIds = Array.from(document.querySelectorAll('.product-card')).map(card => {
            return card.querySelector('.product-image').dataset.id;
        });
        document.getElementById('dress_ids').value = JSON.stringify(dressIds);
        openModal();
    });

    // Handle form submission
    contactForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const csrfToken = document.querySelector('[name=csrf-token]').content;

        // Disable button and change text
        submitButton.disabled = true;
        submitButton.textContent = 'Отправка заявки...';
        submitButton.classList.remove('success', 'error'); // Remove previous states

        fetch('/book/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest' // Important for Django's is_ajax()
            },
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    // If response is not 2xx, throw an error to be caught by .catch()
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
                    // Close the modal after a short delay
                    // Give user a moment to see the success message then close and reset
                    setTimeout(() => {
                        closeModal();
                        contactForm.reset(); // Clear the form fields
                        submitButton.textContent = 'ЗАБРОНИРОВАТЬ ПРИМЕРКУ'; // Reset button text
                        submitButton.disabled = false;
                        submitButton.classList.remove('success');
                    }, 2000); // Wait 2 seconds before closing
                } else {
                    // Display specific error from Django's JsonResponse or generic error
                    const errorMessage = data.error || (data.errors ? Object.values(data.errors).join(', ') : 'Произошла ошибка!');
                    submitButton.textContent = 'Ошибка: ' + errorMessage;
                    submitButton.classList.add('error');
                    submitButton.disabled = false; // Re-enable button
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                submitButton.textContent = 'Ошибка сети или сервера';
                submitButton.classList.add('error');
                submitButton.disabled = false; // Re-enable button
            });
    });
});