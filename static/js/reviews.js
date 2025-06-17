class ReviewsCarousel {
    currentSlide = 0;
    slides;
    dots;
    autoPlay=null;

    constructor() {
        this.slides = document.querySelectorAll('.review-item');
        this.dots = document.querySelectorAll('.dot');

        this.init();
    }

    init() {

        
        this.dots.forEach((dot, index) => {
            dot.addEventListener('click', () => this.goToSlide(index));
            dot.addEventListener('mouseenter', () => this.stopAutoPlay());
            dot.addEventListener('mouseleave', () => this.startAutoPlay());
        });

        
        this.startAutoPlay();

        
        const carousel = document.querySelector('.reviews-carousel');
        carousel?.addEventListener('mouseenter', () => this.stopAutoPlay());
        carousel?.addEventListener('mouseleave', () => this.startAutoPlay());
    }

    showSlide(index) {
        for (const slide of this.slides) {
            slide.classList.remove('active', 'prev');
        }
        for (const dot of this.dots) {
            dot.classList.remove('active');
        }

        
        this.slides[index]?.classList.add('active');
        this.dots[index]?.classList.add('active');

       
        const prevIndex = index === 0 ? this.slides.length - 1 : index - 1;
        this.slides[prevIndex]?.classList.add('prev');
    }

    goToSlide(index) {
        this.currentSlide = index;
        this.showSlide(this.currentSlide);
    }

    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.slides.length;
        this.showSlide(this.currentSlide);
    }

    startAutoPlay() {
        this.stopAutoPlay();
        this.autoPlayInterval = window.setInterval(() => {
            this.nextSlide();
        }, 4000);
    }

    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
}

document.addEventListener('DOMContentLoaded', ()=>new ReviewsCarousel())