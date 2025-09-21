'use strict'
const btnScrollTo = document.querySelector('.btn--scroll-to');
const section1 = document.querySelector('#section--1');

btnScrollTo.addEventListener('click', function(e) {
    const s1Coords = section1.getBoundingClientRect();
    console.log(s1Coords);

    console.log(e.target.getBoundingClientRect())
     section1.scrollIntoView({ behavior: 'smooth' });

})
// Lazy Loading Images 
document.addEventListener('DOMContentLoaded', () => {
  // Select all images with the 'lazy-img' class
  const lazyImages = document.querySelectorAll('.lazy-img');

  // Function to load the image
  const loadLazyImage = (img) => {
    // Replace the placeholder src with the actual image URL from data-src
    img.src = img.dataset.src;

    // Once the image has finished loading, remove the blur effect
    img.addEventListener('load', () => {
      img.classList.remove('lazy-img'); // Or add a 'loaded' class
      img.classList.add('lazy-img-loaded');
    });
  };

  // Options for the observer (e.g., load image when it's 200px from the viewport)
  const observerOptions = {
    root: null, // observes intersections relative to the viewport
    rootMargin: '0px',
    threshold: 0.1 // Trigger when 10% of the image is visible
  };

  // Create the Intersection Observer
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      // If the image is intersecting the viewport
      if (entry.isIntersecting) {
        // Load the image
        loadLazyImage(entry.target);
        // Stop observing this image once it has been loaded
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Start observing each lazy image
  lazyImages.forEach(img => {
    observer.observe(img);
  });
});
// Slider
const slider = function () {
  const slides = document.querySelectorAll('.slide');
  const btnLeft = document.querySelector('.slider__btn--left');
  const btnRight = document.querySelector('.slider__btn--right');
  const dotContainer = document.querySelector('.dots');

  let curSlide = 0;
  const maxSlide = slides.length;

  // Functions
  const createDots = function () {
    slides.forEach(function (_, i) {
      dotContainer.insertAdjacentHTML(
        'beforeend',
        `<button class="dots__dot" data-slide="${i}"></button>`
      );
    });
  };

  const activateDot = function (slide) {
    document
      .querySelectorAll('.dots__dot')
      .forEach(dot => dot.classList.remove('dots__dot--active'));

    document
      .querySelector(`.dots__dot[data-slide="${slide}"]`)
      .classList.add('dots__dot--active');
  };

  const goToSlide = function (slide) {
    slides.forEach(
      (s, i) => (s.style.transform = `translateX(${100 * (i - slide)}%)`)
    );
  };

  // Next slide
  const nextSlide = function () {
    if (curSlide === maxSlide - 1) {
      curSlide = 0;
    } else {
      curSlide++;
    }

    goToSlide(curSlide);
    activateDot(curSlide);
  };

  const prevSlide = function () {
    if (curSlide === 0) {
      curSlide = maxSlide - 1;
    } else {
      curSlide--;
    }
    goToSlide(curSlide);
    activateDot(curSlide);
  };

  const init = function () {
    goToSlide(0);
    createDots();

    activateDot(0);
  };
  init();

  // Event handlers
  btnRight.addEventListener('click', nextSlide);
  btnLeft.addEventListener('click', prevSlide);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') prevSlide();
    e.key === 'ArrowRight' && nextSlide();
  });

  dotContainer.addEventListener('click', function (e) {
    if (e.target.classList.contains('dots__dot')) {
      const { slide } = e.target.dataset;
      goToSlide(slide);
      activateDot(slide);
    }
  });
};
slider();
