
let socket;
const MARKET=1,LIMIT=2;

function show_toast(msg) {

    let new_toast = $(`<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                        <div id="toast_header" class="toast-header">
                            ${msg}
                        </div>
                        <div class="toast-body" style="color:red">
                        </div>
                    </div>`
                )

    $(".toast-container").prepend(new_toast);
    new_toast.toast('show');
}


$(document).ready(()=>{ 
    
    socket=io("http://localhost:5000",{query:`email=${email}`});

    socket.on('welcome',(data)=>{
        console.log(data.msg+" , socket connect krdia hai order karo...!!");
    })

    $("#scheduler").on('click',()=>{
        let coin=$("#coin").val();
        let price=$("#price").val();
        let data={coin,price};
        socket.emit("schedule_buy_limit_order",data);
      })
  
      $("#remove").on('click',()=>{
        socket.emit("remove_task");
      })
  
      socket.on("executed",(data)=>{
          let order_id=data.order_id;
          let msg=`Order executed with id : ${order_id}`;
          let url = "/orders/handle_limit_orders/";
          let sent = {
              'order_id' : order_id,
              'price' : data.price,
          } 
          console.log(data);
        $.ajax({
            type: 'GET',
            url: url,
            data: sent,
            success: function (data) {
              console.log(`${order_id} is executed`)
            },
            error: function (data) {
                show_toast('An error occurred.');
            },
        });
          show_toast(msg);
      })


    $("#buy_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("buy_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
        margin_required = document.getElementById("margin_required")
        console.log(margin_required.type)
        margin_required.innerHTML=total_price;
    
    })

    $("#sell_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("sell_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(2);
    
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

                let order = data.order;
                if(order.order_type==MARKET || data.success==0)
                {
                    // alert(data.msg);
                    let x = data.msg;
                    show_toast(x);
                    return;
                }
                console.log(order)
                socket.emit('schedule_buy_limit_order',order);                
            },
            error: function (data) {
                // alert('An error occurred.');
                show_toast("An error occured.");
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
                show_toast(data.msg);
            },
            error: function (data) {
                show_toast('An error occurred.');
            },
        });
    })

})