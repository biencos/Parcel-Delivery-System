let tableBody, addLabelForm, addLabelButton;
window.onload = function() {
    initializeFields();
}

function initializeFields() {
    tableBody = document.getElementById("table-body");
    addLabelForm = document.getElementById("add-label-form");
    addLabelButton = document.getElementById("add-label-button");
    receiverName = document.getElementById("receiver_name");
    parcelLockerId = document.getElementById("parcel_locker_id");
    packageSize = document.getElementById("package_size");

    addLabelButton.onclick = () => {
        addLabelButton.hidden = true;
        addLabel();
        addLabelButton.hidden = false;
    }
    getLabels();
}


function fillLabelsTable(labels) {
    resetTable(tableBody)

    labels.forEach(
        label => {
            const row = tableBody.insertRow(-1);

            for (k in label) {
                var td = document.createElement('td');
                var cellValue = document.createTextNode(label[k]);
                td.appendChild(cellValue);
                row.appendChild(td);
            }
            row.appendChild(createDeleteLabelButton(label));
            row.appendChild(createChangeLabelSentStatusButton(label));
        });
}

function resetTable(tb) {
    while (tb.children.length > 0)
        tb.deleteRow(0);
}

function createDeleteLabelButton(label) {
    var td = document.createElement('td');

    var deleteLabelButton = document.createElement('button');
    deleteLabelButton.id = label['label_id'];
    deleteLabelButton.innerText = "Usuń Etykietę";

    deleteLabelButton.onclick = e => {
        if (label['sent'] != "tak") {
            deleteLabelButton.hidden = true;
            deleteLabel(e);
        }
    }

    deleteLabelButton.classList.add("delete-label-button");

    td.appendChild(deleteLabelButton);
    return td
}



function createChangeLabelSentStatusButton(label) {
    var td = document.createElement('td');

    var changeLabelSentStatusButton = document.createElement('button');
    changeLabelSentStatusButton.id = label['label_id'];
    changeLabelSentStatusButton.innerText = "Nadaj/Cofnij";
    changeLabelSentStatusButton.onclick = e => {
        changeLabelSentStatusButton.hidden = true;
        changeLabelSentStatus(e);
        changeLabelSentStatusButton.hidden = false;

        /* (changeLabelSentStatusButton.hidden = true).then(
            fetch("/labels/" + e.target.id, { method: 'PUT' })).then(
            getLabels()).then(
            changeLabelSentStatusButton.hidden = false); */
    }
    changeLabelSentStatusButton.classList.add("change-label-sent-status-button");

    td.appendChild(changeLabelSentStatusButton);
    return td
}


function getLabels() {
    // Fill Table with Labels
    fetch("/labels").then(res => { res.json().then(obj => fillLabelsTable(obj['labels'])); })
}


function addLabel() {
    if (("" + receiverName.value).length > 0 && ("" + parcelLockerId.value).length > 0 && ("" + packageSize.value).length > 0) {
        let formData = new FormData(addLabelForm);
        fetch("/labels", { method: 'POST', body: formData }).then(res => {
            if (res.status === 201) {
                // Clear form
                addLabelForm.reset();
                // Update Table
                getLabels();
            }
        });
    } else
        alert("Nieprawidłowy format, Wypełnij poprawnie pola i spróbuj ponownie!");
}


function changeLabelSentStatus(e) {
    fetch("/labels/" + e.target.id, { method: 'PUT' }).then(getLabels());
}


function deleteLabel(e) {
    fetch("/labels/" + e.target.id, { method: 'DELETE' }).then(getLabels());
}