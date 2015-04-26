function invite(val){
    var group_id = $("#groupSelect").val();
    var user_id = $("#userId").val();
    var pathname = baseURL + "groups/" + group_id + "/join/";
    $.post(pathname, {user: user_id}, function(data) {
        window.location.reload();
    });
}


$('#inviteBtn').click(invite);
