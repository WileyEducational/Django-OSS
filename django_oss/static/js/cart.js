var updateButtons = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateButtons.length;i++){
  updateButtons[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action

    if(user=== 'AnonymousUser'){
      // anonymous shopping is not integrated
      alert("anonymous shopping is not allowed, please log in.");
    }
    else{
      updateUserCart(productId, action)
    }
  })
  
}

function updateUserCart(productId, action){
  var url = '/update_cart/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'productId':productId, "action":action})
  })

  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    console.log('data:',data)
    location.reload()
    })
}
