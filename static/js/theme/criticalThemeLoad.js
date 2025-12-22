(function() {
  function safeGet(k){ try{ return localStorage.getItem(k) } catch(e){ return null } }
  function safeSet(k,v){ try{ localStorage.setItem(k,v) } catch(e){} }

  const root = document.documentElement;
  const mql = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');

  const stored = safeGet('theme');
  if (!stored) {
    // если нет сохранённого значения — используем системную тему и сохраняем auto
    const prefers = mql ? mql.matches : false;
    root.dataset.theme = prefers ? 'dark' : 'light';
    safeSet('theme', 'auto');

    // подписка на изменения системной темы
    if (mql) {
      mql.addEventListener('change', e => {
        root.dataset.theme = e.matches ? 'dark' : 'light';
      });
    }
  } else if (stored === 'auto') {
    // auto: вычисляем по системной теме и подписываемся на изменения
    root.dataset.theme = mql && mql.matches ? 'dark' : 'light';
    if (mql) {
      mql.addEventListener('change', e => {
        root.dataset.theme = e.matches ? 'dark' : 'light';
      });
    }
  } else {
    // явный выбор light/dark
    root.dataset.theme = stored;
  }
})();
