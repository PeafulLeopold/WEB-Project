document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelector('.slides');
    const slideItems = document.querySelectorAll('.slide');
    let currentIndex = 0;
    const totalSlides = slideItems.length;

    function autoScroll() {
        currentIndex = (currentIndex + 1) % totalSlides;
        const offset = -currentIndex * 100;
        slides.style.transform = `translateX(${offset}%)`;
    }

    // Медленное автоматическое переключение каждые 8 секунд
    setInterval(autoScroll, 8000);
});