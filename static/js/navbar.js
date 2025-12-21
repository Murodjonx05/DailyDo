document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('main-navbar');

    // Scroll Effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile Menu (Simple implementation matching CSS classes)
    const mobileToggle = document.querySelector('.mobile-toggle');
    // Note: Full mobile implementation assumes HTML structure exists.
    // This is a placeholder to ensure the file exists and basic listeners are ready.
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            // Toggle logic here
            console.log('Mobile toggle clicked');
        });
    }
});
