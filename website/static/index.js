function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners to existing notes
  const notes = document.querySelectorAll(".note");
  notes.forEach((note) => {
    note.addEventListener("click", function () {
      makeEditable(this);
    });
  });
});

function makeEditable(noteElement) {
  // Create a textarea element
  const textarea = document.createElement("textarea");
  textarea.className = "note-editable form-control";
  textarea.value = noteElement.textContent.trim();

  // Replace the note element with the textarea
  noteElement.parentNode.replaceChild(textarea, noteElement);

  // Create a Save button
  const saveButton = document.createElement("button");
  saveButton.className = "btn btn-primary mt-2";
  saveButton.textContent = "Save";

  // Add event listener to save button
  saveButton.addEventListener("click", function () {
    updateNote(noteElement.dataset.noteId, textarea.value.trim());
  });

  // Append the Save button after the textarea
  textarea.insertAdjacentElement("afterend", saveButton);

  // Focus on the textarea
  textarea.focus();
}

function updateNote(noteId, newContent) {
  fetch("/update-note", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ noteId: noteId, newContent: newContent }),
  })
    .then((response) => {
      if (response.ok) {
        console.log("Note updated successfully");
        window.location.reload(); // Refresh the page after updating the note
      } else {
        console.error("Failed to update note");
      }
    })
    .catch((error) => {
      console.error("Network error:", error);
    });
}
