// ! Markdown editor

const editor_pairs = { "*": "*", "_": "_", "`": "`", "\"": "\"", "(": ")", "[": "]" }
const editor_closers = ["*", "_", "`", "\"", ")", "]"]
const editor_doubles = ["*", "_", "`"] // Typing these again inside an empty pair doubles them (**|**)
const word_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

const editor_menu_items = [
    { "label": "Bold", "hint": "Ctrl+B", "action": () => wrapEditorSelection("**", "**", "bold text") },
    { "label": "Italic", "hint": "Ctrl+I", "action": () => wrapEditorSelection("*", "*", "italic text") },
    { "label": "Inline code", "hint": "`", "action": () => wrapEditorSelection("`", "`", "code") },
    { "label": "Link", "hint": "[ ]( )", "action": () => wrapEditorSelection("[", "](https://)", "link text") },
    { "divider": true },
    { "label": "Heading", "hint": "##", "action": () => insertEditorLine("## ") },
    { "label": "Bullet list", "hint": "-", "action": () => insertEditorLine("- ") },
    { "label": "Numbered list", "hint": "1.", "action": () => insertEditorLine("1. ") },
    { "label": "Checklist", "hint": "- [ ]", "action": () => insertEditorLine("- [ ] ") },
    { "label": "Quote", "hint": ">", "action": () => insertEditorLine("> ") },
    { "divider": true },
    { "label": "Table", "hint": "", "action": () => insertEditorBlock("| Column 1 | Column 2 |\n| --- | --- |\n| ", "Cell", " |  |") },
    { "label": "Code block", "hint": "```", "action": () => insertEditorBlock("```\n", "code", "\n```") },
    { "label": "Horizontal line", "hint": "---", "action": () => insertEditorBlock("---\n", "", "") }
]

// Editing helpers

function replaceEditorText(start, end, new_text) { // Replaces the description text between start and end in a way that Ctrl+Z can undo
    let area = document.querySelector("#description")

    area.focus() // New syntax: .focus() - puts the cursor back in the textarea so the change goes there
    area.selectionStart = start
    area.selectionEnd = end

    if (new_text !== "") {
        document.execCommand("insertText", false, new_text) // New syntax: execCommand("insertText") - types the text in as if from the keyboard, so Ctrl+Z can undo it
    }
    else if (start !== end) {
        document.execCommand("delete") // New syntax: execCommand("delete") - deletes the selected text as if Backspace was pressed, so Ctrl+Z can undo it
    }
}

function selectEditorText(start, end) { // Selects the description text between start and end
    let area = document.querySelector("#description")

    area.selectionStart = start
    area.selectionEnd = end
}

function wrapEditorSelection(before, after, placeholder) { // Puts before and after around the selected text, or around a selected placeholder if nothing is selected
    let area = document.querySelector("#description")
    let start = area.selectionStart
    let end = area.selectionEnd
    let selected = area.value.substr(start, end - start)

    if (selected == "") {
        selected = placeholder
    }

    replaceEditorText(start, end, before + selected + after)
    selectEditorText(start + before.length, start + before.length + selected.length)
}

// Auto-complete

