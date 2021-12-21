let portfolio=JSON.parse(document.getElementById('portfolio').textContent);

console.log(portfolio)


$(document).ready(function(){
    setInterval(() => {
        changeAllPrices();
    },200);
});

function changeAllPrices()
{
    portfolio.forEach(holding => {
        changeEachCoinPrice(holding);
    });
}

async function changeEachCoinPrice(holding) {
    
    let coin_name = holding.name;
    let coin_symbol = holding.symbol;
    let currency_name = "USD";
    let real_time_url = "https://min-api.cryptocompare.com/data/price?fsym=" +  coin_symbol  +"&tsyms="+currency_name;
    const response = await fetch(real_time_url);
    var data = await response.json();
    let current_price = data.USD;
    let quantity = holding.quantity
    let avg_price = holding.avg_price
    let total_pl = (current_price*quantity-avg_price*quantity).toFixed(2)
    let pl_id = "id_p&l_"+coin_symbol;
    let pl_container = document.getElementById(pl_id);
   

    if(total_pl>0)
    {
        pl_container.innerHTML="+"+ total_pl+'<span style="font-size:20px; font-weight:900;">&#8593;</span>';
        pl_container.style.color="green";
       
    }
    else if(total_pl<0)
    {
        pl_container.innerHTML=total_pl+'<span style="font-size:20px; font-weight:900;">&#8595;</span>';
        pl_container.style.color="red";
    }
}

