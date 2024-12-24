const toggleDarkMode = () => {
    document.documentElement.classList.toggle('dark');
    console.log('Dark mode toggled')
};

document.querySelector('#darkModeToggle').addEventListener('click', toggleDarkMode)