function editorKeyDown() { // Auto-completes Markdown as it's typed, like Obsidian
    let area = document.querySelector("#description")
    let text = area.value
    let start = area.selectionStart
    let end = area.selectionEnd
    let key = event.key
    let previous = ""
    let before_previous = ""
    let next = text.substr(start, 1)

    if (start > 0) {
        previous = text.substr(start - 1, 1)
    }

    if (start > 1) {
        before_previous = text.substr(start - 2, 1)
    }

    let previous_is_word = previous !== "" && word_characters.includes(previous) // New syntax: && and || - JavaScript's "and" and "or"
    let in_empty_pair = start == end && previous !== "" && editor_pairs[previous] == next // e.g. (|) or *|* (New syntax: && and || - JavaScript's "and" and "or")
    let in_single_pair = in_empty_pair && before_previous !== previous && (before_previous == "" || word_characters.includes(before_previous) == false) // *|* but not **|** or **bold*|* (New syntax: && and || - JavaScript's "and" and "or")

    if (event.ctrlKey && (key == "b" || key == "B")) { // New syntax: && and || - JavaScript's "and" and "or"
        event.preventDefault()
        wrapEditorSelection("**", "**", "bold text")
    }
    else if (event.ctrlKey && (key == "i" || key == "I")) { // New syntax: && and || - JavaScript's "and" and "or"
        event.preventDefault()
        wrapEditorSelection("*", "*", "italic text")
    }
    else if (event.ctrlKey || event.altKey || event.metaKey) { // New syntax: && and || - JavaScript's "and" and "or"
        // Leave other shortcuts (copy, paste, undo...) to the browser
    }
    else if (editor_closers.includes(key) && start == end && next == key && (in_single_pair == false || editor_doubles.includes(key) == false)) { // The closing character is already there, so move past it (New syntax: && and || - JavaScript's "and" and "or")
        event.preventDefault()
        selectEditorText(start + 1, start + 1)
    }
    else if (editor_pairs[key] !== undefined && start !== end) { // Wrap the selected text in the pair (New syntax: && and || - JavaScript's "and" and "or")
        event.preventDefault()
        let selected = text.substr(start, end - start)

        replaceEditorText(start, end, key + selected + editor_pairs[key])
        selectEditorText(start + 1, end + 1)
    }
    else if (editor_pairs[key] !== undefined && (key == "(" || key == "[" || previous_is_word == false)) { // Add the closing half too (but not for * _ ` " in the middle of a word, e.g. snake_case) (New syntax: && and || - JavaScript's "and" and "or")
        event.preventDefault()

        replaceEditorText(start, end, key + editor_pairs[key])
        selectEditorText(start + 1, start + 1)
    }
    else if (key == " " && in_single_pair && (previous == "*" || previous == "_")) { // "* " starts a bullet point, so drop the closing * (New syntax: && and || - JavaScript's "and" and "or")
        event.preventDefault()

        replaceEditorText(start, start + 1, " ")
    }
    else if (key == "Backspace" && in_empty_pair) { // Delete both halves of an empty pair (New syntax: && and || - JavaScript's "and" and "or")
        event.preventDefault()

        replaceEditorText(start - 1, start + 1, "")
    }
    else if (key == "Enter" && start == end && event.shiftKey == false) { // New syntax: && and || - JavaScript's "and" and "or"
        continueEditorList(text, start)
    }
}

function continueEditorList(text, start) { // Starts the next list item when Enter is pressed on a list line, or ends the list on an empty item
    let line_start = text.lastIndexOf("\n", start - 1) + 1 // New syntax: .lastIndexOf() - like .indexOf() but searches backwards from the cursor, so this finds where the current line starts
    let line = text.substr(line_start, start - line_start)
    let indent = ""
    let marker = ""
    let next_marker = ""

    for (let i = 0; i < line.length && (line[i] == " " || line[i] == "\t"); i++) { // New syntax: && and || - JavaScript's "and" and "or"
        indent += line[i]
    }

    let rest = line.substr(indent.length)

    if (rest.indexOf("- [ ] ") == 0 || rest.indexOf("- [x] ") == 0) { // New syntax: && and || - JavaScript's "and" and "or"
        marker = rest.substr(0, 6)
        next_marker = "- [ ] "
    }
    else if (rest.indexOf("- ") == 0 || rest.indexOf("* ") == 0 || rest.indexOf("> ") == 0) { // New syntax: && and || - JavaScript's "and" and "or"
        marker = rest.substr(0, 2)
        next_marker = marker
    }
    else {
        let digits = ""

        for (let i = 0; i < rest.length && "0123456789".includes(rest[i]); i++) { // New syntax: && and || - JavaScript's "and" and "or"
            digits += rest[i]
        }

        if (digits !== "" && rest.substr(digits.length, 2) == ". ") { // New syntax: && and || - JavaScript's "and" and "or"
            marker = digits + ". "
            next_marker = (parseInt(digits) + 1) + ". " // New syntax: parseInt() - turns text like "3" into the number 3 so 1 can be added
        }
    }

    if (marker !== "") {
        event.preventDefault()

        if (rest == marker) { // Empty list item, so remove the marker and end the list
            replaceEditorText(line_start, start, "")
        }
        else {
            replaceEditorText(start, start, "\n" + indent + next_marker)
        }
    }
}

// Right-click menu

function insertEditorLine(marker) { // Adds the marker (e.g. "## " or "- ") to the start of the current line
    let area = document.querySelector("#description")
    let start = area.selectionStart
    let end = area.selectionEnd
    let line_start = area.value.lastIndexOf("\n", start - 1) + 1 // New syntax: .lastIndexOf() - like .indexOf() but searches backwards from the cursor, so this finds where the current line starts

    replaceEditorText(line_start, line_start, marker)
    selectEditorText(start + marker.length, end + marker.length)
}

