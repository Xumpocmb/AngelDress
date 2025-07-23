document.addEventListener('DOMContentLoaded', function () {
    const promoSlider = new Swiper('.promo-swiper', {
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: '.promo-button-next',
            prevEl: '.promo-button-prev',
        },
        pagination: {
            el: '.promo-pagination',
            clickable: true,
        },
    });
});