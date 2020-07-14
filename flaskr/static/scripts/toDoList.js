function add(){
    $.post(addLink, {
        toDoItem : $("#todoitem").val()
    },
    function(data, status){         
        alert("Data: " + data.note + "\nStatus: " + status);
        });
};

$('#task').on('click', function ()    {    
    $.post(deleteLink, {
        note_text : $(this).text(),
        note_id : $(this).attr("note_id")
    },
    function(data, status){         
        alert("Data: " + data.done + "\nStatus: " + status);
        });
});