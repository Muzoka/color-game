# color-game

This is a simple 3D color battle game built with Firebase. To run locally you need a Firebase project and Firestore rules that allow access to the game documents.

The `firestore.rules` file in this repo grants open read/write permissions for the game's collection under:

```
artifacts/<appId>/public/data/color-wars-3d-games/{gameId}
```

Deploy these rules using `firebase deploy --only firestore` before playing with friends.
