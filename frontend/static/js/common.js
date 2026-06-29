async function flashMessage(message) {
    console.log(`Flashing message ${message}`)
    const container = document.getElementById("flash-container");

    const msg = document.createElement("div");
    msg.className = "flash-message";
    msg.textContent = message;

    container.appendChild(msg);

    setTimeout(() => {
        msg.remove();
    }, 3000);
}

async function login() {
    event.preventDefault()

    var username = document.querySelector("#username").value;
    var password = document.querySelector("#password").value;

    response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "username": username,
            "password": password
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        window.location.replace("./admin-dashboard")
    }
    else {
        console.log(response_json)
        flashMessage(response_json.message)
    }
}