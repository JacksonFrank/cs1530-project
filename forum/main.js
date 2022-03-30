function showCommentArea(){
    let commentArea = document.getElementById("comment_area");
    commentArea.setAttribute("style", "display:block;");
}
function hideCommentArea(){
    let commentArea = document.getElementById("comment_area");
    commentArea.setAttribute("style", "display:none;");
}

function showReply(){
    let reply = document.getElementsById("comment_container");
    reply.setAttribute("style", "display:block;");
}