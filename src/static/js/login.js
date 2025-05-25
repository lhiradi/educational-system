document.getElementById('loginForm').addEventListener('submit', function(e) {

    const userId = this.user_id.value.trim();
    const password = this.password.value.trim();
    if (!userId || !password) {
        alert('Please fill in both fields.');
        e.preventDefault();
    }
});