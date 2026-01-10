import { translateData } from './translate-data.js';

const Lang = {
    current: localStorage.getItem('lang') || 'uz',
    cache: {}, // Синхронизировано с critical.html

    loadCache() {
        try {
            const stored = JSON.parse(localStorage.getItem('lang_cache'));
            // Проверяем структуру: должна быть { "uz": { "widths": {...} }, "en": {...} }
            if (stored && typeof stored === 'object') {
                this.cache = stored;
            } else {
                this.cache = {};
            }
        } catch {
            this.cache = {};
        }
    },

    saveCache() {
        localStorage.setItem('lang_cache', JSON.stringify(this.cache));
    },

    apply() {
        const elements = document.querySelectorAll('[data-translate]');
        const lang = this.current;

        // Создаем ветку для языка, если её нет
        if (!this.cache[lang]) this.cache[lang] = { widths: {} };
        // На случай если структура старая
        if (!this.cache[lang].widths) this.cache[lang].widths = {};

        elements.forEach(el => {
            const key = el.dataset.translate;
            const text = translateData[key]?.[lang] || key;
            const len = text.length;

            // 1. Обновляем текст
            el.textContent = text;

            // 2. Умное обновление классов (чтобы не затирать другие стили)
            const otherClasses = el.className.replace(/\bch-\d+\b/g, '').trim();
            el.className = `${otherClasses} ch-${len}`.trim();

            // 3. Сохраняем ширину для Critical Path
            this.cache[lang].widths[key] = len;
        });

        this.saveCache();
        // Показываем контент: удаляем opacity: 0 и visibility: hidden
        document.body.classList.add('translated');
    },

    set(lang) {
        if (lang !== this.current) {
            this.current = lang;
            localStorage.setItem('lang', lang);
            this.apply();
        }
    },

    init() {
        if (!localStorage.getItem('lang')) {
            localStorage.setItem('lang', 'uz');
        }

        this.loadCache();
        this.apply();

        // Делегирование кликов (более надежно для динамических элементов)
        document.addEventListener('click', e => {
            const langBtn = e.target.closest('[data-lang]');
            if (langBtn) {
                e.preventDefault();
                this.set(langBtn.dataset.lang);
            }
        });
    }
};

// Запуск
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Lang.init());
} else {
    Lang.init();
}