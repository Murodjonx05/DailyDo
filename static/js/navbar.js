document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('main-navbar');

    // Simplified throttle function
    function throttle(func, delay) {
        let lastCall = 0;
        return function (...args) {
            const now = Date.now();
            if (now - lastCall >= delay) {
                lastCall = now;
                func.apply(this, args);
            }
        };
    }

    // Optimized dropdown handling using event delegation
    function handleDropdownClick(e) {
        const trigger = e.target.closest(".account-img, .accounts-icon-img");
        if (!trigger) return;

        const container = trigger.closest(".dropdown-container");
        if (!container) return;

        e.stopPropagation();

        // Close all dropdowns first
        document.querySelectorAll("nav .dropdown-container.open").forEach(openContainer => {
            openContainer.classList.remove("open");
        });

        // Toggle clicked dropdown
        container.classList.toggle("open");
    }

    // Single click listener for all dropdown triggers using event delegation
    document.addEventListener("click", handleDropdownClick);

    // Single click listener to close dropdowns when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".dropdown-container")) {
            document.querySelectorAll("nav .dropdown-container.open").forEach(container => {
                container.classList.remove("open");
            });
        }
    });

    // Single keydown listener for Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            document.querySelectorAll("nav .dropdown-container.open").forEach(container => {
                container.classList.remove("open");
            });
        }
    });

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

        const isMobile = window.innerWidth <= 1024;
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
    const mobileMediaQuery = window.matchMedia('(max-width: 1024px)');
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
