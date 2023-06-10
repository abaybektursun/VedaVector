document.getElementById("file-input").addEventListener("change", function() {
    var files = Array.from(this.files);
    var formData = new FormData();

    files.forEach(function(file) {
        formData.append("files", file);
    });

    // Send the files to the Flask backend
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
