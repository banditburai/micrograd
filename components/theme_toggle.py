# theme_toggle.py

from fasthtml.common import *

fouc_script = Script("""
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
""")

dark_mode_toggle_script = """
    function toggleDarkMode() {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.theme = 'light';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        }
    }
"""

def ThemeToggle():
    return Div(
        Button(
            Img(src='assets/moon.svg', cls="w-6 h-6 dark:hidden"),
            Img(src='assets/sun.svg', cls="w-6 h-6 hidden dark:block"),
            id="theme-toggle",
            cls="p-2 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center",
            onclick="toggleDarkMode()",
        ),
        id="theme-toggle-wrapper",
        cls="flex items-center"
    )

def HamburgerMenu():
    return Label(
        Input(type="checkbox"),
        cls="hamburger-menu"
    )
