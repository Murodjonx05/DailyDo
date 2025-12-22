document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('main-navbar');
    const account = document.querySelector("nav .accounts");
    if (account) {
        const img = account.querySelector(".account-img");

        // Open/Close on click
        img.addEventListener("click", (e) => {
            e.stopPropagation();
            account.classList.toggle("open");
        });

        // Close on click outside
        document.addEventListener("click", (e) => {
            if (!account.contains(e.target)) {
                account.classList.remove("open");
            }
        });

        // Close on Escape
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") account.classList.remove("open");
        });
    }

    // Scroll Effect
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Mobile dropdown для логотипа
    const logo = document.querySelector("nav .logo");
    if (logo && window.innerWidth <= 768) {
        const logoLink = logo.querySelector("a");

        // Prevent default link behavior in mobile mode
        if (logoLink) {
            logoLink.addEventListener("click", (e) => {
                e.preventDefault();
                logo.classList.toggle("mobile-open");
            });
        }

        // Close on click outside
        document.addEventListener("click", (e) => {
            if (!logo.contains(e.target)) {
                logo.classList.remove("mobile-open");
            }
        });

        // Close on Escape
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") logo.classList.remove("mobile-open");
        });
    }

    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navbar.classList.toggle('nav-open');
        });
    }
});
