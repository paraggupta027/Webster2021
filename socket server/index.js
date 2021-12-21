const axios = require('axios');
const express = require('express')
const cors = require('cors')
const http = require('http');
const socketio = require('socket.io');

const schedule = require('node-schedule')


const app = express()
const port = 5000

const server = http.createServer(app);
const io = socketio(server);

app.use(cors())

app.use(express.json())

let jobs=new Map();
let sockets = new Map();


const scheduleTask = (order,socket_id)=>{
    console.log("scheduled");
    let tp = "*/3 * * * * *";

    let coin_symbol=order.coin_symbol;
    let limit_price=order.limit_price;

	  let name=(order.id).toString();
    const job = schedule.scheduleJob(name,tp,async ()=>{
      let url="https://min-api.cryptocompare.com/data/price?fsym=" +  coin_symbol  +"&tsyms=USD";

      axios.get(url)
      .then(function (response) {
        let cur_price=response.data.USD;
        console.log(`price of ${coin_symbol} is ${cur_price} ---- order id: ${name} -----my demand ${limit_price}`);

        if(order.order_mode==1&&cur_price<=limit_price)
        {
            job.cancel();
            console.log("Order executed "+name);
            io.to(sockets.get(job)).emit("executed",{order_id:name,price:cur_price});
        }
        if(order.order_mode==2&&cur_price>=limit_price)
        {
            job.cancel();
            console.log("Order executed "+name);
            io.to(sockets.get(job)).emit("executed",{order_id:name,price:cur_price});
        }
      })
    });
  jobs.set(name,job);
	sockets.set(job,socket_id);
}


io.use((socket, next) => {
	io.engine.generateId = () => {
	  return socket.handshake.query.email;
	}
	next(null, true);
});


io.on('connection',(socket)=>{
    socket.emit('welcome',{msg:"hello bhai"})
    console.log("User Connected "+socket.handshake.query.email);	
	
    socket.on("schedule_limit_order",(order)=>{
        // console.log(socket.id);
        console.log(order);
        scheduleTask(order,socket.id);
    })
   
    socket.on("remove_task",()=>{
    //   jobs.get("BTC").cancel();
    })
});


server.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
