(function() {
  try {
    const saved = localStorage.getItem('theme');
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    const sysTheme = mql.matches ? 'dark' : 'light';

    // Если явно сохранено 'light' или 'dark', используем.
    // Если 'auto' или ничего нет (null) -> используем системную.
    if (saved === 'dark' || saved === 'light') {
      document.documentElement.setAttribute('data-theme', saved);
    } else {
      document.documentElement.setAttribute('data-theme', sysTheme);
    }
  } catch (e) {}
})();
