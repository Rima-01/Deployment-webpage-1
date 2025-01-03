// Base URL for API Endpoints
const API_BASE_URL = "http://54.211.211.195:8000/api"; // Replace with your backend URL

// Utility function to handle errors
const handleError = (error, errorElement) => {
    console.error("Error:", error);
    errorElement.innerText = "Failed to connect to the server. Please try again.";
};

// Sign Up functionality
const initializeSignup = () => {
    const signupBtn = document.getElementById('signup-btn');
    if (signupBtn) {
        signupBtn.addEventListener('click', async () => {
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;

            const signupError = document.getElementById('signup-error');
            const signupSuccess = document.getElementById('signup-success');

            signupError.innerText = '';
            signupSuccess.innerText = '';

            try {
                const response = await fetch(`${API_BASE_URL}/signup/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    signupSuccess.innerText = data.message || 'User created successfully.';
                } else {
                    signupError.innerText = data.error || 'Signup failed.';
                }
            } catch (error) {
                handleError(error, signupError);
            }
        });
    }
};

// Login functionality
const initializeLogin = () => {
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', async () => {
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            const loginError = document.getElementById('login-error');
            const loginSuccess = document.getElementById('login-success');

            loginError.innerText = '';
            loginSuccess.innerText = '';

            try {
                const response = await fetch(`${API_BASE_URL}/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    loginSuccess.innerText = data.message || 'Login successful.';
                    setTimeout(() => {
                        // Redirect to posters.html on successful login
                        window.location.href = "posters.html";
                    }, 2000);
                } else {
                    loginError.innerText = data.error || 'Login failed.';
                }
            } catch (error) {
                handleError(error, loginError);
            }
        });
    }
};

// Initialize functionality based on the current page
document.addEventListener('DOMContentLoaded', () => {
    initializeSignup();
    initializeLogin();
});
