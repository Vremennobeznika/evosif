// Кнопка оплаты становится активной после двух отметок: согласие с офертой и согласие на обработку данных.
document.addEventListener('DOMContentLoaded', () => {
    const offer = document.getElementById('agreeOffer');
    const pd = document.getElementById('agreePd');
    const pay = document.getElementById('payBtn');
    if (!offer || !pd || !pay) return;

    function update() {
        const ok = offer.checked && pd.checked;
        pay.classList.toggle('is-disabled', !ok);
        pay.setAttribute('aria-disabled', ok ? 'false' : 'true');
        if (ok) {
            pay.setAttribute('href', pay.dataset.href);
            pay.removeAttribute('tabindex');
        } else {
            pay.removeAttribute('href');
            pay.setAttribute('tabindex', '-1');
        }
    }

    offer.addEventListener('change', update);
    pd.addEventListener('change', update);
    update();
});
