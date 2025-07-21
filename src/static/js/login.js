document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        const userId = form.user_id.value.trim();
        const password = form.password.value.trim();
        let errorMsg = '';

        if (!userId || !password) {
            errorMsg = 'Please fill in both fields.';
        }

        
        if (errorMsg) {
            let alertBox = document.createElement('div');
            alertBox.className = 'alert alert-danger alert-dismissible fade show mt-2';
            alertBox.role = 'alert';
            alertBox.innerHTML = `
                ${errorMsg}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            form.parentNode.insertBefore(alertBox, form);
            e.preventDefault();
        }
    });
});