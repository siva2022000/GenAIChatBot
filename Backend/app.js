const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const dotenv = require('dotenv');
const cors = require('cors');
const { default: axios } = require('axios');

dotenv.config();

const PORT = process.env.SERVER_PORT || 3000;

const app = express();
app.use(express.json());

const httpServer = http.createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: process.env.FRONTEND_HOST,
        methods: ["GET", "POST"]
    },
});


io.on('connection', (socket) => {
    socket.on('disconnect', () => {
    });

    socket.on('user_message', (message) => {
        axios.post(`${process.env.MACHINE_LEARNING_API_HOST}/extractanswer`, { question: message }).then((response)=>{
            socket.emit('bot_message', response.data.answer);
        }).catch((err)=>{
            // console.log(err);
            socket.emit('bot_message', "answer extraction failed");
        })
    });
});

httpServer.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

