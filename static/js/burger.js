// const burger = document.getElementById('burger');
// const mobileMenu = document.getElementById('mobileMenu');
// burger.addEventListener('click', () => { burger.classList.toggle('active'); mobileMenu.classList.toggle('active'); document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : ''; });
// window.addEventListener('resize', () => { if (window.innerWidth > 1020 && mobileMenu.classList.contains('active')) { burger.classList.remove('active'); mobileMenu.classList.remove('active'); document.body.style.overflow = ''; } });

// const callbackForm = document.getElementById('callbackForm');
// const closeCallbackForm = document.getElementById('closeCallbackForm');
// const openBtns = document.querySelectorAll('.openCallbackForm');
// openBtns.forEach(btn => { btn.addEventListener('click', e => { e.preventDefault(); callbackForm.classList.add('active'); document.body.style.overflow = 'hidden'; burger.classList.remove('active'); mobileMenu.classList.remove('active'); }); });
// closeCallbackForm.addEventListener('click', () => { callbackForm.classList.remove('active'); document.body.style.overflow = ''; });
// callbackForm.addEventListener('click', e => { if (e.target === callbackForm) { callbackForm.classList.remove('active'); document.body.style.overflow = ''; } });


// OLD

// document.addEventListener('DOMContentLoaded', () => {
//     const burgerBtn = document.querySelector('.burger-btn');
//     const navContainer = document.querySelector('.nav-container');

//     burgerBtn.addEventListener('click', () => {
//         burgerBtn.classList.toggle('active');
//         navContainer.classList.toggle('active');
//         burgerBtn.setAttribute('aria-expanded',
//             burgerBtn.classList.contains('active'));
//     });

//     // Закрытие меню при клике на ссылку
//     document.querySelectorAll('.nav-menu a').forEach(link => {
//         link.addEventListener('click', () => {
//             if (window.innerWidth <= 992) {
//                 burgerBtn.classList.remove('active');
//                 navContainer.classList.remove('active');
//                 burgerBtn.setAttribute('aria-expanded', 'false');
//             }
//         });
//     });

//     // Закрытие меню при ресайзе (если вдруг пользователь повернул устройство)
//     window.addEventListener('resize', () => {
//         if (window.innerWidth > 992) {
//             burgerBtn.classList.remove('active');
//             navContainer.classList.remove('active');
//             burgerBtn.setAttribute('aria-expanded', 'false');
//         }
//     });
// });
