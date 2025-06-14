// Массив с изображениями товара
const productImages = [
    '../img/dress1_sample.png',
    '../img/dress_sample.png',
    '../img/dress1_sample.png',
    '../img/dress_sample.png'
];

// Массив с описаниями к изображениям
const imageAltTexts = [
    'Платье пудрово-розовое - вид спереди',
    'Платье пудрово-розовое - вид сбоку',
    'Платье пудрово-розовое - деталь спины',
    'Платье пудрово-розовое - примерка'
];

let currentImageIndex = 0;
const mainImage = document.getElementById('mainImage');
const thumbnails = document.querySelectorAll('.thumbnail');

// Функция для смены изображения
function changeImage(index) {
    currentImageIndex = index;
    mainImage.src = productImages[index];
    mainImage.alt = imageAltTexts[index];

    // Обновляем активную миниатюру
    thumbnails.forEach((thumb, i) => {
        if (i === index) {
            thumb.classList.add('active');
        } else {
            thumb.classList.remove('active');
        }
    });
}

// Функция для перехода к предыдущему изображению
function prevImage() {
    currentImageIndex = (currentImageIndex - 1 + productImages.length) % productImages.length;
    changeImage(currentImageIndex);
}

// Функция для перехода к следующему изображению
function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % productImages.length;
    changeImage(currentImageIndex);
}

// Автопрокрутка изображений (опционально)
let slideInterval = setInterval(nextImage, 5000);

// Остановка автопрокрутки при наведении на изображение
document.querySelector('.main-image-container').addEventListener('mouseenter', () => {
    clearInterval(slideInterval);
});

// Возобновление автопрокрутки при уходе курсора
document.querySelector('.main-image-container').addEventListener('mouseleave', () => {
    slideInterval = setInterval(nextImage, 5000);
});
