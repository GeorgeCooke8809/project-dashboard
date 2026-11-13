async function flashMessage(message) {
    console.log(`Flashing message ${message}`)
    const container = document.getElementById("flash-container");

    const msg = document.createElement("div");
    msg.className = "flash-message";
    msg.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="7" x2="12" y2="13"/><circle class="flash-icon-dot" cx="12" cy="17" r="1.3"/></svg>` // New syntax: .innerHTML - turns the text into HTML elements inside msg (used for the "!" icon)

    const text = document.createElement("span")
    text.textContent = message
    msg.appendChild(text)

    container.appendChild(msg);

    setTimeout(() => {
        msg.remove();
    }, 3000);
}

async function login() {
    event.preventDefault()

    var username = document.querySelector("#username").value;
    var password = document.querySelector("#password").value;

    response = await fetch("/api/login", {
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
    var description = document.querySelector("#description").value
    var created = document.querySelector("#created").value;
    var updated = document.querySelector("#updated").value;

    response = await fetch("/api/add-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "title": title,
            "url": url,
            "description": description,
            "created": created,
            "updated": updated
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        if (add_again == true) {
            document.querySelector("#title").value = "";
            document.querySelector("#url").value = "";
            document.querySelector("#description").value = ""
            showWriteTab()
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

async function archiveProject(id) {
    response = await fetch("/api/archive-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "id": id
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

async function restoreProject(id) {
    response = await fetch("/api/restore-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "id": id
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        window.location.replace("./inactive-projects")
    }
    else {
        console.log(response_json)
        flashMessage(response_json.message)
    }
}

async function editProject(id) {
    event.preventDefault()

    var title = document.querySelector("#title").value;
    var url = document.querySelector("#url").value;
    var description = document.querySelector("#description").value
    var created = document.querySelector("#created").value;
    var updated = document.querySelector("#updated").value;

    response = await fetch("/api/edit-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            "id": id,
            "title": title,
            "url": url,
            "description": description,
            "created": created,
            "updated": updated
        })
    })

    response_json = await response.json()

    if (response_json.code == 200) {
        window.location.replace("/admin-dashboard")
    }
    else {
        console.log(response_json)
        flashMessage(response_json.message)
    }
}

function setTodays() {
    let today = new Date().toISOString().substr(0, 10);
    document.querySelectorAll(".today").value = today;
}

// ! AI collaboration rating

const ai_collaboration_names = ["No AI", "A little AI help", "Some AI help", "Half AI", "Mostly AI", "Vibe coded"]

function showAiCollaborationName() { // Shows the name of the current rating under the boxes
    let rating = document.querySelectorAll("#ai-rating .ai-rating-filled").length // The rating is the number of filled in boxes

    document.querySelector("#ai-rating-name").textContent = `${rating}/5 · ${ai_collaboration_names[rating]}`
}

function setAiCollaboration(rating) { // Fills in the boxes up to the one clicked, or clears them all if the current rating is clicked again
    let current_rating = document.querySelectorAll("#ai-rating .ai-rating-filled").length

    if (rating == current_rating) {
        rating = 0
    }

    let boxes = document.querySelectorAll("#ai-rating .ai-rating-box")

    for (let i = 0; i < boxes.length; i++) {
        if (i < rating) {
            boxes[i].classList.add("ai-rating-filled")
        } else {
            boxes[i].classList.remove("ai-rating-filled")
        }
    }

    showAiCollaborationName()
}

if (document.querySelector("#ai-rating") !== null) { // Only on pages that show the rating
    showAiCollaborationName()
}