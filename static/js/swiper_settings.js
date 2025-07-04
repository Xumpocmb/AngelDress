document.addEventListener('DOMContentLoaded', function () {
            new Swiper('.swiper', {
                loop: true,
                centeredSlides: true,
                slidesPerView: 1,
                spaceBetween: 0,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                roundLengths: true, // Точные расчёты ширины
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
            });
        });
