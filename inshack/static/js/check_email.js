function showError(containerParentNode, errorMessage) {
    containerParentNode.className = 'error';
    var spanElem = document.createElement('span');
    spanElem.className = "error-message";
    spanElem.innerHTML = errorMessage;
    containerParentNode.appendChild(spanElem);
}

function resetError(containerParentNode) {
    containerParentNode.className = '';
    if (containerParentNode.lastChild.className == "error-message") {
        containerParentNode.removeChild(containerParentNode.lastChild);
    }
}

function validate(form) {
    var elems = form.elements;
    var regEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/ ;
    
    if (!elems.email.value) {
        showError(elems.email.parentNode, 'Please enter your Email.');
        return false;
    } else if (!regEmail.test(elems.email.value)) {
        showError(elems.email.parentNode, 'Please enter a valid Email.');
        return false;
    }
    
    form.submit();
}