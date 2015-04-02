var http = require('http');
var server = http.createServer().listen(8002);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var amqp = require('amqp');
var uuid = require('node-uuid');

// Connect to RabbitMQ
var connection = amqp.createConnection({ host: 'localhost' });
var exchange;

// Wait for connection to RabbitMQ become established.
connection.on('ready', function () {
    exchange = connection.exchange(
        'notifications',
        { noDeclare: true }
    );
});

// Declare the notifications socket.io namespace
var notifications = io.of('/notifications');
notifications.use(function(socket, next) {
    // Check for the django cookie
    if (socket.request.headers.cookie) {
        return next();
    } else {
        next(new Error('Authentication error'));
    }
});
notifications.on('connection', function (socket) {
    // Subscribe to the notifications queue
    var queue = connection.queue(
        'notifications-' + uuid.v1(),
        { 'autoDelete': true },
        function (q) {
            // Catch all messages with the routing key 'notifications' on the notifications exchange
            q.bind(exchange, 'notifications');

            // Receive messages
            q.subscribe(function (message) {
                socket.emit('notification', message);
            });
        }
    );

    socket.on('disconnect', function () {
        if (queue !== undefined || queue !== null) {
            queue.unbind(exchange, 'notifications');
        }
    });
});