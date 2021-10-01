# online_tic_tac_toe

A new web version that adds lobbies and fixes the issues with this version is now up here https://murtada58.github.io/websockets_tic_tac_toe/

A simple online tic tac toe game made to learn a bit more about sockets and networking

The server has been deactivated for now do localhost if you want to try it

Currently this has only been made to work for 2 clients and the server will not work properly if the clients dont disconnect correctly (you need to close the pygame window instead of ctrl+C)

This also means that if you try to connect while 2 clients are already open it wont work, most likeley you will get an unresponsive black screen, as the server has been set to ignore extra connections for now

If a client disconnects mid play it could also cause issues with game state so both clients will have to disconnect and reconnect to reset the game state

A future version will be built with a lobby system and possibly secure authentiction when I learn a bit more about security

![demo](https://user-images.githubusercontent.com/36714364/135265725-d7f1c212-5348-40e3-8c42-ba017b821229.png)
