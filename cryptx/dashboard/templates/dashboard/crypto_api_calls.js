const crypto = ["BTC", "LTC", "ETH", "NEO", "BNB", "QTUM", "EOS", "SNT"];
// let url="wss://stream.binance.com:9443/ws/ethusdt@trade";
let url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD";
let coin_name = "BTC"
let currency_name = "USD"
let time_stamp = Math.round(new Date().getTime() / 1000);

let history_url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=" +
    coin_name + "&tsym=" + currency_name + "&limit=2000" + "&toTs=" + time_stamp;
console.log(time_stamp)

let all_candles = [];

let reset = 0;
let chart;
let lineSeries;


$(document).ready(
    function() {

        var rateP = document.getElementById('rate');

        chart = LightweightCharts.createChart(document.getElementById('mychart'), {

        });
        lineSeries = chart.addLineSeries({
            drawCrosshairMarker: true,
            lineWidth: 2,
            color: 'black',
        });


        chart.applyOptions({
            title: 'DOGE',
            priceScale: {
                position: 'right',
                mode: 0,
                // autoScale: false,
                // invertScale: true,
                // alignLabels: true,
                borderVisible: true,
                borderColor: 'blackb',
                scaleMargins: {
                    top: 0.30,
                    bottom: 0.25,
                },
            },
            timeScale: {
                rightOffset: 12,
                barSpacing: 3,
                // fixLeftEdge: true,
                lockVisibleTimeRangeOnResize: true,
                rightBarStaysOnScroll: true,
                borderVisible: true,
                borderColor: 'black',
                visible: true,
                timeVisible: true,
                secondsVisible: false,
                tickMarkFormatter: (time, tickMarkType, locale) => {
                    console.log(time, tickMarkType, locale);
                    let date = new Date(time * 1000);
                    const year = date.getHours() + ":" + date.getMinutes();
                    return String(year);
                },
            },

            // timeScale: {
            //     rightOffset: 50,
            //     tickMarkFormatter: (time, tickMarkType, locale) => {
            // let date = new Date(time * 1000);
            // const year = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
            //         // console.log(year);

            //         return String(year);
            //     },
            // },
            crosshair: {
                vertLine: {
                    color: 'Black',
                    width: 1.7,
                    style: 1,
                    visible: true,
                    labelVisible: true,
                },
                horzLine: {
                    color: 'Black',
                    width: 1.7,
                    style: 1,
                    visible: true,
                    labelVisible: true,
                },
                mode: 0,
            },
        });
        var k = 2;
        async function add_history() {
            const response = await fetch(history_url);
            var dataRes = await response.json();
            var data = dataRes.Data.Data;
            // if(data)
            // data.reverse();
            // k--;
            // if(k==0)clearInterval(interval)
            if (data)
                for (let i = 0; i < data.length; i++) {
                    let candle = data[i];
                    var newDate = new Date();
                    var curtime = candle.time;
                    let newCandle = { time: curtime, value: candle.close };
                    all_candles.push(newCandle);
                    // console.log(all_candles.slice(-1));
                    // lineSeries.setData(all_candles);
                    // lineSeries.setData(newCandle)
                    // take++;
                }
            console.log(all_candles.length)
            console.log(time_stamp);
            time_stamp -= 2000 * 60;
            history_url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=" +
                coin_name + "&tsym=" + currency_name + "&limit=2000" + "&toTs=" + time_stamp;
            // console.log();

            //  all_candles.push(newCandle);
            console.log(all_candles);


        }
        // chart.timeScale().setVisibleRange({
        //     from: (new Date(Date.UTC(2021, 0, 1, 0, 0, 0, 0))).getTime() / 1000,
        //     to: (new Date(Date.UTC(2023, 1, 1, 0, 0, 0, 0))).getTime() / 1000,
        // });
        // var interval = setInterval(() => {
        //     add_history()

        // }, 100);
        setInterval(() => {
            addPoint();
        }, 1000);
        // setTimeout(()=>{
        //     lineSeries.setData(all_candles);
        // },1000)

    });








async function addPoint() {

    console.log(all_candles.length);

    const response = await fetch(url);
    var data = await response.json();

    console.log(data.USD);

    var newDate = new Date();
    var curtime = newDate.getTime() / 1000;
    let newCandle = { time: curtime, value: data.USD };

    // console.log(curtime);
    all_candles.push(newCandle);

    lineSeries.setData(all_candles);


}
