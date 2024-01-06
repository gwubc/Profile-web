function displayMessage(msg) {
    console.log(msg)
    const messageWindow = document.getElementById("messageWindow");
    messageWindow.innerHTML = msg;
    if (msg.trim() !== "") {
        messageWindow.style.display = "block";
    } else {
        messageWindow.style.display = "none";
    }
}

function showForm(formId) {
    ['login', 'register'].forEach(function (id) {
        document.getElementById(id).classList.remove('active');
        document.getElementById(id + 'Form').classList.remove('active');
    });
    displayMessage("");
    document.getElementById(formId).classList.add('active');
    document.getElementById(formId + 'Form').classList.add('active');
}



document.getElementById('showRegister').onclick = function showRegister(event) {
    event.preventDefault();
    showForm("register");
}
document.getElementById('showLogin').onclick = function showLogin(event) {
    event.preventDefault();
    showForm("login");
}

document.getElementById('loginForm').onsubmit = function login(event) {
    event.preventDefault();
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: document.getElementById("loginUsername").value,
            password: document.getElementById("loginPassword").value
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data["next"];
            } else {
                displayMessage(data.message);
            }
        })
        .catch(error => {
            displayMessage(error.message);
        });
}

document.getElementById('registerForm').onsubmit = function register(event) {
    event.preventDefault();
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: document.getElementById("registerUsername").value,
            password: document.getElementById("registerPassword").value
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data["next"];
            } else {
                displayMessage(data.message);
            }
        })
        .catch(error => {
            displayMessage(error.message);
        });
}