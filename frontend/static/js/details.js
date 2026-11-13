// ! Code blocks

const language_names = {
    "python": "Python",
    "ps1": "PowerShell",
    "powershell": "PowerShell",
    "pwsh": "PowerShell",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "cpp": "C++",
    "c++": "C++",
    "cs": "C#",
    "csharp": "C#",
    "c#": "C#",
    "sql": "SQL",
    "bash": "Bash",
    "sh": "Bash",
    "shell": "Bash",
    "json": "JSON",
    "yaml": "YAML",
    "yml": "YAML"
}

const copy_icon = `<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/></svg>`
const tick_icon = `<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>`

function decorateCodeBlocks(container) { // Adds a header with the language and a copy button to every code block in the container
    let code_blocks = container.querySelectorAll(".highlight")

    for (let i = 0; i < code_blocks.length; i++) {
        let code_block = code_blocks[i]
        let code = code_block.querySelector("code")

        if (code == null) { // Not a code block
            continue
        }

        if (code_block.querySelector(".code-header") !== null) { // Already has a header
            continue
        }

        let header = document.createElement("div")
        header.className = "code-header"

        let language = code.getAttribute("data-language") // New syntax: .getAttribute(name) - gets the value of an HTML attribute, or null if the element doesn't have it

        if (language == null) { // Blocks from before the language label was added
            language = "text"
        }

        if (language !== "text") { // No language was given, so no name is shown
            let language_label = document.createElement("span")

            if (language_names[language] !== undefined) {
                language_label.textContent = language_names[language]
            } else {
                language_label.textContent = language
            }

            header.appendChild(language_label)
        }

        let copy_button = document.createElement("button")
        copy_button.className = "copy-button"
        copy_button.type = "button"
        copy_button.title = "Copy code"
        copy_button.setAttribute("aria-label", "Copy code")
        copy_button.innerHTML = copy_icon
        copy_button.onclick = function () {
            copyCode(copy_button, code)
        }

        header.appendChild(copy_button)
        code_block.prepend(header) // New syntax: .prepend(element) - adds the element as the first thing inside code_block, so the header goes above the code
    }
}

async function copyCode(copy_button, code) { // Copies the code to the clipboard and shows a tick for 1.5 seconds
    await navigator.clipboard.writeText(code.textContent) // New syntax: navigator.clipboard.writeText(text) - copies the text to the clipboard

    copy_button.innerHTML = tick_icon
    copy_button.classList.add("copied")

    setTimeout(() => {
        copy_button.innerHTML = copy_icon
        copy_button.classList.remove("copied")
    }, 1500)
}

// ! Details page

function checkStickyPanel() { // Only keeps the info panel in place while scrolling if it fits in the window
    let panel = document.querySelector("#details-info-panel")

    if (panel.offsetHeight + 88 < window.innerHeight) {
        panel.classList.add("sticky-panel")
    } else {
        panel.classList.remove("sticky-panel")
    }
}

if (document.querySelector("#details-info-panel") !== null) { // Only run on the details page, as the project form loads this file too
    decorateCodeBlocks(document.querySelector("#details-description"))
    checkStickyPanel()
    window.onresize = checkStickyPanel
}