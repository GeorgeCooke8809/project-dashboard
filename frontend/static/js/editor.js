// ! Markdown editor

const editor_pairs = { "*": "*", "_": "_", "`": "`", "\"": "\"", "(": ")", "[": "]" }
const editor_closers = ["*", "_", "`", "\"", ")", "]"]
const editor_doubles = ["*", "_", "`"] // Typing these again inside an empty pair doubles them (**|**)
const word_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

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