function addJq() {
    if (document.getElementById('todoitem').value.trim() != "") {
        $.post(addLink, {
                toDoItem: $("#todoitem").val()
            },
            function(data, status) {
                if (data.done == "reload") {
                    location.reload();
                }
                if (data.done == "yep") {
                    $(".list-items").append(
                        '<li class="not-marked" id="task" note_id="' + data.note_id + '"><span class="completeJq todo-item" onmouseout="textHoverOut(this)">' + data.note + '</span> \
                        <div class="list-item-button-continer"> \
                        <input type="image" src="/static/img/checkmark.png" value="Complete" title="Toggle status" class="completeJq complete-button" onmouseover="completeHover(this)" onmouseout="buttonHoverOut(this)" onclick="buttonHoverOut(this)"> \
                        <input class="deleteJq eraser" type="image" src="/static/img/eraser.png" title="Delete" value="Delete" onmouseover="eraseHover(this)" onmouseout="buttonHoverOut(this)"> \
                        </div>\
                    </li>')
                };
            });
    }
    document.getElementById('todoitem').value = "";
    document.getElementById('todoitem').focus();
};

$(document).on('click', '.deleteJq', function() {
    $.post(deleteLink, {
            note_text: $(this).parent().parent().text(),
            note_id: $(this).parent().parent().attr("note_id")
        },
        function(data, status) {
            if (data.done == "reload") {
                location.reload();
            }
            if (data.done == "yep") {
                var item = "[note_id='" + data.note_id + "']";
                document.querySelector(item).remove();
            }
        });
});

$(document).on('click', '.completeJq, .completeJq-item', function() {
    if (($(this).attr('class').includes("complete-button"))) {
        data = {
            note_text: $(this).parent().parent().text(),
            note_id: $(this).parent().parent().attr("note_id")
        }
    } else {
        data = {
            note_text: $(this).parent().text(),
            note_id: $(this).parent().attr("note_id")
        }
    }
    $.post(completeLink, data,
        function(data, status) {
            if (data.done == "reload") {
                location.reload();
            }
            if (data.done == "yep") {
                var item = "[note_id='" + data.note_id + "']";
                var temp_note = document.querySelector(item);
                if (temp_note.className == "not-marked" || temp_note.className == "not-marked clicked") {
                    temp_note.className = "marked clicked";
                } else {
                    temp_note.className = "not-marked clicked";
                };
            };
        });
});

/* multi script */
var input = document.getElementsByClassName("todo-input")[0];
input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        document.getElementsByClassName("todo-input-pencil")[0].click();
    }
});

function eraseHover(e) {
    e.parentElement.previousElementSibling.style.textDecoration = 'line-through wavy 2.5px';
    e.parentElement.previousElementSibling.style.opacity = "50%";
}

function completeHover(e) {
    e.parentElement.previousElementSibling.style.textDecoration = 'line-through'
    if (e.parentElement.parentElement.getAttribute('class').includes('not-marked')) {
        e.parentElement.previousElementSibling.style.textDecorationColor = 'rgba(0, 0, 0, 0.65)';
    } else {
        e.parentElement.previousElementSibling.style.textDecorationColor = 'rgba(0, 0, 0, 0.35)';
    }
}

function buttonHoverOut(e) {
    e.parentElement.previousElementSibling.style.textDecoration = "";
    e.parentElement.previousElementSibling.style.opacity = "";
    e.parentElement.parentElement.classList.remove("clicked");
}

function textHoverOut(e) {
    e.parentElement.classList.remove("clicked");
}

// not logged in scripts
function add() {
    if (document.getElementById('todoitem').value.trim() != "") {
        $(".list-items").append(
            '<li class="not-marked" id="task"><span class="complete todo-item" onmouseout="textHoverOut(this)">' + $("#todoitem").val() + '</span> \
                    <div class="list-item-button-continer"> \
                        <input type="image" src="/static/img/checkmark.png" value="Complete" class="complete complete-button" title="Toggle status" onmouseover="completeHover(this)" onmouseout="buttonHoverOut(this)" onclick="buttonHoverOut(this)"> \
                        <input class="delete eraser" type="image" src="/static/img/eraser.png" value="Delete" title="Delete" onmouseover="eraseHover(this)" onmouseout="buttonHoverOut(this)"> \
                    </div>\
            </li>');
    }
    document.getElementById('todoitem').value = "";
    document.getElementById('todoitem').focus();
}

$(document).on('click', '.delete', function() {
    $(this).parent().parent().remove();
});

$(document).on('click', '.complete', function() {
    if (($(this).attr('class').includes("complete-button"))) {
        $(this).parent().parent().toggleClass('marked');
        $(this).parent().parent().toggleClass('not-marked');
        $(this).parent().parent().addClass('clicked');
    } else {
        $(this).parent().toggleClass('marked');
        $(this).parent().toggleClass('not-marked');
        $(this).parent().addClass('clicked');
    }
})