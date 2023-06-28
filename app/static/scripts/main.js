function replaceModalLink(content) {
    document.getElementById('modal-confirm-button').href = `/delete/${content}`;
}

// fieldList should be a 
function fillFormFields(fields) {
    for(let i = 0; i < Object.keys(fields).length; i++) {
        if (Object.keys(fields)[i] != "is_public") {
            document.getElementById(Object.keys(fields)[i]).value = Object.values(fields)[i];
        }
        if (Object.keys(fields)[i] == "is_public" && Object.values(fields)[i] == true) {
            document.getElementById(Object.keys(fields)[i]).checked = Object.values(fields)[i];
        }
    }
}