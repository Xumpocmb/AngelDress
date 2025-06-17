// Функционал вкладок
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            tabPanes.forEach(pane => pane.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
});

document.querySelectorAll('.size-option').forEach(option => {
    option.addEventListener('click', function () {
        document.querySelectorAll('.size-option').forEach(el => {
            el.classList.remove('active');
        });
        this.classList.add('active');
        this.querySelector('input[type="radio"]').checked = true;
    });
});
