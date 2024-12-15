const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const dotenv = require('dotenv');
const cors = require('cors');

dotenv.config();

const PORT = process.env.SERVER_PORT || 3000;

const app = express();
app.use(express.json());

const httpServer = http.createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: "http://localhost:3000",
        methods: ["GET", "POST"]
    },
});


io.on('connection', (socket) => {
    socket.on('disconnect', () => {
    });

    socket.on('user_message', (message) => {
        socket.emit('bot_message', "Bot message for user message: " + message);
    });
});

httpServer.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

