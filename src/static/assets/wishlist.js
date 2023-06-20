//const wishlistButton = document.querySelector(".btn-wishlist")
//
//
//
//
//wishlistButton.addEventListener("click", function(event) {
//    event.preventDefault()
//
//    const productId = this.dataset.product_id
//
//    fetch(
//        "/api/user/add/favorite/"+ productId + "/", {
//        method: 'GET',
//        headers:{
//            "Content-Type": "application/json"
//        }
//        }
//    ).then(response => {
//        if(response.ok){
//            return response.json()
//        } else {
//            alert(response.json()["message"])
//        }
//    }).catch(error => {
//        alert("Произошла ошибка!")
//    })
//
//})