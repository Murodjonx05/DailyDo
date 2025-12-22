(function() {
  function safeGet(k){ try{ return localStorage.getItem(k) } catch(e){ return null } }
  function safeSet(k,v){ try{ localStorage.setItem(k,v) } catch(e){} }

  const root = document.documentElement;
  const mql = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
  let mqlListener = null;

  function applyAuto() {
    root.dataset.theme = mql && mql.matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    if (theme === 'auto') {
      applyAuto();
      safeSet('theme','auto');

      if (mql && mqlListener) {
        try{ mql.removeEventListener('change', mqlListener) }
        catch(e){ try{ mql.removeListener(mqlListener) } catch(e){} }
      }
      mqlListener = e => { root.dataset.theme = e.matches ? 'dark' : 'light' };
      if (mql) {
        try{ mql.addEventListener('change', mqlListener) }
        catch(e){ try{ mql.addListener(mqlListener) } catch(e){} }
      }
    } else {
      root.dataset.theme = theme;
      safeSet('theme', theme);
      if (mql && mqlListener) {
        try{ mql.removeEventListener('change', mqlListener) }
        catch(e){ try{ mql.removeListener(mqlListener) } catch(e){} }
        mqlListener = null;
      }
    }

    // подсветка активного пункта меню
    const dropdown = document.getElementById('THEME-DROPDOWN');
    if (dropdown) {
      dropdown.querySelectorAll('a[data-theme]').forEach(a => {
        a.classList.toggle('active', a.getAttribute('data-theme') === theme);
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.getElementById('THEME-DROPDOWN');
    if (!dropdown) return;

    dropdown.addEventListener('click', function(e) {
      const a = e.target.closest && e.target.closest('a[data-theme]');
      if (!a) return;
      e.preventDefault();
      setTheme(a.getAttribute('data-theme'));
    });

    // при загрузке: берём сохранённое значение или auto по умолчанию
    setTheme(safeGet('theme') || 'auto');
  });

  window.setTheme = setTheme;
})();