function insertEditorBlock(before, placeholder, after) { // Inserts a table, code block or line on its own lines, with a blank line above it so the Markdown works
    let area = document.querySelector("#description")
    let start = area.selectionStart
    let end = area.selectionEnd
    let line_start = area.value.lastIndexOf("\n", start - 1) + 1 // New syntax: .lastIndexOf() - like .indexOf() but searches backwards from the cursor, so this finds where the current line starts
    let selected = area.value.substr(start, end - start)

    if (selected == "") {
        selected = placeholder
    }

    if (start > line_start) { // The cursor is part way through a line, so start a new paragraph
        before = "\n\n" + before
    }
    else if (line_start > 1 && area.value.substr(line_start - 2, 1) !== "\n") { // The line above has text on it, so leave a blank line (New syntax: && and || - JavaScript's "and" and "or")
        before = "\n" + before
    }

    replaceEditorText(start, end, before + selected + after)
    selectEditorText(start + before.length, start + before.length + selected.length)
}

function createEditorMenu() { // Builds the right-click menu from editor_menu_items and adds it to the page
    let cover = document.createElement("div")
    cover.id = "editor-menu-cover"
    cover.className = "editor-hidden"
    cover.setAttribute("onclick", "closeEditorMenu()")

    let menu = document.createElement("div")
    menu.id = "editor-menu"
    menu.className = "editor-hidden"
    menu.setAttribute("role", "menu")
    menu.setAttribute("aria-label", "Insert Markdown")
    menu.setAttribute("onkeydown", "editorMenuKeyDown()")

    for (let i = 0; i < editor_menu_items.length; i++) {
        if (editor_menu_items[i].divider == true) {
            let divider = document.createElement("div")
            divider.className = "editor-menu-divider"
            divider.setAttribute("role", "separator")
            menu.appendChild(divider)
        }
        else {
            let button = document.createElement("button")
            button.type = "button"
            button.className = "editor-menu-item"
            button.setAttribute("role", "menuitem")
            button.setAttribute("onclick", `runEditorMenuItem(${i})`)

            let label = document.createElement("span")
            label.textContent = editor_menu_items[i].label
            button.appendChild(label)

            let hint = document.createElement("span")
            hint.className = "editor-menu-hint"
            hint.textContent = editor_menu_items[i].hint
            button.appendChild(hint)

            menu.appendChild(button)
        }
    }

    document.body.appendChild(cover)
    document.body.appendChild(menu)
}

async function openEditorMenu() { // Opens the menu where the textarea was right-clicked (or long-pressed), kept inside the screen
    event.preventDefault()

    let menu = document.querySelector("#editor-menu")
    let x = event.clientX
    let y = event.clientY

    document.querySelector("#editor-menu-cover").classList.remove("editor-hidden")
    menu.classList.remove("editor-hidden")

    if (x + menu.offsetWidth > window.innerWidth - 8) {
        x = window.innerWidth - menu.offsetWidth - 8
    }

    if (y + menu.offsetHeight > window.innerHeight - 8) {
        y = window.innerHeight - menu.offsetHeight - 8
    }

    if (x < 8) {
        x = 8
    }

    if (y < 8) {
        y = 8
    }

    menu.style.left = `${x}px`
    menu.style.top = `${y}px`

    document.querySelector(".editor-menu-item").focus() // New syntax: .focus() - moves the keyboard focus to the first item so the arrow keys work straight away
}

async function closeEditorMenu() { // Hides the menu
    document.querySelector("#editor-menu-cover").classList.add("editor-hidden")
    document.querySelector("#editor-menu").classList.add("editor-hidden")
}

async function runEditorMenuItem(index) { // Closes the menu and does what the picked item says
    closeEditorMenu()
    editor_menu_items[index].action() // New syntax: .action() - runs the arrow function saved under "action" in editor_menu_items for this item
}

async function editorMenuKeyDown() { // Moves between menu items with the arrow keys, and closes the menu with Escape or Tab
    let items = document.querySelectorAll(".editor-menu-item")
    let current = 0

    for (let i = 0; i < items.length; i++) {
        if (items[i] == document.activeElement) {
            current = i
        }
    }

    if (event.key == "ArrowDown") {
        event.preventDefault()
        items[(current + 1) % items.length].focus() // New syntax: .focus() - moves the keyboard focus to the next item (% wraps round to the first)
    }
    else if (event.key == "ArrowUp") {
        event.preventDefault()
        items[(current - 1 + items.length) % items.length].focus() // New syntax: .focus() - moves the keyboard focus to the item above (% wraps round to the last)
    }
    else if (event.key == "Escape") {
        event.preventDefault()
        closeEditorMenu()
        document.querySelector("#description").focus() // New syntax: .focus() - puts the cursor back in the textarea
    }
    else if (event.key == "Tab") {
        closeEditorMenu()
    }
}

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

createEditorMenu() // Builds the menu when the page loads (this file is loaded with defer, so the page is ready by now)