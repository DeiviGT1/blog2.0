/* Brisa Sites - Interactividad: idioma, FAQ, animaciones */

(function() {
  // ─── LANGUAGE TOGGLE ──────────────────────────
  // Detect saved language or default to Spanish
  const savedLang = localStorage.getItem('brisa-lang');
  const initialLang = savedLang || 'es';
  document.documentElement.lang = initialLang;

  function toggleLanguage() {
    const current = document.documentElement.lang;
    const newLang = current === 'es' ? 'en' : 'es';
    document.documentElement.lang = newLang;
    localStorage.setItem('brisa-lang', newLang);
    updateToggleButton();
  }

  function updateToggleButton() {
    const buttons = document.querySelectorAll('.lang-toggle');
    const current = document.documentElement.lang;
    buttons.forEach(btn => {
      // Show the OTHER language as the action label
      btn.textContent = current === 'es' ? 'EN' : 'ES';
    });
  }

  // Wait for DOM ready
  document.addEventListener('DOMContentLoaded', function() {

    // Set up language toggle buttons
    const langButtons = document.querySelectorAll('.lang-toggle');
    langButtons.forEach(btn => {
      btn.addEventListener('click', toggleLanguage);
    });
    updateToggleButton();

    // ─── FAQ ACCORDION ───────────────────────────
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
      const question = item.querySelector('.faq-q');
      if (question) {
        question.addEventListener('click', () => {
          item.classList.toggle('open');
        });
      }
    });

    // ─── FADE-IN AL SCROLL ───────────────────────
    const fadeEls = document.querySelectorAll('.fade-in');

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.1,
        rootMargin: '0px 0px -60px 0px'
      });

      fadeEls.forEach(el => observer.observe(el));
    } else {
      fadeEls.forEach(el => el.classList.add('visible'));
    }

    // ─── SMOOTH SCROLL EN ANCLAS ─────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          const offset = 80;
          const targetPos = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top: targetPos, behavior: 'smooth' });
        }
      });
    });

  });
})();
