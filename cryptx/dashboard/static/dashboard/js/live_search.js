
let live_search_url = "/dashboard/live_search/";

$('#search').on('input',function(e){
    let val = $("#search").val();

    if(val.length>0){
        $.ajax({
            url : live_search_url,
            data : {'query':val},
            success:function(response)
            {
                var coin_list = response.coins;
                console.log(coin_list);
                
                var list = $("#search_result");
                list.empty();
                for(let i=0;i<coin_list.length;i++)
                {
                    var opt = "<option>"+coin_list[i]+"</option>";
                    // opt.attr('width',"100px");
                    list.append(opt);
                }

            }
        })
    }
});


let redirect_url="www.google.com"
$("#search_btn").on('click',function(e){
    var query = $("#search").val();
    var url="/dashboard/search/";
    if(query.length>0){
        $.ajax({
            url:url,
            data:{'query':query},
            success:function(response)
            {
                if(response.success==1)
                {
                    window.location=redirect_url;
                }
                else
                {
                    alert("no such coin");
                }
            }
        })
    }
});