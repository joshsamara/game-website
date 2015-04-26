function sendResponse(val){
    var pathname = window.location.pathname;
    $.post(pathname, {accept: val}, function(data) {
        window.location.href = data.url;
    });
}

function accept(){sendResponse(true);}
function decline(){sendResponse(true);}

$('#acceptBtn').click(accept);
$('#declineBtn').click(decline);
