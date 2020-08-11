function addJq() {
    $.post(addLink, {
            toDoItem: $("#todoitem").val()
        },
        function(data, status) {
            if (data.done == "reload") {
                location.reload();
            }
            if (data.done == "yep") {
                $(".list-items").append(
                    '<li class="not-marked" id="task" note_id="' + data.note_id + '"><span class="completeJq todo-item">' + data.note + '</span> \
                        <div class="list-item-button-continer"> \
                        <input type="image" src="/static/img/checkmark.png" value="Complete" title="Toggle status" class="completeJq complete-button"> \
                        <input class="deleteJq eraser" type="image" src="/static/img/eraser.png" title="Delete" value="Delete"> \
                        </div>\
                    </li>')
            };
        });
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
                var item = "[note_id='" + data.note_id + "']"
                document.querySelector(item).remove()
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
                var item = "[note_id='" + data.note_id + "']"
                var temp_note = document.querySelector(item)
                if (temp_note.className == "not-marked") {
                    temp_note.className = "marked";
                } else {
                    temp_note.className = "not-marked";
                };
            };
        });
});

// not logged in scripts
function add() {
    $(".list-items").append(
            '<li class="not-marked" id="task"><span class="complete todo-item">' + $("#todoitem").val() + '</span> \
                <div class="list-item-button-continer"> \
                    <input type="image" src="/static/img/checkmark.png" value="Complete" class="complete complete-button" title="Toggle status"> \
                    <input class="delete eraser" type="image" src="/static/img/eraser.png" value="Delete" title="Delete"> \
                </div>\
        </li>')
        /*
            <input type="image" src='/static/img/checkmark.png' value="Complete" title="Toggle status" class="completeJq complete-button">
            <input class="deleteJq eraser" type="image" src='/static/img/eraser.png' title="Delete" value="Delete">
        */
};

$(document).on('click', '.delete', function() {
    $(this).parent().parent().remove()
});

$(document).on('click', '.complete', function() {
    if (($(this).attr('class').includes("complete-button"))) {
        $(this).parent().parent().toggleClass('marked');
        $(this).parent().parent().toggleClass('not-marked')
    } else {
        $(this).parent().toggleClass('marked');
        $(this).parent().toggleClass('not-marked')
    }
});