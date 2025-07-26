document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('.filters-toggle-button');
    const dropdownContent = document.querySelector('.filters-dropdown-content');

    if (toggleButton && dropdownContent) {
        toggleButton.addEventListener('click', function () {
            this.classList.toggle('active');
            dropdownContent.classList.toggle('active');

            // Опционально: Сброс инлайновых стилей, если они мешают анимации
            // dropdownContent.style.cssText = '';
        });

        // Опционально: Закрытие при клике вне аккордеона (если нужно)
        // document.addEventListener('click', function(event) {
        //     if (!toggleButton.contains(event.target) && !dropdownContent.contains(event.target)) {
        //         toggleButton.classList.remove('active');
        //         dropdownContent.classList.remove('active');
        //     }
        // });
    }

    // Обновляем счетчик выбранных фильтров (если функция существует)
    if (typeof updateFiltersCount === 'function') {
        updateFiltersCount();
    }
});

// Обновляем счетчик при изменении фильтров (если функция существует)
document.addEventListener('change', function(e) {
    if (e.target.closest('#filterForm')) {
        // Добавим небольшую задержку, чтобы убедиться, что состояние чекбоксов обновилось
        setTimeout(updateFiltersCount, 0);
    }
});

// Функция обновления счетчика (если еще не определена в другом месте)
function updateFiltersCount() {
    const filterForm = document.getElementById('filterForm');
    const countElement = document.querySelector('.filters-count');

    if (filterForm && countElement) {
        // Считаем отмеченные чекбоксы
        const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]:checked');

        // Считаем выбранные селекты (кроме сортировки)
        const selects = filterForm.querySelectorAll('select');
        let selectCount = 0;
        selects.forEach(select => {
            if (select.name !== 'sort' && select.value) {
                // Проверяем, отличается ли значение от дефолтного (например, пустого или "newest")
                // Это зависит от твоей логики. Пример:
                if (select.value !== '' && select.value !== 'newest') {
                    selectCount++;
                }
            }
        });

        const totalCount = checkboxes.length + selectCount;

        if (totalCount > 0) {
            countElement.textContent = `(${totalCount})`;
        } else {
            countElement.textContent = '';
        }
    }
}
