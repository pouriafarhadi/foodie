// JavaScript function to go back to the previous page
function goBack() {
    window.history.back();
}

$(document).ready(function(){
    // add food item
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');


        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status === 'login_required'){
                    Swal.fire({
                            title: 'Login credentials',
                            text: response.message,
                            icon: 'warning',
                            confirmButtonText: 'go to login page'
                        }).then(function () {
                        window.location = "/login";
                    })

                }else if (response.status === "Failed") {
                    Swal.fire({
                            title: 'Failed',
                            text: response.message,
                            icon: "error",
                            confirmButtonText: 'ok'
                        })
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // subtotal, tax and grandtotal
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grandtotal'],
                    )
                }

            }
        })
    })


    // place the cart item quantity on load
    $('.item_qty').each(function (){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#'+the_id).html(qty);
    });

    //decrease food item
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');
        var cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status === 'login_required'){
                    Swal.fire({
                            title: 'Login credentials',
                            text: response.message,
                            icon: 'warning',
                            confirmButtonText: 'go to login page'
                        }).then(function () {
                        window.location = "/login";
                    })

                }else if (response.status === "Failed") {
                    Swal.fire({
                            title: 'Failed',
                            text: response.message,
                            icon: "error",
                            confirmButtonText: 'ok'
                        })
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grandtotal'],
                    )
                    if(window.location.pathname === '/marketplace/cart/') {
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }

            }
        })
    })

    // Delete cart item
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        var cart_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if (response.status === "Failed") {
                    Swal.fire({
                            title: 'Failed',
                            text: response.message,
                            icon: "error",
                            confirmButtonText: 'ok'
                        })
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);

                    Swal.fire({
                            title: 'Success',
                            text: response.message,
                            icon: "success",
                            confirmButtonText: 'Great'
                        })
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grandtotal'],
                    )
                    removeCartItem(0, cart_id)
                    checkEmptyCart();
                }

            }
        })
    })

    // Delete the cart element if the qty is zero
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
           // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }
    
    // apply cart amounts
    function applyCartAmounts(subtotal, tax, grandtotal) {
        if(window.location.pathname === '/marketplace/cart/') {
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grandtotal)
        }
    }

    // add opening hour
    $('.add_hour').on('click', function (e) {
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value
        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else {
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }

        if(eval(condition)){
            $.ajax({
                type:'POST',
                url: url,
                data: {
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success:function (response){
                    if (response.status === 'success'){
                        console.log(url);
                        if (response.is_closed === "Closed"){
                         html = '<tr id="hour-'+response.id+'"><th><b>'+response.daay+'</b></th><td>Closed</td><td><a href="#" class="text-danger remove_hour" data-url="/vendor/opening_hours/remove/'+response.id+'/"><i class="bi bi-trash text-danger"> </i>Remove</a></td></tr>'

                        }else {
                         html = '<tr id="hour-'+response.id+'"><th><b>'+response.daay+'</b></th><td>'+response.from_hour+'-'+response.to_hour+'</td><td><a href="#" class="text-danger remove_hour" data-url="/vendor/opening_hours/remove/'+response.id+'/"><i class="bi bi-trash text-danger"> </i>Remove</a></td></tr>'
                        }
                        $(".opening_hours").append(html)
                        document.getElementById("opening_hours").reset()
                    }else {
                        Swal.fire({
                            title: 'Error',
                            text: response.message,
                            icon: "error",
                            confirmButtonText: 'try again!'
                        })
                    }
                }
            })
        }else {
            Swal.fire({
                        text: 'please fill all fields',
                        icon: "warning",
                        confirmButtonText: 'ok'
                    })
        }
    })
    $(document).on('click','.remove_hour', function (e) {
        e.preventDefault();
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success:function (response){
                if(response.status === 'success'){
                    document.getElementById('hour-' + response.id).remove()

                }
            }

        })

    })
});
