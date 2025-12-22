import { translateData } from './translate-data.js';

const Lang = {
    current: localStorage.getItem('lang') || 'uz',
    cache: null, // { lang: 'uz', texts: { plans: 'Rejalar', ... } }

    loadCache() {
        try {
            this.cache = JSON.parse(localStorage.getItem('lang_cache'));
        } catch {
            this.cache = null;
        }
    },

    saveCache(texts) {
        this.cache = { lang: this.current, texts };
        localStorage.setItem('lang_cache', JSON.stringify(this.cache));
    },

    apply() {
        const elements = document.querySelectorAll('[data-translate]');

        // If cache exists and language matches - use cached texts directly
        if (this.cache?.lang === this.current) {
            elements.forEach(el => {
                const key = el.dataset.translate;
                el.textContent = this.cache.texts[key] || key;
            });
            return;
        }

        // No cache or language changed - translate and cache
        const texts = {};
        elements.forEach(el => {
            const key = el.dataset.translate;
            const text = translateData[key]?.[this.current] || key;
            texts[key] = text;
            el.textContent = text;
        });
        this.saveCache(texts);
    },

    set(lang) {
        if (lang !== this.current) {
            localStorage.setItem('lang', this.current = lang);
            this.cache = null; // Invalidate cache
            this.apply();
        }
    },

    init() {
        if (!localStorage.getItem('lang')) {
            localStorage.setItem('lang', 'uz');
        }
        this.loadCache();
        this.apply();
        document.body.classList.add('translated'); // Show content
        document.querySelectorAll('[data-lang]').forEach(el => 
            el.addEventListener('click', e => (e.preventDefault(), this.set(el.dataset.lang)))
        );
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Lang.init(), { once: true });
} else {
    Lang.init();
}