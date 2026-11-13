// ! Markdown editor

// Tabs

async function showWriteTab() { // Shows the description textarea and hides the preview
    document.querySelector("#write-tab").classList.add("editor-tab-active")
    document.querySelector("#write-tab").setAttribute("aria-selected", "true")
    document.querySelector("#preview-tab").classList.remove("editor-tab-active")
    document.querySelector("#preview-tab").setAttribute("aria-selected", "false")

    document.querySelector("#description").classList.remove("editor-hidden")
    document.querySelector("#editor-preview").classList.add("editor-hidden")
}

async function showPreviewTab() { // Shows the description as it will look on the details page
    let description = document.querySelector("#description")
    let preview = document.querySelector("#editor-preview")

    document.querySelector("#preview-tab").classList.add("editor-tab-active")
    document.querySelector("#preview-tab").setAttribute("aria-selected", "true")
    document.querySelector("#write-tab").classList.remove("editor-tab-active")
    document.querySelector("#write-tab").setAttribute("aria-selected", "false")

    description.classList.add("editor-hidden") // Hidden rather than removed so the cursor and undo history are kept
    preview.classList.remove("editor-hidden")

    if (description.value == "") {
        let empty_message = document.createElement("p")
        empty_message.className = "muted-text"
        empty_message.textContent = "Nothing to preview"

        preview.textContent = ""
        preview.appendChild(empty_message)
    }
    else {
        response = await fetch("/api/render-markdown", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "text": description.value
            })
        })

        response_json = await response.json()

        if (response_json.code == 200) {
            preview.innerHTML = response_json.html // New syntax: .innerHTML - turns the HTML text from the server into elements inside the preview
            decorateCodeBlocks(preview) // Adds the language name and copy button to each code block (in details.js)
        }
        else {
            console.log(response_json)
            flashMessage(response_json.message)
        }
    }
}