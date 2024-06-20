$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        var data = {
            food_id: food_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+food_id).html(response.qty);
            }
        })
    })


    // place the cart item quantity on load
    $('.item_qty').each(function (){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#'+the_id).html(qty);
    });
});
