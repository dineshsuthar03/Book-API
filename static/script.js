// JavaScript for API interactions
async function fetchBooks() {
    const response = await fetch('/api/books');
    const books = await response.json();
    console.log(books);
}

// Function to register a new user
async function registerUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
        alert('Registration successful!');
        location.href = '/login';
    } else {
        alert('Registration failed.');
    }
}

// Assuming login function fetches the token upon successful login
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.token); // Store token
        alert('Login successful!');
        window.location.href = '/books'; // Redirect to books page
    } else {
        alert('Invalid credentials.');
    }
}