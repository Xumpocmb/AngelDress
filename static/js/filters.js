document.addEventListener('DOMContentLoaded', function () {
    // Открытие/закрытие выпадающих фильтров
    document.querySelectorAll('.filter-toggle').forEach(toggle => {
        toggle.addEventListener('click', function () {
            const dropdown = this.closest('.filter-dropdown');
            document.querySelectorAll('.filter-dropdown').forEach(d => {
                if (d !== dropdown) d.classList.remove('active');
            });
            dropdown.classList.toggle('active');
        });
    });

    // Закрытие фильтров при клике вне их
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.filter-dropdown')) {
            document.querySelectorAll('.filter-dropdown').forEach(d => {
                d.classList.remove('active');
            });
        }
    });

    // Очистка поиска
    const clearSearch = document.querySelector('.clear-search');
    if (clearSearch) {
        clearSearch.addEventListener('click', function () {
            document.querySelector('.search-input').value = '';
            document.getElementById('searchForm').submit();
        });
    }
});

document.querySelectorAll('.filter-toggle').forEach(button => {
    button.addEventListener('click', () => {
        const options = button.nextElementSibling;
        options.classList.toggle('active');
    });
});