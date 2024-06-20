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
                if(response.status == 'login_required'){
                    swal('Title', 'subtitle', 'info')
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
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

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'Failed'){
                    console.log(response)
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                }

            }
        })
    })

});
