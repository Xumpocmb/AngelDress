document.addEventListener('DOMContentLoaded', function () {
    // Получаем элементы по правильным селекторам
    const searchInput = document.querySelector('.search-input');
    const clearIcon = document.getElementById('clearSearchIcon');
    const searchForm = document.getElementById('searchForm');

    // Показать/скрыть иконку очистки в зависимости от содержимого поля
    if (searchInput && clearIcon) {
        // Инициализируем видимость иконки при загрузке
        clearIcon.style.display = searchInput.value ? 'block' : 'none';

        searchInput.addEventListener('input', function () {
            clearIcon.style.display = this.value ? 'block' : 'none';
        });

        // Очистка поля и отправка формы при клике на иконку
        clearIcon.addEventListener('click', function (e) {
            e.preventDefault(); // Предотвращаем возможное другое поведение
            searchInput.value = '';
            clearIcon.style.display = 'none';
            searchForm.submit();
        });
    }
});