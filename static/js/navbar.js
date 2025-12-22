document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('main-navbar');

    // Utility function for throttling
    function throttle(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        return function (...args) {
            const currentTime = Date.now();

            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    }

    // Account dropdown with cleanup
    const account = document.querySelector("nav .accounts");
    if (account) {
        const img = account.querySelector(".account-img");
        if (img) {
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
    }

    // Scroll Effect with throttling
    if (navbar) {
        const throttledScrollHandler = throttle(() => {
            if (window.scrollY > 10) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }, 16); // ~60fps

        window.addEventListener('scroll', throttledScrollHandler);
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
                e.stopPropagation();
                logo.classList.toggle("mobile-open");
            }, { signal: logoController.signal });

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

    // Fallback: also listen to window resize as backup
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(setupMobileLogoDropdown, 100);
    });

    // Handle nav-links hover behavior for active state management
    const navLinks = document.querySelector('nav .nav-links');
    const linkHeaders = document.querySelectorAll('nav .nav-links .link-header');

    if (navLinks && linkHeaders.length > 0) {
        linkHeaders.forEach(header => {
            header.addEventListener('mouseenter', () => {
                // Reset active styling for all headers when hovering over any header
                linkHeaders.forEach(h => {
                    if (h !== header) {
                        h.classList.add('hover-reset-active');
                    }
                });
            });

            header.addEventListener('mouseleave', () => {
                // Restore active styling when not hovering
                linkHeaders.forEach(h => {
                    h.classList.remove('hover-reset-active');
                });
            });
        });
    }
});
