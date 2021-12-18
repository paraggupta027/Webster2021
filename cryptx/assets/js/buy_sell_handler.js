
$(document).ready(()=>{

    
    $("#buy_quantity").on('change',(e)=>{

        // console.log("hi");

        let qty = document.getElementById("buy_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
        document.getElementById("buy_price").value=total_price;
    
    })

    $("#sell_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("sell_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
        document.getElementById("sell_price").value=total_price;
    
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