// Execute on https://pvmonitor.pl/i_sprzet.php
const data = [...document.querySelector('#lkpomiary > div > table:nth-child(5)').querySelectorAll('tr')]
const entries = data.map(x => x.children).map(x => ({id: x[0].textContent, description: x[1].textContent, unit:x[2].textContent }))