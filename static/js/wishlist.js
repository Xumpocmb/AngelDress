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


// Функция для переключения избранного
async function toggleFavorite(element, dressId) {
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

// Обновление счетчика избранного
function updateWishlistCount(count) {
    const counterElements = document.querySelectorAll('.wishlist-count');
    counterElements.forEach(el => {
        el.textContent = count;
        el.style.display = count > 0 ? 'block' : 'none';
    });
}

// Загрузка количества избранного при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fetch('/wishlist/api/count/')
        .then(response => response.json())
        .then(data => updateWishlistCount(data.count))
        .catch(error => console.error('Error:', error));
});