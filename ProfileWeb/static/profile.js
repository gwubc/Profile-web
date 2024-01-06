function displayMessage(msg) {
    console.log(msg)
    const messageWindow = document.getElementById("messageWindow");
    messageWindow.innerHTML = msg;
    messageWindow.style.display = "block";
}

document.getElementById('introduction_form').onsubmit = function update_introduction(event) {
    event.preventDefault();
    fetch('/update_introduction', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "introduction": document.getElementById('introduction').value
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                displayMessage(data.message);
            }
        })
        .catch(error => {
            displayMessage(error.message);
        });
}