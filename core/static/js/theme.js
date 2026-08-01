const themeSwitch = document.getElementById('theme-switch');
const themeIndicator = document.getElementById('theme-indicator');

function applyTheme(theme) {
    document.body.classList.toggle('dark', theme === 'dark');
    themeIndicator.classList.toggle('icon-moon', theme === 'dark');
    themeIndicator.classList.toggle('icon-sun', theme !== 'dark');
    themeSwitch.checked = theme === 'dark';
    localStorage.setItem('theme', theme);
}

applyTheme(localStorage.getItem('theme') === 'dark' ? 'dark' : 'light');

themeSwitch.addEventListener('change', () => applyTheme(themeSwitch.checked ? 'dark' : 'light'));
