function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(".button-minus").click(function(){
    let product_id = $(this).attr('data-id')
    $.ajax({
        type: "post",
        url: "/api/cart/minus/product/"+product_id+"/",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
    }).done(function(){
        location.reload();
    });
})


$(".button-plus").click(function(){
    let product_id = $(this).attr('data-id')
    $.ajax({
        type:"post",
        url: "/api/cart/plus/product/"+product_id+"/",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
    }).done(function(){
        location.reload();
    })
})