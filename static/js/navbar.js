document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('main-navbar');

    // Account dropdown with cleanup
    const account = document.querySelector("nav .accounts");
    if (account) {
        const img = account.querySelector(".account-img");
        const accountController = new AbortController();

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
        }, { signal: accountController.signal });

        // Close on Escape
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") account.classList.remove("open");
        }, { signal: accountController.signal });

        // Store controller for potential cleanup
        account._dropdownController = accountController;
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

    // Mobile dropdown для логотипа - responsive initialization
    const logo = document.querySelector("nav .logo");
    let logoController = null;

    function setupMobileLogoDropdown() {
        if (!logo) return;

        const isMobile = window.innerWidth <= 768;
        const logoLink = logo.querySelector("a");

        // Remove existing listeners if switching modes
        if (logoController) {
            logoController.abort();
            logoController = null;
        }

        // Reset mobile state
        logo.classList.remove("mobile-open");

        if (isMobile && logoLink) {
            logoController = new AbortController();

            // Prevent default link behavior in mobile mode
            logoLink.addEventListener("click", (e) => {
                e.preventDefault();
                logo.classList.toggle("mobile-open");
            });

            // Close on click outside
            document.addEventListener("click", (e) => {
                if (!logo.contains(e.target)) {
                    logo.classList.remove("mobile-open");
                }
            }, { signal: logoController.signal });

            // Close on Escape
            document.addEventListener("keydown", (e) => {
                if (e.key === "Escape") logo.classList.remove("mobile-open");
            }, { signal: logoController.signal });
        }
    }

    // Initial setup
    setupMobileLogoDropdown();

    // Responsive setup on resize using matchMedia for better performance
    const mobileMediaQuery = window.matchMedia('(max-width: 768px)');
    mobileMediaQuery.addEventListener('change', setupMobileLogoDropdown);

    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    if (mobileToggle && navbar) {
        mobileToggle.addEventListener('click', () => {
            navbar.classList.toggle('nav-open');
        });
    }
});
