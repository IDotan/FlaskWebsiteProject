function addJq(){
    $.post(addLink, {
        toDoItem : $("#todoitem").val()
        },
        function(data, status){
            if (data.done == "reload"){
                location.reload();
            }
            if (data.done == "yep"){
                $(".list-items").append(
                    '<li class="not-marked" id="task" note_id="'+ data.note_id +'">' + data.note +' \
                        <input type="button" value="Complete" class="completeJq"> \
                        <input type="button" value="Delete" class="deleteJq">  \
                    </li>')};
        });
};

$(document).on('click', '.deleteJq' , function ()    { 
    $.post(deleteLink, {
        note_text : $(this).parent().text(),
        note_id : $(this).parent().attr("note_id")
        },
        function(data, status){   
            if (data.done == "reload"){
                location.reload();
            }
            if (data.done == "yep")    {
                var item = "[note_id='"+ data.note_id + "']"
                document.querySelector(item).remove()
            }
            });
});

$(document).on('click', '.completeJq' , function ()    {
    $.post(completeLink, {
        note_text : $(this).parent().text(),
        note_id : $(this).parent().attr("note_id")
        },
        function(data, status){   
            if (data.done == "reload"){
                location.reload();
                }
            if (data.done == "yep")    {
                var item = "[note_id='"+ data.note_id + "']"
                document.querySelector(item).className = "marked"
                }
            });
});

// not logged in scripts
function add(){
    $(".list-items").append(
        '<li class="not-marked" id="task">' + $("#todoitem").val() +' \
            <input type="button" value="Complete" class="Complete"> \
            <input type="button" value="Delete" class="delete">  \
        </li>')};

$(document).on('click', '.delete', function(){
    $(this).parent().remove()
});

$(document).on('click', '.Complete', function(){
    $(this).parent().addClass('marked');
    $(this).parent().removeClass('not-marked')
});