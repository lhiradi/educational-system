function tableSearch(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    const trs = table.getElementsByTagName("tr");
    for (let i = 1; i < trs.length; i++) {
        let show = false;
        const tds = trs[i].getElementsByTagName("td");
        for (let j = 0; j < tds.length; j++) {
            if (tds[j].textContent.toLowerCase().indexOf(filter) > -1) {
                show = true;
                break;
            }
        }
        trs[i].style.display = show ? "" : "none";
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const flashContainer = document.getElementById('flash-messages');
    if (flashContainer) {
       
        const flashes = flashContainer.querySelectorAll('.flash');
        flashes.forEach(flash => {
            const closeBtn = document.createElement('span');
            closeBtn.className = 'flash-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cursor = 'pointer';
            closeBtn.style.marginLeft = '10px';
            closeBtn.style.fontWeight = 'bold';
            closeBtn.addEventListener('click', () => {
                flash.style.display = 'none';
            });
            flash.appendChild(closeBtn);

         
            setTimeout(() => {
                flash.style.transition = 'opacity 0.5s ease-out';
                flash.style.opacity = '0';
                setTimeout(() => {
                    flash.style.display = 'none';
                }, 500);
            }, 5000);
        });
    }
});
