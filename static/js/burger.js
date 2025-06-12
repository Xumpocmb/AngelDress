document.addEventListener('DOMContentLoaded', () => {
    const burgerBtn = document.querySelector('.burger-btn');
    const navContainer = document.querySelector('.nav-container');

    burgerBtn.addEventListener('click', () => {
        burgerBtn.classList.toggle('active');
        navContainer.classList.toggle('active');
        burgerBtn.setAttribute('aria-expanded',
            burgerBtn.classList.contains('active'));
    });

    // Закрытие меню при клике на ссылку
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 992) {
                burgerBtn.classList.remove('active');
                navContainer.classList.remove('active');
                burgerBtn.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Закрытие меню при ресайзе (если вдруг пользователь повернул устройство)
    window.addEventListener('resize', () => {
        if (window.innerWidth > 992) {
            burgerBtn.classList.remove('active');
            navContainer.classList.remove('active');
            burgerBtn.setAttribute('aria-expanded', 'false');
        }
    });
});