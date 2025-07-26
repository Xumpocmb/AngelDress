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
        roundLengths: true,
        pagination: {
            el: '.promo-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.promo-button-next',
            prevEl: '.promo-button-prev',
        },
    });
});
