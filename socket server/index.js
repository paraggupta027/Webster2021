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
let job_to_email = new Map();
let email_to_socket = new Map();

const COMPANY_EMAIL='s@gmail.com';


const scheduleTask = (order,email)=>{
    console.log("limit order scheduled");
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
        
        let email_for_job = job_to_email.get(job);
        let socket_for_email = email_to_socket.get(email_for_job);

        if(order.order_mode==1&&cur_price<=limit_price)
        {console.log(`price of ${coin_symbol} is ${cur_price} ---- order id: ${name} -----my buy price ${limit_price}`);
            job.cancel();
            console.log("Order executed "+name);
            io.to(socket_for_email).emit("executed",{order_id:name,price:cur_price});
        }
        if(order.order_mode==2&&cur_price>=limit_price)
        {console.log(`price of ${coin_symbol} is ${cur_price} ---- order id: ${name} -----my sell price ${limit_price}`);
            job.cancel();
            console.log("Order executed "+name);
            io.to(socket_for_email).emit("executed",{order_id:name,price:cur_price});
        }
        // sending data to company socket
        io.to(email_to_socket.get(COMPANY_EMAIL)).emit("executed",{order_id:name,price:cur_price});
      })
    });

  jobs.set(name,job);
	job_to_email.set(job,email);

}


const scheduleAlertTask = (data)=>{
  console.log("alert scheduled");
  let tp = "*/3 * * * * *";

  let coin_symbol=data.coin_symbol;
  let email=data.email;
  let price=data.price;
  let f=0;
  let last_price=0;

  const job = schedule.scheduleJob("alert",tp,async ()=>{
    let url="https://min-api.cryptocompare.com/data/price?fsym=" +  coin_symbol  +"&tsyms=USD";
    axios.get(url)
    .then(function (response) {
      let cur_price=response.data.USD;
      console.log(`price of ${coin_symbol} is ${cur_price} ---- but alert at ${price}`);
      
      let email_for_job = job_to_email.get(job);
      let socket_for_email = email_to_socket.get(email_for_job);

      if( (last_price<=price && price<=cur_price && f) || (last_price>=price && price>=cur_price && f) )
      {
          job.cancel();
          console.log("Alert executed");
          let msg = `${coin_symbol} reached ${price}`;
          io.to(socket_for_email).emit("alert",{msg:msg});
      }
      last_price=cur_price;
      f=1;

      })
  });

job_to_email.set(job,email);

}





io.on('connection',(socket)=>{

  socket.on('storeInfo',(data)=>{
    email_to_socket.set(data.email,socket.id);
    console.log("Stored info for ",data.email);
    let msg =`new user connected : ${data.email}`;
    io.to(email_to_socket.get(COMPANY_EMAIL)).emit("new-user",{msg:msg});

  })
	
    socket.on("schedule_limit_order",({order,email})=>{
        console.log(order);
        scheduleTask(order,email);
    })

    socket.on("set_price_alert",(data)=>{
      console.log(data);
      scheduleAlertTask(data);
  })
   
    socket.on("remove_task",()=>{
    //   jobs.get("BTC").cancel();
    })
});


server.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
