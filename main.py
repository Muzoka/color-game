<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حرب الألوان 3D</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; touch-action: manipulation; overflow: hidden; }
        #canvas-container { width: 100%; height: 60vh; max-height: 550px; cursor: pointer; border: 2px solid #4a5568; border-radius: 0.5rem; margin: auto; background-color: #1f2937; }
        canvas { display: block; }
        .color-box { width: 2rem; height: 2rem; border: 2px solid white; transition: transform 0.2s; }
        .color-box.selected { transform: scale(1.2); border: 3px solid #6366F1; }
        .btn-primary { @apply bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-colors duration-300 disabled:bg-gray-600 disabled:text-gray-400 disabled:cursor-not-allowed; }
        .card { @apply bg-gray-800 p-6 rounded-xl shadow-2xl border border-gray-700; }
        .player-list-item { @apply flex items-center gap-3 p-2 bg-gray-700 rounded-md; }
        .input-field { @apply text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5 text-center; }
    </style>
</head>
<body class="bg-gray-900 text-white flex items-center justify-center min-h-screen">

    <div id="app" class="container mx-auto p-4 max-w-4xl text-center">

        <div id="game-setup" class="card">
            <h1 class="text-4xl font-bold mb-2 text-indigo-400">حرب الألوان 3D</h1>
            <p class="text-gray-400 mb-6">سيطر على المكعبات بلونك الخاص!</p>
            
            <div class="mb-4 max-w-sm mx-auto">
                <label for="player-name-input" class="block mb-2 text-sm font-medium text-gray-300">اسمك في اللعبة</label>
                <input type="text" id="player-name-input" class="input-field" style="background-color: #4B5563; color: #FFFFFF; border: 1px solid #6B7280;" placeholder="اكتب اسمك هنا" maxlength="12">
            </div>

            <div class="mb-4 max-w-sm mx-auto">
                 <label class="block mb-2 text-sm font-medium text-gray-300">اختر لونك</label>
                 <div id="color-picker" class="flex justify-center gap-2"></div>
            </div>

            <div class="space-y-4 max-w-sm mx-auto">
                <button id="create-game-btn" class="btn-primary w-full" disabled>🚀 إنشاء لعبة جديدة</button>
                <div class="flex items-center">
                    <hr class="w-full border-gray-600"><span class="p-2 text-gray-500">أو</span><hr class="w-full border-gray-600">
                </div>
                <input type="text" id="join-game-id-input" class="input-field" placeholder="أدخل معرّف اللعبة هنا" style="background-color: #4B5563; color: #FFFFFF; border: 1px solid #6B7280;">
                <button id="join-game-btn" class="btn-primary w-full" disabled>🤝 انضمام إلى لعبة</button>
            </div>
             <p id="auth-status" class="text-xs text-yellow-400 mt-4 h-4">جاري الاتصال بالخادم...</p>
        </div>

        <div id="game-lobby" class="hidden card">
            <h2 class="text-3xl font-bold text-indigo-400 mb-4">غرفة الانتظار</h2>
            <p class="text-gray-400 mb-2">شارك هذا المعرّف مع أصدقائك للانضمام:</p>
            <p id="lobby-game-id" class="text-4xl font-mono p-3 bg-gray-900 rounded-lg cursor-pointer mb-6" title="اضغط للنسخ"></p>
            <h3 class="text-xl font-bold text-gray-300 mb-3">اللاعبون المنضمون (<span id="player-count">0</span>):</h3>
            <div id="lobby-players-list" class="space-y-2 text-left max-w-md mx-auto mb-8 min-h-[5rem]"></div>
            <button id="start-game-btn" class="btn-primary w-full max-w-md mx-auto hidden">🚀 بدء اللعبة</button>
            <p id="lobby-waiting-msg" class="text-gray-400 mt-4">في انتظار المضيف لبدء اللعبة...</p>
        </div>

        <div id="game-board" class="hidden">
            <div class="card mb-4">
                <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
                    <div><p class="text-sm text-gray-400">معرّف اللعبة:</p><p id="game-id-display" class="text-2xl font-bold font-mono text-indigo-400"></p></div>
                    <div id="timer-display" class="text-5xl font-bold">05:00</div>
                    <div><p class="text-sm text-gray-400">لونك:</p><div id="player-color-box" class="color-box rounded-md mx-auto"></div></div>
                </div>
                 <div id="status-message" class="mt-4 text-yellow-400 h-6"></div>
            </div>
            <div id="canvas-container"></div>
            <div id="scoreboard" class="card mt-4">
                <h3 class="text-xl font-bold mb-2">لوحة النتائج</h3><div id="scores-container" class="grid grid-cols-2 sm:grid-cols-4 gap-4"></div>
            </div>
        </div>

        <div id="winner-modal" class="hidden fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
            <div class="card text-center">
                <h2 id="winner-title" class="text-3xl font-bold mb-4"></h2>
                <p id="winner-message" class="text-lg mb-6"></p>
                <button id="play-again-btn" class="btn-primary">العب مرة أخرى</button>
            </div>
        </div>
    
    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
    <script type="importmap">{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.155.0/examples/jsm/" } }</script>
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, doc, getDoc, setDoc, onSnapshot, updateDoc, arrayUnion, runTransaction } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

        const GRID_SIZE = 15, GAME_DURATION_SECONDS = 300, PIXEL_CLICK_COOLDOWN = 250;
        const PLAYER_COLORS = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF", "#33FFA1", "#FFD700", "#00FFFF"];
        
        const firebaseConfig = JSON.parse(typeof __firebase_config !== 'undefined' ? __firebase_config : '{}');
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-color-wars-3d';
        const DB_PATH = `artifacts/${appId}/public/data/color-wars-3d-games`;

        let app, auth, db, userId, selectedColorIndex = 0;
        let unsubGame = null, timerInterval = null, currentGameId = null, lastClickTime = 0;
        let scene, camera, renderer, controls, raycaster, mouse, cubeMeshes = [], is3DInitialized = false;

        const el = (id) => document.getElementById(id);
        const [gameSetupDiv, playerNameInput, gameLobbyDiv, lobbyGameId, lobbyPlayersList, playerCount, startGameBtn, lobbyWaitingMsg, gameBoardDiv, canvasContainer, createGameBtn, joinGameBtn, joinGameIdInput, authStatus, gameIdDisplay, timerDisplay, playerColorBox, statusMessage, scoresContainer, winnerModal, winnerTitle, winnerMessage, playAgainBtn, colorPicker] =
            ['game-setup', 'player-name-input', 'game-lobby', 'lobby-game-id', 'lobby-players-list', 'player-count', 'start-game-btn', 'lobby-waiting-msg', 'game-board', 'canvas-container', 'create-game-btn', 'join-game-btn', 'join-game-id-input', 'auth-status', 'game-id-display', 'timer-display', 'player-color-box', 'status-message', 'scores-container', 'winner-modal', 'winner-title', 'winner-message', 'play-again-btn', 'color-picker'].map(el);

        function init3D() {
            if (is3DInitialized) return;
            scene = new THREE.Scene(); scene.background = new THREE.Color(0x111827);
            renderer = new THREE.WebGLRenderer({ antialias: true }); renderer.setPixelRatio(window.devicePixelRatio); renderer.setSize(canvasContainer.clientWidth, canvasContainer.clientHeight);
            canvasContainer.innerHTML = ''; canvasContainer.appendChild(renderer.domElement);
            camera = new THREE.PerspectiveCamera(50, canvasContainer.clientWidth / canvasContainer.clientHeight, 1, 1000); camera.position.set(GRID_SIZE, GRID_SIZE, GRID_SIZE * 1.5);
            controls = new OrbitControls(camera, renderer.domElement); controls.enableDamping = true;
            scene.add(new THREE.AmbientLight(0xffffff, 0.6)); const dirLight = new THREE.DirectionalLight(0xffffff, 0.8); dirLight.position.set(50, 50, 50); scene.add(dirLight);
            raycaster = new THREE.Raycaster(); mouse = new THREE.Vector2();
            createCubeGrid(); animate(); is3DInitialized = true;
        }

        function createCubeGrid() {
            if (cubeMeshes.length > 0) return;
            const geometry = new THREE.BoxGeometry(1, 1, 1);
            const offset = - (GRID_SIZE * 1.2) / 2 + 0.6;
            for (let i = 0; i < GRID_SIZE * GRID_SIZE; i++) {
                const material = new THREE.MeshLambertMaterial({ color: 0x4B5563 });
                const cube = new THREE.Mesh(geometry, material);
                cube.position.set((i % GRID_SIZE) * 1.2 + offset, Math.floor(i / GRID_SIZE) * 1.2 + offset, 0);
                cube.userData.gridIndex = i;
                scene.add(cube); cubeMeshes.push(cube);
            }
        }
        function animate() { requestAnimationFrame(animate); if(controls) controls.update(); if (renderer && scene && camera) renderer.render(scene, camera); }
        function onWindowResize() { if (!is3DInitialized) return; camera.aspect = canvasContainer.clientWidth / canvasContainer.clientHeight; camera.updateProjectionMatrix(); renderer.setSize(canvasContainer.clientWidth, canvasContainer.clientHeight); }
        
        async function initialize() {
             try {
                renderColorPicker();
                app = initializeApp(firebaseConfig); db = getFirestore(app); auth = getAuth(app);
                onAuthStateChanged(auth, async (user) => {
                    if (user) { userId = user.uid; createGameBtn.disabled = false; joinGameBtn.disabled = false; authStatus.textContent = "متصل وجاهز للعب!"; authStatus.classList.remove('text-yellow-400'); authStatus.classList.add('text-green-400'); }
                });
                if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) await signInWithCustomToken(auth, __initial_auth_token); else await signInAnonymously(auth);
            } catch (error) { authStatus.textContent = "فشل الاتصال بالخادم."; }
        }
        
        function getPlayerInput() {
            const name = playerNameInput.value.trim();
            return { uid: userId, name: name.slice(0, 12), colorIndex: selectedColorIndex };
        }

        async function createGame() {
            if (!playerNameInput.value.trim()) {
                authStatus.textContent = "الرجاء إدخال اسمك.";
                return;
            }
            const gameId = crypto.randomUUID().split('-')[0];
            const gameRef = doc(db, DB_PATH, gameId);
            const player = getPlayerInput();
            await setDoc(gameRef, { 
                host: userId, 
                status: "lobby",
                players: [player]
            });
            listenToGameUpdates(gameId);
        }
        async function joinGame(gameId) {
            if (!gameId) { authStatus.textContent = "الرجاء إدخال معرّف اللعبة."; return; }
            if (!playerNameInput.value.trim()) { authStatus.textContent = "الرجاء إدخال اسمك."; return; }
            joinGameBtn.disabled = true;
            authStatus.textContent = "جاري التحقق من اللعبة...";
            try {
                const gameRef = doc(db, DB_PATH, gameId);
                await runTransaction(db, async (tx) => {
                    const gameSnap = await tx.get(gameRef);
                    if (!gameSnap.exists()) throw new Error("اللعبة غير موجودة! تأكد من المعرّف.");
                    const gameData = gameSnap.data();
                    const players = gameData.players || [];
                    if (players.some(p => p.uid === userId)) return;
                    if (gameData.status !== 'lobby') throw new Error("لا يمكن الانضمام، اللعبة قد بدأت بالفعل.");
                    if (players.length >= PLAYER_COLORS.length) throw new Error("عذراً، هذه اللعبة ممتلئة.");
                    const newPlayer = getPlayerInput();
                    const usedColors = players.map(p => p.colorIndex);
                    if (usedColors.includes(newPlayer.colorIndex)) {
                        const availableColor = PLAYER_COLORS.map((_,i) => i).find(i => !usedColors.includes(i));
                        if (availableColor !== undefined) newPlayer.colorIndex = availableColor;
                        else throw new Error("عذراً، لا توجد ألوان متاحة.");
                    }
                    tx.update(gameRef, { players: arrayUnion(newPlayer) });
                });
                listenToGameUpdates(gameId);
            } catch (error) {
                authStatus.textContent = error.message;
                setTimeout(() => { authStatus.textContent = "متصل وجاهز للعب!"; joinGameBtn.disabled = false; }, 3000);
            }
        }

        
        async function startGame() {
            const gameRef = doc(db, DB_PATH, currentGameId);
            await updateDoc(gameRef, { status: 'playing', grid: Array(GRID_SIZE * GRID_SIZE).fill(-1), startTime: new Date().toISOString() });
        }
        
        function listenToGameUpdates(gameId) {
            cleanupListeners();
            currentGameId = gameId;
            const gameRef = doc(db, DB_PATH, gameId);
            unsubGame = onSnapshot(gameRef, (docSnap) => {
                if (!docSnap.exists()) { resetToLobby("تم حذف اللعبة من قبل المضيف."); return; }
                const gameData = docSnap.data();
                render(gameData);
            }, (error) => {
                resetToLobby("حدث خطأ في الاتصال باللعبة.");
            });
        }
        
        function render(gameData) {
            if (!gameData || !gameData.status || !gameData.players) return;
            // The user is considered "in the game" if their ID is in the players array.
            if (gameData.players.some(p => p.uid === userId)) {
                if (gameData.status === 'lobby') {
                    renderLobby(gameData);
                } else if (gameData.status === 'playing' || gameData.status === 'finished') {
                    renderGameBoard(gameData);
                    if (gameData.status === 'finished') {
                        if (!gameData.winner && userId === gameData.host) calculateAndSetWinner(gameData);
                        if (!winnerModal.classList.contains('flex')) showWinner(gameData);
                    }
                }
            }
        }
        
        function renderLobby(gameData) {
            gameSetupDiv.classList.add('hidden'); gameBoardDiv.classList.add('hidden'); gameLobbyDiv.classList.remove('hidden');
            lobbyGameId.textContent = currentGameId;
            lobbyPlayersList.innerHTML = '';
            playerCount.textContent = gameData.players.length;
            gameData.players.forEach(p => { lobbyPlayersList.innerHTML += `<div class="player-list-item"><div class="color-box rounded-md" style="background-color: ${PLAYER_COLORS[p.colorIndex]}"></div><span class="text-lg">${p.name}</span></div>`; });
            
            if (userId === gameData.host) { startGameBtn.classList.remove('hidden'); lobbyWaitingMsg.classList.add('hidden'); }
            else { startGameBtn.classList.add('hidden'); lobbyWaitingMsg.classList.remove('hidden'); }
        }
        
        function renderGameBoard(gameData) {
            if (gameBoardDiv.classList.contains('hidden')) { gameLobbyDiv.classList.add('hidden'); gameBoardDiv.classList.remove('hidden'); if (!is3DInitialized) { init3D(); onWindowResize(); } }
            updateUI(gameData);
        }

        function startClientTimer(startTime) {
            if (timerInterval) clearInterval(timerInterval);
            const gameEndTime = new Date(startTime).getTime() + GAME_DURATION_SECONDS * 1000;
            timerInterval = setInterval(async () => {
                const timeLeft = Math.max(0, gameEndTime - Date.now());
                const minutes = Math.floor((timeLeft / 1000) / 60).toString().padStart(2, '0');
                const seconds = Math.floor((timeLeft / 1000) % 60).toString().padStart(2, '0');
                timerDisplay.textContent = `${minutes}:${seconds}`;
                if (timeLeft === 0) {
                    clearInterval(timerInterval); timerInterval = null;
                    if (currentGameId) {
                        const gameRef = doc(db, DB_PATH, currentGameId);
                        const docSnap = await getDoc(gameRef);
                        if (docSnap.exists() && docSnap.data().host === userId && docSnap.data().status === 'playing') {
                            await updateDoc(gameRef, { status: "finished" });
                            await calculateAndSetWinner(docSnap.data());
                        }
                    }
                }
            }, 500);
        }

        function updateUI(gameData) {
            const me = gameData.players.find(p => p.uid === userId);
            if (!me) { resetToLobby("لقد تم إزالتك من اللعبة."); return; }
            gameIdDisplay.textContent = currentGameId;
            if (gameData.startTime && !timerInterval) startClientTimer(gameData.startTime);
            updateCubeColors(gameData.grid, gameData.players);
            updateScores(gameData.grid, gameData.players);
            playerColorBox.style.backgroundColor = PLAYER_COLORS[me.colorIndex];
        }
        
        function updateCubeColors(grid, players) {
            if (!is3DInitialized || !Array.isArray(grid) || grid.length === 0) return;
            grid.forEach((colorIndex, i) => { if (cubeMeshes[i]) cubeMeshes[i].material.color.set(colorIndex !== -1 ? PLAYER_COLORS[colorIndex] : 0x4B5563); });
        }

        function updateScores(grid, players) {
            scoresContainer.innerHTML = '';
            if (!Array.isArray(grid) || !Array.isArray(players)) return;
            const scores = {};
            players.forEach(p => scores[p.colorIndex] = 0);
            for (const colorIndex of grid) if (colorIndex in scores) scores[colorIndex]++;
            players.forEach(p => {
                const scoreElement = document.createElement('div');
                scoreElement.className = 'flex items-center justify-center gap-2 p-2 bg-gray-700 rounded-lg';
                scoreElement.innerHTML = `<div class="color-box rounded-md" style="background-color: ${PLAYER_COLORS[p.colorIndex]}"></div><span class="font-bold text-lg">${scores[p.colorIndex] || 0}</span>`;
                scoresContainer.appendChild(scoreElement);
            });
        }
        
        async function handleCanvasClick(event) {
            if (Date.now() - lastClickTime < PIXEL_CLICK_COOLDOWN || !currentGameId) return;
            const gameRef = doc(db, DB_PATH, currentGameId);
            const gameSnap = await getDoc(gameRef);
            if (!gameSnap.exists() || gameSnap.data().status !== "playing") return;
            
            const me = gameSnap.data().players.find(p => p.uid === userId);
            if (!me) return;

            const rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1; mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(scene.children);
            if (intersects.length > 0) {
                const index = intersects[0].object.userData.gridIndex;
                if (index !== undefined) { lastClickTime = Date.now(); await updateDoc(gameRef, { [`grid.${index}`]: me.colorIndex }); }
            }
        }
        
        async function calculateAndSetWinner(gameData) {
            if (gameData.winner || !Array.isArray(gameData.grid)) return;
            const scores = {};
            gameData.players.forEach(p => scores[p.uid] = 0);
            for (const colorIndex of gameData.grid) {
                const player = gameData.players.find(p => p.colorIndex === colorIndex);
                if (player) scores[player.uid]++;
            }
            let winnerId = null, maxScore = -1, isTie = false;
            Object.keys(scores).forEach(pId => { if (scores[pId] > maxScore) { maxScore = scores[pId]; winnerId = pId; isTie = false; } else if (scores[pId] === maxScore && maxScore > 0) { isTie = true; } });
            await updateDoc(doc(db, DB_PATH, currentGameId), { winner: isTie ? 'tie' : winnerId });
        }
        
        function showWinner(gameData) {
            if (winnerModal.classList.contains('flex')) return;
            if (gameData.winner === 'tie') { winnerTitle.textContent = "👑 تعادل! 👑"; winnerMessage.textContent = "لقد كانت معركة شرسة وانتهت بالتعادل!"; }
            else {
                const winnerInfo = gameData.players.find(p => p.uid === gameData.winner);
                if (winnerInfo) { winnerTitle.textContent = "🎉 الفائز هو! 🎉"; winnerMessage.innerHTML = `اللاعب <span class="font-bold" style="color:${PLAYER_COLORS[winnerInfo.colorIndex]}">${winnerInfo.name}</span> هو المسيطر على اللوحة!`; }
            }
            winnerModal.classList.remove('hidden');
            winnerModal.classList.add('flex');
        }

        function cleanupListeners() {
            if(unsubGame) unsubGame(); if(timerInterval) clearInterval(timerInterval);
            unsubGame = timerInterval = currentGameId = null;
        }

        function resetToLobby(message = "متصل وجاهز للعب!") {
            cleanupListeners();
            is3DInitialized = false; cubeMeshes = [];
            winnerModal.classList.add('hidden'); gameBoardDiv.classList.add('hidden'); gameLobbyDiv.classList.add('hidden'); gameSetupDiv.classList.remove('hidden');
            joinGameIdInput.value = ''; authStatus.textContent = message;
        }
        
        function copyGameId(id) {
            if (!id) return;
            const textArea = document.createElement("textarea");
            textArea.value = id;
            textArea.style.position = "fixed"; textArea.style.top = "-9999px";
            document.body.appendChild(textArea);
            textArea.focus(); textArea.select();
            try { document.execCommand('copy'); lobbyGameId.textContent = "تم النسخ!"; }
            catch (err) { lobbyGameId.textContent = "فشل النسخ"; }
            document.body.removeChild(textArea);
            setTimeout(() => { if(lobbyGameId) lobbyGameId.textContent = id; }, 1500);
        }
        
        function renderColorPicker() {
            PLAYER_COLORS.forEach((color, index) => {
                const colorDiv = document.createElement('div');
                colorDiv.className = 'color-box rounded-full cursor-pointer';
                if(index === selectedColorIndex) colorDiv.classList.add('selected');
                colorDiv.style.backgroundColor = color;
                colorDiv.dataset.colorIndex = index;
                colorPicker.appendChild(colorDiv);
            });
        }

        colorPicker.addEventListener('click', (e) => {
            if(e.target.dataset.colorIndex !== undefined){
                selectedColorIndex = parseInt(e.target.dataset.colorIndex, 10);
                document.querySelectorAll('#color-picker .color-box').forEach(div => div.classList.remove('selected'));
                e.target.classList.add('selected');
            }
        });

        createGameBtn.addEventListener('click', createGame); joinGameBtn.addEventListener('click', () => joinGame(joinGameIdInput.value.trim()));
        startGameBtn.addEventListener('click', startGame); lobbyGameId.addEventListener('click', () => copyGameId(currentGameId));
        playAgainBtn.addEventListener('click', resetToLobby); canvasContainer.addEventListener('click', handleCanvasClick);
        window.addEventListener('resize', onWindowResize);

        initialize();
    </script>
</body>
</html>
