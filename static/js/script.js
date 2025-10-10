// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        alerts.forEach(function(alert) {
            setTimeout(function() {
                // Bootstrap's own dismiss functionality is better.
                // If you have a close button with data-dismiss="alert", it will work.
                // This is a fallback.
                alert.style.display = 'none';
            }, 5000);
        });
    }

    // অন্য কোনো JavaScript কোডের প্রয়োজন নেই।
    // Bootstrap ড্রপডাউন এবং মোবাইল নেভিগেশন নিজে থেকেই পরিচালনা করে।
});
