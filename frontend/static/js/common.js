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

async function addProject() {
    event.preventDefault()

    var title = document.querySelector("#title").value;
    var url = document.querySelector("#url").value;
    var add_again = document.querySelector("#add-another").checked;
    var description = document.querySelector("#description-area").value;

    response = await fetch("/api/add-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "title": title,
            "url": url,
            "description": description
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        if (add_again == true) {
            document.querySelector("#title").value = "";
            document.querySelector("#url").value = "";
            document.querySelector("#description-area").value = "";
        }
        else {
            window.location.replace("/admin-dashboard")
        }
    }
    else {
        console.log(response_json)
        flashMessage(response_json.message)
    }
}