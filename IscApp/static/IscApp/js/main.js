document.addEventListener('DOMContentLoaded', () => {
    console.log("ISC Goma homepage loaded");
    
    // Attach form submission handler for all forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            alert("Form submitted!");
        });
    });

    // Attach event handler for the signup button
    const signupButton = document.querySelector('.btn-signup');
    if (signupButton) {
        signupButton.addEventListener('click', handleSignup);
    }
});

// Function to handle signup form validation and actions
function handleSignup(event) {
    const username = document.querySelector('input[name="username"]').value.trim();
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;

    // Validate form inputs
    if (!username || !email || !password || !confirmPassword) {
        showAlert("All fields are required!", "error");
        event.preventDefault();
        return;
    }

    if (!validateEmail(email)) {
        showAlert("Please enter a valid email address.", "error");
        event.preventDefault();
        return;
    }

    if (password.length < 8) {
        showAlert("Password must be at least 8 characters long.", "error");
        event.preventDefault();
        return;
    }

    if (password !== confirmPassword) {
        showAlert("Passwords do not match!", "error");
        event.preventDefault();
        return;
    }

    showAlert("Account created successfully!", "success");
    // Here you can submit the form data to an API or perform other actions
}

// Function to display alert messages
function showAlert(message, type) {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
    document.body.appendChild(alertBox);

    setTimeout(() => {
        alertBox.remove();
    }, 3000); // Automatically remove the alert after 3 seconds
}

// Helper function to validate email format
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

  