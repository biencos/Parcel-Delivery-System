let notifications, deleteButton;
window.onload = function() {
    initializeFields();
}

function initializeFields() {
    notifications = document.getElementById("notifications");

    deleteButton = document.getElementById("delete-notifications");
    deleteButton.onclick = () => deleteNotifications();
    getNotifications()
}


function getNotifications() {
    fetch("/notifications").then(res => {
        if (res.status === 200) {
            res.json().then(obj => parseNotifications(obj['notifications']));
        }
        /* else {
                   alert("Coś poszło nie tak, Spróbuj ponownie później")
               } */
    });

    // Get new notifications
    DELAY = 1000
    setTimeout(getNotifications, DELAY);
}

function parseNotifications(ns) {
    noNotifications = document.getElementById("no-notifications");
    if (ns.length > 0) {
        // Hide No Notifications Text
        if (noNotifications.style.visibility === "visible") {
            noNotifications.style.visibility = "hidden";
        }

        ns.forEach(e => {
            let n = document.createElement('li');
            let it;

            if (e['new_status'] == 'w drodze')
                it = `Paczka zaadresowana do ${e['label_receiver']} właśnie wyruszyła w drogę!`;
            else if (e['new_status'] == 'odebrana')
                it = `Paczka zaadresowana do ${e['label_receiver']} właśnie została odebrana!`;
            else if (e['new_status'] == 'dostarczona')
                it = `Paczka zaadresowana do ${e['label_receiver']} została dostarczona!`;
            else
                it = '';

            n.innerText = it;
            notifications.insertBefore(n, notifications.firstChild);
        });
    } else {
        if (noNotifications.style.visibility === "hidden") {
            noNotifications.style.visibility = "visible";
        }
    }
}

function deleteNotifications() {
    if (notifications) {
        if (notifications.length > 0) {
            while (notifications.firstChild)
                notifications.removeChild(notifications.firstChild);
        } else
            alert("Na razie nie masz żadnych powiadomień do usunięcia!");
    } else
        alert("Na razie nie masz żadnych powiadomień do usunięcia!");
}