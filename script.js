document.addEventListener("DOMContentLoaded", function () {
    // Emergency Activation Button
    document.querySelector(".emergency-section .button").addEventListener("click", function () {
        alert("Emergency Mode Activated! Authorities have been notified.");
    });

    // Live Location Sharing Button
    document.querySelector(".location .button").addEventListener("click", function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                alert("Location Shared: " + position.coords.latitude + ", " + position.coords.longitude);
            }, function () {
                alert("Error: Unable to retrieve location.");
            });
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    });

    // Form Submission
    document.querySelector("form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload
        alert("Report Submitted Successfully!");
    });
});


