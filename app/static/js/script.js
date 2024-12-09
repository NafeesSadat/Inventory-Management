document.addEventListener('DOMContentLoaded', function() {
    // Example: Add event listeners or other JavaScript functionality
    console.log('Document is ready');

    // Add dynamic behavior to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const action = form.getAttribute('action') || window.location.href;
            const method = form.getAttribute('method') || 'POST';

            fetch(action, {
                method: method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Form submitted successfully!');
                    window.location.reload();
                } else {
                    alert('Form submission failed: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Form submission failed: ' + error.message);
            });
        });
    });

    // Add dynamic behavior to table rows
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            const itemId = this.getAttribute('data-id');
            window.location.href = `/inventory/update/${itemId}`;
        });
    });
});