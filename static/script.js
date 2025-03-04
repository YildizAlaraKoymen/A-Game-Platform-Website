
 function togglePassword(element) {
            const hiddenPassword = document.getElementById("password");
            if (hiddenPassword.dataset.shown === "true") {
                hiddenPassword.textContent = "******"; // Reset to stars
                hiddenPassword.dataset.shown = "false";
                element.textContent = "Show Password";
            } else {
                hiddenPassword.textContent = hiddenPassword.dataset.realPassword; // Reveal actual password
                hiddenPassword.dataset.shown = "true";
                element.textContent = "Hide Password";
            }
}

function changePassword() {
    const passwordSpan = document.getElementById("password");
    const passwordBox = document.getElementById("passwordBox");
    const saveButton = document.getElementById("saveButton");
    const showButton = document.getElementById("showPassword");

    const passwordBoxDisplay = window.getComputedStyle(passwordBox).display;

    if (passwordBoxDisplay === "none") {
        showButton.style.display = "none";
        passwordSpan.style.display = "none";
        passwordBox.style.display = "inline-block";
        saveButton.style.display = "inline-block";
    } else {
        showButton.style.display = "inline-block";
        passwordSpan.style.display = "inline-block";
        passwordBox.style.display = "none";
        saveButton.style.display = "none";
    }
}

function savePassword() {
    const passwordSpan = document.getElementById("password");
    const passwordBox = document.getElementById("passwordBox");
    const saveButton = document.getElementById("saveButton");

    const newPassword = passwordBox.value.trim();
    if (newPassword === "") {
        alert("Password cannot be empty.");
        return;
    }

    // Update the password span with dots based on the new password length
    passwordSpan.textContent = "*".repeat(newPassword.length);

    // Hide the input box and Save button, and show the password span
    passwordSpan.style.display = "inline-block";
    passwordBox.style.display = "none";
    saveButton.style.display = "none";

}