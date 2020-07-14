function add(){
    $.post(addLink, {
        toDoItem : $("#todoitem").val()
    },
    function(data, status){         
        // alert("Data: " + data.note + "\nStatus: " + status);
        $(".list-items").append(
            '<li style="font-size: 30pt" class="mark" id="task" note_id="'+ data.note_id +'">' + data.note +' \
                    <input type="button" value="Complete"> \
                    <input type="button" value="Delete" class="delete">  \
                </li>'
        )
        });
};

$(document).on('click', '.delete' , function ()    { 
    $.post(deleteLink, {
        note_text : $(this).parent().text(),
        note_id : $(this).parent().attr("note_id")
    },
    function(data, status){        
        // alert("Data: " + data.done + "\nStatus: " + status);
        if (data.done == "yep")    {
            var item = "[note_id='"+ data.note_id + "']"
            document.querySelector(item).remove()
        }
        });
});