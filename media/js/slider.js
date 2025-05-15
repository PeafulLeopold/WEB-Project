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

    // Quantity selector functionality
    document.querySelectorAll('.quantity-selector').forEach(selector => {
        const minusBtn = selector.querySelector('.minus');
        const plusBtn = selector.querySelector('.plus');
        const quantityInput = selector.querySelector('.quantity-input');

        minusBtn.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            if (value > 1) {
                quantityInput.value = value - 1;
            }
        });

        plusBtn.addEventListener('click', () => {
            let value = parseInt(quantityInput.value);
            quantityInput.value = value + 1;
        });
    });
});