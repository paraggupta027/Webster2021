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

let id=1;
let jobs=new Map();
let sockets = new Map();


const scheduleTask = (coin_symbol,price,socket_id)=>{
    console.log("scheduled");
    id++;
    let tp = "*/3 * * * * *";

	let name="JOB"+id;
    const job = schedule.scheduleJob(name,tp,async ()=>{
      let url="https://min-api.cryptocompare.com/data/price?fsym=" +  coin_symbol  +"&tsyms=USD";

      axios.get(url)
      .then(function (response) {
        let cur_price=response.data.USD;
        console.log(`price of ${coin_symbol} is ${cur_price} ---- order id: ${name}`);
        if(cur_price<=price)
        {
			job.cancel();
			console.log("Order executed "+name);
			io.to(sockets.get(job)).emit("executed",name);
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
	console.log("User Connected "+socket.handshake.query.email);	
	
    socket.on("schedule_task",(data)=>{
        console.log(socket.id);
        scheduleTask(data.coin,data.price,socket.id);
    })

    socket.on("remove_task",()=>{
    //   jobs.get("BTC").cancel();
    })
});


server.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
