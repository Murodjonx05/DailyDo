(function() {
  const root = document.documentElement;
  const mql = window.matchMedia('(prefers-color-scheme: dark)');
  let currentListener = null;

  // Безопасное чтение/запись
  const storage = {
    get: () => { try { return localStorage.getItem('theme'); } catch(e){ return null; } },
    set: (v) => { try { localStorage.setItem('theme', v); } catch(e){} }
  };

  function updateActiveState(theme) {
    const dropdown = document.getElementById('THEME-DROPDOWN');
    if (!dropdown) return;
    const items = dropdown.querySelectorAll('a[data-theme]');
    items.forEach(el => {
      if (el.dataset.theme === theme) el.classList.add('active');
      else el.classList.remove('active');
    });
  }

  function handleAutoChange(e) {
    if (storage.get() === 'auto') {
      root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  }

  function setTheme(theme) {
    storage.set(theme);

    // Убираем старый слушатель, если был
    if (currentListener) {
      mql.removeEventListener('change', currentListener);
      currentListener = null;
    }

    if (theme === 'auto') {
      // При auto — ставим текущую системную и вешаем слушатель
      root.setAttribute('data-theme', mql.matches ? 'dark' : 'light');
      currentListener = handleAutoChange;
      mql.addEventListener('change', currentListener);
    } else {
      // Жесткая тема
      root.setAttribute('data-theme', theme);
    }

    updateActiveState(theme);
  }

  function init() {
    const saved = storage.get() || 'auto';

    // Восстанавливаем слушатель для auto, но НЕ переключаем тему,
    // если она уже выставлена criticalThemeLoad.js верно (чтобы избежать мерцания).
    // Но так как critical скрипт простой, мы тут можем просто вызвать setTheme,
    // чтобы привязать слушатели. Операция setAttribute идемпотентна, если значение то же.
    setTheme(saved);

    // Делегирование кликов
    const dropdown = document.getElementById('THEME-DROPDOWN');
    if (dropdown) {
      dropdown.addEventListener('click', (e) => {
        const link = e.target.closest('a[data-theme]');
        if (link) {
          e.preventDefault();
          setTheme(link.dataset.theme);
        }
      });
    }
  }

  // Запуск
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Экспорт
  window.setTheme = setTheme;
})();
