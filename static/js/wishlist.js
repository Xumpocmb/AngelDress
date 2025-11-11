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
        if (data.status === 'added') {
            element.classList.add('just-added');
            setTimeout(() => {
                element.classList.remove('just-added');
            }, 500);
        }
        // updateWishlistCount(data.count);
    } catch (error) {
        console.error('Error:', error);
    }
}

// async function toggleWishlistButton(button, dressId) {
//     try {
//         const csrfToken = await getCSRFToken();
//         const response = await fetch(`/wishlist/api/toggle/${dressId}/`, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': csrfToken,
//                 'Content-Type': 'application/json'
//             },
//             credentials: 'same-origin'
//         });
//
//         const data = await response.json();
//
//         if (data.status === 'added') {
//             button.classList.add('in-wishlist', 'just-added');
//             button.textContent = '✓ В ИЗБРАННОМ';
//
//             setTimeout(() => {
//                 button.classList.remove('just-added');
//             }, 700);
//         } else {
//             button.classList.remove('in-wishlist');
//             button.textContent = 'ДОБАВИТЬ В ИЗБРАННОЕ';
//         }
//
//         updateWishlistCount(data.count);
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// Функция для работы с иконкой избранного в карточке товара (адаптирована с рабочего варианта)
async function toggleProductWishlist(iconElement, productId, modelType) {
    try {
        // Добавляем анимацию сразу при клике
        iconElement.classList.add('wishlist-just-added');

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                         document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        // Используем тот же URL, что и в рабочем варианте, но с параметром типа товара
        const response = await fetch(`/wishlist/api/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify({
                model_type: modelType // 'dress' или 'accessory'
            })
        });

        const data = await response.json();

        if (data.status === 'added') {
            // Добавлено в избранное
            iconElement.classList.add('product-wishlist-active');

            // Можно добавить дополнительную анимацию при добавлении
            setTimeout(() => {
                iconElement.classList.remove('wishlist-just-added');
            }, 700);
        } else {
            // Удалено из избранного
            iconElement.classList.remove('product-wishlist-active');

            setTimeout(() => {
                iconElement.classList.remove('wishlist-just-added');
            }, 500);
        }

        // updateWishlistCount(data.count);

    } catch (error) {
        console.error('Error toggling wishlist:', error);
        // Убираем анимацию в случае ошибки
        setTimeout(() => {
            iconElement.classList.remove('wishlist-just-added');
        }, 500);
    }
}


// function updateWishlistCount(count) {
//     const counterElements = document.querySelectorAll('.wishlist-count');
//     counterElements.forEach(el => {
//         el.textContent = count;
//     });
// }

// document.addEventListener('DOMContentLoaded', function () {
//     fetch('/wishlist/api/count/')
//         .then(response => response.json())
//         .then(data => updateWishlistCount(data.count))
//         .catch(error => console.error('Error:', error));
// });
