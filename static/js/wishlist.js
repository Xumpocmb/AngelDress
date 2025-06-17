async function getCSRFToken() {
    let csrfToken = null;
    const metaTags = document.getElementsByTagName('meta');
    for (let tag of metaTags) {
        if (tag.name === 'csrf-token') {
            csrfToken = tag.content;
            break;
        }
    }
    return csrfToken;
}


async function toggleWishlist(element, dressId) {
    try {
        const csrfToken = await getCSRFToken();
        const response = await fetch(`/wishlist/api/toggle/${dressId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        });

        const data = await response.json();
        element.classList.toggle('active');
        updateWishlistCount(data.count);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function toggleWishlistButton(button, dressId) {
    try {
        const csrfToken = await getCSRFToken();
        const response = await fetch(`/wishlist/api/toggle/${dressId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        });

        const data = await response.json();

        if (data.status === 'added') {
            button.classList.add('in-wishlist', 'just-added');
            button.textContent = '✓ В ИЗБРАННОМ';

            setTimeout(() => {
                button.classList.remove('just-added');
            }, 700);
        } else {
            button.classList.remove('in-wishlist');
            button.textContent = 'ДОБАВИТЬ В ИЗБРАННОЕ';
        }

        updateWishlistCount(data.count);
    } catch (error) {
        console.error('Error:', error);
    }
}


function updateWishlistCount(count) {
    const counterElements = document.querySelectorAll('.wishlist-count');
    counterElements.forEach(el => {
        el.textContent = count;
        el.style.display = count > 0 ? 'block' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', function () {
    fetch('/wishlist/api/count/')
        .then(response => response.json())
        .then(data => updateWishlistCount(data.count))
        .catch(error => console.error('Error:', error));
});
