// CSRF Token Setup
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Increase Quantity
document.querySelectorAll('.increase-quantity').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default form submission
        const name = this.getAttribute('data-name');
        fetch(`/update-quantity/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ id: name, action: 'increase' }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`quantity-${name}`).textContent = data.new_quantity;
                document.getElementById(`price-${name}`).textContent = data.new_price;
            })
            .catch(error => console.error('Error:', error));
    });
});

// Decrease Quantity
document.querySelectorAll('.decrease-quantity').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default form submission
        const name = this.getAttribute('data-name');
        fetch(`/update-quantity/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ id: name, action: 'decrease' }),
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`quantity-${name}`).textContent = data.new_quantity;
                document.getElementById(`price-${name}`).textContent = data.new_price;
            })
            .catch(error => console.error('Error:', error));
    });
});

// Delete Row
document.querySelectorAll('.delete-row').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        const name = this.getAttribute('data-name');
        fetch(`/delete-product/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ id: name }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`row-${name}`).remove();
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
