var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var produitId = this.dataset.produit
        var action = this.dataset.action
        console.log('produitId:', produitId, 'Action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
           addCookieItem(produitId, action)
        } else {
            updateUserOrder(produitId, action)
        }
    })
}

function addCookieItem(productId, action){
    console.log('User is not authenticated...')

    if (action == 'ajout'){
        if(panier[productId] == undefined){
            panier[productId] = {'quantite':1}
        }else{ 
            panier[productId]['quantite'] += 1
        }
    }
    if (action == 'retrait'){
            panier[productId]['quantite'] -= 1

            if (panier[productId][quantite] <= 0){
                console.log('Retrait')
                delete panier[productId]

            }
    }
    console.log('panier:', panier)
    document.cookie = 'panier=' + JSON.stringify(panier) + ";domain=;path=/"
    location.reload()

}

function updateUserOrder(produitId, action) {
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'produitId': produitId, 'action': action })
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}