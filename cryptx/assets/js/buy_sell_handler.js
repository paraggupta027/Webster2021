

$(document).ready(()=>{
    
    $("#quantity").on('keyup',(e)=>{

        let qty = document.getElementById("quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
        document.getElementById("price").value=total_price;
    
    })


    $("#buy_form").on('submit',(e)=>{
        e.preventDefault();

        let form = $("#buy_form");
        let url = "/orders/handle_buy/";

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {
                alert(data.msg);
            },
            error: function (data) {
                alert('An error occurred.');
            },
        });
    })
    $("#sell_form").on('submit',(e)=>{
        e.preventDefault();

        let form = $("#sell_form");
        let url = "/orders/handle_sell/";

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {
                alert(data.msg);
            },
            error: function (data) {
                alert('An error occurred.');
            },
        });
    })
    

})