document.addEventListener('DOMContentLoaded', function () {
    const radioGroup = document.getElementById('price-option-group');
    if (radioGroup) {
        const radios = radioGroup.querySelectorAll('input[type="radio"]');
        radios.forEach(radio => {
            radio.addEventListener('change', function () {
                radioGroup.querySelectorAll('.radio-option').forEach(option => {
                    option.classList.remove('selected');
                });

                this.closest('.radio-option').classList.add('selected');

                const price = this.getAttribute('data-price');
                const pledge = this.getAttribute('data-pledge');
                const period = this.getAttribute('data-period');

                // Обновляем ОСНОВНУЮ цену
                const mainPriceSpan = document.getElementById('selected-main-price');
                if (mainPriceSpan) {
                    mainPriceSpan.textContent = price;
                }

                const pledgeContainer = document.getElementById('selected-pledge-container');
                const pledgeSpan = document.getElementById('selected-pledge');
                if (pledgeSpan && pledgeContainer) {
                    if (pledge && parseFloat(pledge) > 0) {
                        pledgeSpan.textContent = pledge;
                        pledgeContainer.style.display = 'block';
                    } else {
                        pledgeContainer.style.display = 'none';
                    }
                }

                const periodContainer = document.getElementById('selected-period-container');
                const periodSpan = document.getElementById('selected-period');
                if (periodSpan && periodContainer) {
                    if (period && parseInt(period) > 0) {
                        periodSpan.textContent = period;
                        periodContainer.style.display = 'block';
                    } else {
                        periodContainer.style.display = 'none';
                    }
                }
            });
        });

        const checkedRadio = radioGroup.querySelector('input[type="radio"]:checked');
        if (checkedRadio) {
            checkedRadio.closest('.radio-option').classList.add('selected');
        }
    }
});