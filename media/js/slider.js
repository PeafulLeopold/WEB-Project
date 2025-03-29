document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelector('.slides');
    const slide = document.querySelectorAll('.slide');
    let currentIndex = 0;
  
    function showNextSlide() {
      currentIndex = (currentIndex + 1) % slide.length;
      const offset = -currentIndex * 100;
      slides.style.transform = `translateX(${offset}%)`;
    }
  
    setInterval(showNextSlide, 3000);
  });
  