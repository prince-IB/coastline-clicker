// Initialize Kaboom with responsive scaling
const GAME_WIDTH = 1200;
const GAME_HEIGHT = 750;

kaboom({
    width: GAME_WIDTH,
    height: GAME_HEIGHT,
    background: [200, 220, 230],
    letterbox: true,
    touchToMouse: true,
    crisp: true,
});

// Game state
const gameState = {
    money: 0,
    clicks: 0,
    moneyPerClick: 1,
    moneyPerTick: 0,
    baseMoneyPerTick: 0,
    tickSpeed: 1000,
    multiplier: 1.0,
    multiplierActive: false,
    multiplierEndTime: 0,
    coastMi: 0,
    armyLevel: 1,
    critChance: 100,
    soldiers: [],
    tanks: [],
    planes: [],
    expeditionPower: 0,
    expeditionState: "idle", // idle, going, returning
    countryName: "",
    selectedFlag: 0,
    upgradeScreen: "money", // money or military
    availableToBuy: true,
    // Prices
    upgradeMoneyPrice: 50,
    upgradeMoneyPerTickPrice: 150,
    upgradeTickSpeedPrice: 300,
    critUpgradePrice: 800,
    tickEfficiencyPrice: 1000,
    soldierPrice: 350,
    tankPrice: 1000,
    planePrice: 5000,
    priceMultiplier: 1.2,
};

// Country names
const countryNames = [
    "Alveria", "Belmonte", "Cascadia", "Delvara", "Eastholm",
    "Frostland", "Goldvale", "Harborton", "Ironcliff", "Jade Coast",
    "Kingsport", "Lakeshire", "Marindale", "Northwind", "Oceanview",
    "Pinecrest", "Queensbury", "Riverdale", "Stormhaven", "Tidemark"
];
gameState.countryName = countryNames[Math.floor(Math.random() * countryNames.length)];

// Soldier names
const soldierNames = ["Rifleman", "Machine Gunner", "Mortarman", "Scout", "Sniper", "Missileman", "Grenadier"];
const tankNames = ["M4 Sherman", "T-34", "Panzer IV", "M1 Abrams", "Leopard 2", "T-90", "Challenger 2"];
const planeNames = ["F-15", "F-14 Tomcat", "F-18", "MiG-29", "Su-27", "Rafale", "Eurofighter"];

// Load assets
loadSprite("menu_bg", "assets/Menu.png");
loadSprite("game_bg", "assets/Game.png");
loadSprite("credits_bg", "assets/credits.png");
loadSprite("money_btn", "assets/button_images/Money.png");
loadSprite("money_btn_pressed", "assets/button_images/Money_pressed.png");
loadSprite("wood", "assets/button_images/wood.png");
loadSprite("military", "assets/button_images/Military.png");
loadSprite("soldier1", "assets/button_images/soldier1.jpeg");
loadSprite("soldier2", "assets/button_images/soldier2.jpg");
loadSprite("tank", "assets/button_images/tank.png");
loadSprite("plane", "assets/button_images/plane.png");
loadSprite("ship", "assets/button_images/Ship.png");

// Load flags
const flagIds = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
for (const i of flagIds) {
    loadSprite(`flag${i}`, `assets/flags/flag${i}.png`);
}

// Load sounds
loadSound("click", "assets/sounds/click.wav");
loadSound("select", "assets/sounds/select.wav");
loadSound("upgrade", "assets/sounds/upgrade.wav");
loadSound("money_click", "assets/sounds/money_click.wav");
loadSound("downgrade", "assets/sounds/downgrade.wav");
loadSound("success", "assets/sounds/success.wav");
loadSound("bgm", "assets/Game_BG_Music.wav");

// Helper function to create a button
function createButton(txt, x, y, w, h, textSize = 24, bgColor = [255, 255, 255]) {
    const btn = add([
        rect(w, h, { radius: 10 }),
        pos(x, y),
        area(),
        color(...bgColor),
        anchor("center"),
        "button",
    ]);

    const labelObj = add([
        text(txt, { size: textSize }),
        pos(x, y),
        anchor("center"),
        color(0, 0, 0),
    ]);

    btn.label = labelObj;

    btn.onHover(() => {
        btn.color = rgb(220, 220, 220);
    });

    btn.onHoverEnd(() => {
        btn.color = rgb(...bgColor);
    });

    return btn;
}

// Unlock audio on any interaction
let audioUnlocked = false;
function unlockAudio() {
    if (!audioUnlocked) {
        // Play a silent/quiet sound to unlock audio context
        play("click", { volume: 0.01 });
        audioUnlocked = true;
    }
}

// MENU SCENE
scene("menu", () => {
    add([
        sprite("menu_bg", { width: width(), height: height() }),
        pos(0, 0),
    ]);

    // Unlock audio on first tap anywhere
    onClick(unlockAudio);
    onTouchStart(unlockAudio);

    const startBtn = createButton("START", width() / 2, 500, 200, 100, 30);
    startBtn.label.color = rgb(0, 255, 0);

    startBtn.onClick(() => {
        unlockAudio();
        play("select", { volume: 0.25 });
        go("country");
    });

    const creditsBtn = createButton("CREDITS", width() / 2, 600, 150, 80, 24);

    creditsBtn.onClick(() => {
        go("credits");
    });
});

// CREDITS SCENE
scene("credits", () => {
    // Credits background image (resized to 1200x750)
    add([
        sprite("credits_bg"),
        pos(0, 0),
    ]);

    // X button to go back - top right corner
    const xBtn = createButton("X", width() - 100, 100, 100, 100, 40);

    xBtn.onClick(() => {
        go("menu");
    });
});

// COUNTRY SELECTION SCENE
scene("country", () => {
    add([
        sprite("game_bg", { width: width(), height: height() }),
        pos(0, 0),
    ]);

    // Title - "Choose your country's flag!"
    add([
        text("Choose your country's flag!", { size: 24 }),
        pos(width() / 2, 50),
        anchor("center"),
        color(0, 0, 0),
    ]);

    let currentFlagIdx = gameState.selectedFlag;

    // Flag display - 500x350, centered
    const flagDisplay = add([
        sprite(`flag${flagIds[currentFlagIdx]}`, { width: 500, height: 350 }),
        pos(width() / 2 - 250, 100),
    ]);

    // Left arrow "<" button
    const leftBtn = add([
        rect(100, 100, { radius: 10 }),
        pos(175, 225),
        area(),
        color(255, 255, 255),
    ]);
    const leftLabel = add([
        text("<", { size: 50 }),
        pos(225, 275),
        anchor("center"),
        color(200, 200, 200),
    ]);

    // Right arrow ">" button
    const rightBtn = add([
        rect(100, 100, { radius: 10 }),
        pos(925, 225),
        area(),
        color(255, 255, 255),
    ]);
    const rightLabel = add([
        text(">", { size: 50 }),
        pos(975, 275),
        anchor("center"),
        color(0, 255, 0),
    ]);

    const updateArrows = () => {
        leftLabel.color = currentFlagIdx <= 0 ? rgb(200, 200, 200) : rgb(0, 255, 0);
        rightLabel.color = currentFlagIdx >= flagIds.length - 1 ? rgb(200, 200, 200) : rgb(0, 255, 0);
    };

    leftBtn.onClick(() => {
        if (currentFlagIdx > 0) {
            play("click");
            currentFlagIdx--;
            flagDisplay.use(sprite(`flag${flagIds[currentFlagIdx]}`, { width: 500, height: 350 }));
            updateArrows();
        }
    });

    rightBtn.onClick(() => {
        if (currentFlagIdx < flagIds.length - 1) {
            play("click");
            currentFlagIdx++;
            flagDisplay.use(sprite(`flag${flagIds[currentFlagIdx]}`, { width: 500, height: 350 }));
            updateArrows();
        }
    });

    // Select button
    const selectBtn = createButton("SELECT", width() / 2, 550, 200, 125, 30);
    selectBtn.label.color = rgb(0, 255, 0);

    selectBtn.onClick(() => {
        play("select", { volume: 0.25 });
        gameState.selectedFlag = currentFlagIdx;
        go("game");
    });
});

// MAIN GAME SCENE
scene("game", () => {
    // Start background music on first interaction (mobile requires this)
    let musicStarted = false;
    const startMusic = () => {
        if (!musicStarted) {
            play("bgm", { loop: true, volume: 0.8 });
            musicStarted = true;
        }
    };
    onClick(startMusic);
    onTouchStart(startMusic);

    // Background
    add([
        sprite("game_bg", { width: width(), height: height() }),
        pos(0, 0),
    ]);

    // Wood panel
    add([
        sprite("wood", { width: 330, height: 630 }),
        pos(870, 120),
    ]);

    // === LEFT SIDE ===

    // Money display
    add([
        rect(350, 100, { radius: 0 }),
        pos(10, 10),
        color(255, 255, 255),
    ]);

    const moneyText = add([
        text("You have $0", { size: 20 }),
        pos(185, 35),
        anchor("center"),
        color(0, 0, 0),
    ]);

    const moneyPerTickText = add([
        text("Money Per Tick: $0", { size: 16 }),
        pos(185, 65),
        anchor("center"),
        color(0, 0, 0),
    ]);

    const tickSpeedText = add([
        text("Tick Speed: 1000ms", { size: 10 }),
        pos(185, 90),
        anchor("center"),
        color(0, 0, 0),
    ]);

    // Money button
    const moneyBtn = add([
        sprite("money_btn", { width: 350, height: 350 }),
        pos(10, 120),
        area(),
    ]);

    moneyBtn.onClick(() => {
        play("money_click");
        gameState.clicks++;

        const crit = Math.floor(Math.random() * gameState.critChance) + 1;
        let earned = gameState.moneyPerClick;
        let critText = "";

        if (crit === 1) {
            earned = gameState.moneyPerClick * 10;
            critText = " (Critical!)";
        }

        gameState.money += earned;

        // Floating text
        const mp = mousePos();
        const ft = add([
            text(`+$${earned}${critText}`, { size: 15 }),
            pos(mp.x + rand(-50, 0), mp.y),
            color(255, 255, 255),
            opacity(1),
            anchor("center"),
        ]);

        ft.onUpdate(() => {
            ft.pos.y -= 1;
            ft.opacity -= 0.02;
            if (ft.opacity <= 0) destroy(ft);
        });

        updateUI();
    });

    // Country name
    add([
        rect(350, 75, { radius: 0 }),
        pos(10, 485),
        color(255, 255, 255),
    ]);

    add([
        text(`Country: ${gameState.countryName}`, { size: 18 }),
        pos(185, 522),
        anchor("center"),
        color(0, 0, 0),
    ]);

    // Flag panel
    add([
        rect(350, 200, { radius: 0 }),
        pos(10, 540),
        color(255, 255, 255),
    ]);

    add([
        sprite(`flag${flagIds[gameState.selectedFlag]}`, { width: 250, height: 175 }),
        pos(60, 542),
    ]);

    // === CENTER - MILITARY ===

    add([
        rect(400, 100, { radius: 0 }),
        pos(415, 10),
        color(255, 255, 255),
    ]);

    const coastText = add([
        text("Coastline: 0mi", { size: 24 }),
        pos(615, 60),
        anchor("center"),
        color(0, 0, 0),
    ]);

    // Military background
    add([
        sprite("military", { width: 400, height: 280 }),
        pos(415, 350),
    ]);

    // Soldier display area
    const soldierObjs = [];
    const tankObjs = [];
    const planeObjs = [];

    function updateMilitaryDisplay() {
        // Clear existing
        soldierObjs.forEach(s => destroy(s));
        tankObjs.forEach(t => destroy(t));
        planeObjs.forEach(p => destroy(p));
        soldierObjs.length = 0;
        tankObjs.length = 0;
        planeObjs.length = 0;

        // Draw soldiers
        gameState.soldiers.forEach((s, i) => {
            const row = Math.floor(i / 23);
            const col = i % 23;
            const obj = add([
                rect(8, 16),
                pos(450 + col * 15, 370 + row * 23),
                color(34, 139, 34),
                area(),
                { name: s.name },
            ]);
            soldierObjs.push(obj);
        });

        // Draw tanks
        gameState.tanks.forEach((t, i) => {
            const row = Math.floor(i / 7);
            const col = i % 7;
            const obj = add([
                rect(40, 30),
                pos(450 + col * 51, 420 + row * 51),
                color(85, 107, 47),
                area(),
                { name: t.name },
            ]);
            tankObjs.push(obj);
        });

        // Draw planes
        gameState.planes.forEach((p, i) => {
            const row = Math.floor(i / 4);
            const col = i % 4;
            const obj = add([
                rect(60, 40),
                pos(460 + col * 81, 500 + row * 81),
                color(70, 130, 180),
                area(),
                { name: p.name },
            ]);
            planeObjs.push(obj);
        });
    }

    // Expedition button
    const expeditionBtn = add([
        rect(400, 100, { radius: 10 }),
        pos(415, 640),
        color(255, 255, 255),
        area(),
    ]);

    const expeditionText1 = add([
        text("Send Expedition!", { size: 20 }),
        pos(615, 665),
        anchor("center"),
        color(0, 0, 0),
    ]);

    const expeditionText2 = add([
        text("Chance of Success: 0.00%", { size: 14 }),
        pos(615, 700),
        anchor("center"),
        color(0, 0, 0),
    ]);

    expeditionBtn.onClick(() => {
        if (gameState.expeditionState !== "idle") return;
        if (gameState.expeditionPower < 0.1) return;

        gameState.expeditionState = "going";
        gameState.availableToBuy = false;
        expeditionBtn.color = rgb(200, 200, 200);

        // Animate soldiers going up (simplified)
        wait(2, () => {
            // Calculate success
            const success = Math.random() * 100 < gameState.expeditionPower;
            if (success) {
                play("success");
                const gained = (gameState.expeditionPower / 100) * (gameState.armyLevel / 2);
                gameState.coastMi = Math.round((gameState.coastMi + gained) * 100) / 100;
            } else {
                play("downgrade");
            }

            gameState.expeditionState = "idle";
            gameState.availableToBuy = true;
            expeditionBtn.color = rgb(255, 255, 255);
            updateUI();
        });
    });

    // Ship random event
    let shipActive = false;
    let shipObj = null;

    function spawnShip() {
        if (shipActive) return;
        shipActive = true;

        shipObj = add([
            sprite("ship", { width: 300, height: 200 }),
            pos(-300, rand(150, 500)),
            area(),
            "ship",
        ]);

        const shipLabel = add([
            text("Click me!", { size: 12 }),
            pos(shipObj.pos.x + 150, shipObj.pos.y + 100),
            anchor("center"),
            color(0, 0, 0),
        ]);

        shipObj.onUpdate(() => {
            shipObj.pos.x += 3;
            shipLabel.pos.x = shipObj.pos.x + 150;
            shipLabel.pos.y = shipObj.pos.y + 100;

            if (shipObj.pos.x > width() + 100) {
                destroy(shipObj);
                destroy(shipLabel);
                shipActive = false;
            }
        });

        shipObj.onClick(() => {
            const events = ["+$500", "+$500", "Money Doubled!", "-$500", "Money Halved"];
            const event = events[Math.floor(Math.random() * events.length)];

            if (event === "+$500") {
                play("upgrade");
                gameState.money += 500;
            } else if (event === "Money Doubled!") {
                play("upgrade");
                gameState.money *= 2;
            } else if (event === "-$500") {
                play("downgrade");
                gameState.money = Math.max(0, gameState.money - 500);
            } else if (event === "Money Halved") {
                play("downgrade");
                gameState.money = Math.floor(gameState.money / 2);
            }

            // Show event text
            const ft = add([
                text(event, { size: 20 }),
                pos(shipObj.pos.x + 150, shipObj.pos.y),
                color(0, 0, 0),
                anchor("center"),
            ]);
            ft.onUpdate(() => {
                ft.pos.y -= 1;
                ft.opacity -= 0.02;
                if (ft.opacity <= 0) destroy(ft);
            });

            destroy(shipObj);
            destroy(shipLabel);
            shipActive = false;
            updateUI();
        });
    }

    // Random ship spawning
    loop(1, () => {
        if (!shipActive && Math.random() < 0.01) {
            spawnShip();
        }
    });

    // === RIGHT SIDE - UPGRADES ===

    add([rect(400, 5), pos(870, 120), color(0, 0, 0)]);
    add([rect(5, 700), pos(870, 120), color(0, 0, 0)]);

    // Ascend button
    add([
        rect(300, 100, { radius: 10 }),
        pos(890, 10),
        color(200, 200, 200),
    ]);
    add([
        text("ASCEND", { size: 24 }),
        pos(1040, 40),
        anchor("center"),
        color(160, 32, 240),
    ]);
    add([
        text("10mi Coastline Required", { size: 12 }),
        pos(1040, 70),
        anchor("center"),
        color(160, 32, 240),
    ]);

    // Shop title
    add([rect(300, 100, { radius: 0 }), pos(890, 140), color(255, 255, 255)]);
    add([
        text("UPGRADES SHOP!", { size: 20 }),
        pos(1040, 190),
        anchor("center"),
        color(0, 0, 0),
    ]);

    // Upgrade containers
    const moneyUpgrades = [];
    const militaryUpgrades = [];

    function createUpgradeBtn(y, line1, line2, onClick, arr) {
        const btn = add([
            rect(300, 75, { radius: 10 }),
            pos(890, y),
            color(255, 255, 255),
            area(),
            "upgradeBtn",
        ]);

        btn.line1 = add([
            text(line1, { size: 14 }),
            pos(1040, y + 25),
            anchor("center"),
            color(0, 0, 0),
        ]);

        btn.line2 = add([
            text(line2, { size: 12 }),
            pos(1040, y + 50),
            anchor("center"),
            color(0, 0, 0),
        ]);

        btn.onClick(onClick);
        arr.push(btn);
        return btn;
    }

    // Money upgrades
    const upg1 = createUpgradeBtn(250, "Upgrade Money Per Click", `(Price = $${gameState.upgradeMoneyPrice})`, () => {
        if (gameState.money >= gameState.upgradeMoneyPrice && gameState.moneyPerClick < 10) {
            play("upgrade");
            gameState.money -= gameState.upgradeMoneyPrice;
            gameState.moneyPerClick++;
            gameState.upgradeMoneyPrice = Math.round(gameState.upgradeMoneyPrice * gameState.priceMultiplier);
            upg1.line2.text = gameState.moneyPerClick >= 10 ? "MAX LEVEL" : `(Price = $${gameState.upgradeMoneyPrice})`;
            updateUI();
        }
    }, moneyUpgrades);

    const upg5 = createUpgradeBtn(335, "Upgrade CritClick Chance", `(Price = $${gameState.critUpgradePrice})`, () => {
        if (gameState.money >= gameState.critUpgradePrice && gameState.critChance > 10) {
            play("upgrade");
            gameState.money -= gameState.critUpgradePrice;
            gameState.critChance = Math.max(1, gameState.critChance - 11);
            gameState.critUpgradePrice = Math.round(gameState.critUpgradePrice * 1.3);
            upg5.line2.text = gameState.critChance <= 10 ? "MAX LEVEL" : `(Price = $${gameState.critUpgradePrice})`;
            updateUI();
        }
    }, moneyUpgrades);

    const upg2 = createUpgradeBtn(420, "Upgrade Money Per Tick", `(Price = $${gameState.upgradeMoneyPerTickPrice})`, () => {
        if (gameState.money >= gameState.upgradeMoneyPerTickPrice) {
            play("upgrade");
            gameState.money -= gameState.upgradeMoneyPerTickPrice;
            gameState.baseMoneyPerTick++;
            gameState.upgradeMoneyPerTickPrice = Math.round(gameState.upgradeMoneyPerTickPrice * 1.15);
            upg2.line2.text = `(Price = $${gameState.upgradeMoneyPerTickPrice})`;
            updateUI();
        }
    }, moneyUpgrades);

    const upg3 = createUpgradeBtn(505, "Reduce Tick Speed", `(Price = $${gameState.upgradeTickSpeedPrice})`, () => {
        if (gameState.money >= gameState.upgradeTickSpeedPrice && gameState.tickSpeed > 1) {
            play("upgrade");
            gameState.money -= gameState.upgradeTickSpeedPrice;
            gameState.tickSpeed = Math.max(1, gameState.tickSpeed - Math.floor(rand(35, 70)));
            gameState.upgradeTickSpeedPrice = Math.round(gameState.upgradeTickSpeedPrice * 1.25 * rand(1.2, 1.3));
            upg3.line2.text = gameState.tickSpeed <= 1 ? "MAX LEVEL" : `(Price = $${Math.round(gameState.upgradeTickSpeedPrice)})`;
            updateUI();
        }
    }, moneyUpgrades);

    const upg4 = createUpgradeBtn(590, "Multiply Money Per Tick", `(30s | Price = $${gameState.tickEfficiencyPrice})`, () => {
        if (gameState.money >= gameState.tickEfficiencyPrice && !gameState.multiplierActive && gameState.moneyPerTick >= 1) {
            play("upgrade");
            gameState.money -= gameState.tickEfficiencyPrice;
            gameState.multiplier = 2.0;
            gameState.multiplierActive = true;
            gameState.multiplierEndTime = time() + 30;
            gameState.tickEfficiencyPrice = Math.round(gameState.tickEfficiencyPrice * 1.15);
            upg4.line2.text = "(ACTIVE - 30s)";
            updateUI();
        }
    }, moneyUpgrades);

    // Military upgrades
    const milUpg1 = createUpgradeBtn(250, "Hire Infantry Soldier", `(Price = $${gameState.soldierPrice})`, () => {
        if (gameState.money >= gameState.soldierPrice && gameState.availableToBuy && gameState.soldiers.length < 46) {
            play("upgrade");
            gameState.money -= gameState.soldierPrice;
            gameState.soldiers.push({ name: soldierNames[Math.floor(Math.random() * soldierNames.length)] });
            gameState.expeditionPower += 0.1;
            updateMilitaryDisplay();
            updateUI();
        }
    }, militaryUpgrades);

    const milUpg2 = createUpgradeBtn(335, "Purchase Infantry Tank", `(Price = $${gameState.tankPrice})`, () => {
        if (gameState.money >= gameState.tankPrice && gameState.availableToBuy && gameState.tanks.length < 14) {
            play("upgrade");
            gameState.money -= gameState.tankPrice;
            gameState.tanks.push({ name: tankNames[Math.floor(Math.random() * tankNames.length)] });
            gameState.expeditionPower += 1;
            updateMilitaryDisplay();
            updateUI();
        }
    }, militaryUpgrades);

    const milUpg3 = createUpgradeBtn(420, "Purchase Fighter Jet", `(Price = $${gameState.planePrice})`, () => {
        if (gameState.money >= gameState.planePrice && gameState.availableToBuy && gameState.planes.length < 8) {
            play("upgrade");
            gameState.money -= gameState.planePrice;
            gameState.planes.push({ name: planeNames[Math.floor(Math.random() * planeNames.length)] });
            gameState.expeditionPower += 5;
            updateMilitaryDisplay();
            updateUI();
        }
    }, militaryUpgrades);

    // Switch screen button
    const switchBtnMoney = createUpgradeBtn(675, "PRESS TO GO TO", "MILITARY UPGRADES", () => {
        gameState.upgradeScreen = "military";
        updateUpgradeVisibility();
    }, moneyUpgrades);
    switchBtnMoney.line1.color = rgb(0, 255, 0);
    switchBtnMoney.line2.color = rgb(0, 255, 0);

    const switchBtnMil = createUpgradeBtn(675, "PRESS TO GO TO", "MONEY UPGRADES", () => {
        gameState.upgradeScreen = "money";
        updateUpgradeVisibility();
    }, militaryUpgrades);
    switchBtnMil.line1.color = rgb(0, 255, 0);
    switchBtnMil.line2.color = rgb(0, 255, 0);

    function updateUpgradeVisibility() {
        const showMoney = gameState.upgradeScreen === "money";
        moneyUpgrades.forEach(btn => {
            btn.hidden = !showMoney;
            btn.line1.hidden = !showMoney;
            btn.line2.hidden = !showMoney;
        });
        militaryUpgrades.forEach(btn => {
            btn.hidden = showMoney;
            btn.line1.hidden = showMoney;
            btn.line2.hidden = showMoney;
        });
    }

    // Initial visibility
    updateUpgradeVisibility();

    // Update UI function
    function updateUI() {
        gameState.moneyPerTick = Math.floor(gameState.baseMoneyPerTick * gameState.multiplier);
        moneyText.text = `You have $${Math.floor(gameState.money)}`;
        moneyPerTickText.text = `Money Per Tick: $${gameState.moneyPerTick}`;
        tickSpeedText.text = `Tick Speed: ${gameState.tickSpeed}ms`;
        coastText.text = `Coastline: ${gameState.coastMi}mi`;
        expeditionText2.text = `Chance of Success: ${gameState.expeditionPower.toFixed(2)}%`;

        // Button colors
        upg1.color = (gameState.money >= gameState.upgradeMoneyPrice && gameState.moneyPerClick < 10) ? rgb(255, 255, 255) : rgb(200, 200, 200);
        upg2.color = gameState.money >= gameState.upgradeMoneyPerTickPrice ? rgb(255, 255, 255) : rgb(200, 200, 200);
        upg3.color = (gameState.money >= gameState.upgradeTickSpeedPrice && gameState.tickSpeed > 1) ? rgb(255, 255, 255) : rgb(200, 200, 200);
        upg4.color = (gameState.money >= gameState.tickEfficiencyPrice && !gameState.multiplierActive && gameState.moneyPerTick >= 1) ? rgb(255, 255, 255) : rgb(200, 200, 200);
        upg5.color = (gameState.money >= gameState.critUpgradePrice && gameState.critChance > 10) ? rgb(255, 255, 255) : rgb(200, 200, 200);

        milUpg1.color = (gameState.money >= gameState.soldierPrice && gameState.availableToBuy) ? rgb(255, 255, 255) : rgb(200, 200, 200);
        milUpg2.color = (gameState.money >= gameState.tankPrice && gameState.availableToBuy) ? rgb(255, 255, 255) : rgb(200, 200, 200);
        milUpg3.color = (gameState.money >= gameState.planePrice && gameState.availableToBuy) ? rgb(255, 255, 255) : rgb(200, 200, 200);

        expeditionBtn.color = gameState.expeditionPower >= 0.1 && gameState.expeditionState === "idle" ? rgb(255, 255, 255) : rgb(200, 200, 200);
    }

    // Money per tick loop
    let lastTick = time();

    onUpdate(() => {
        const now = time();

        if (gameState.moneyPerTick > 0 && (now - lastTick) * 1000 >= gameState.tickSpeed) {
            gameState.money += gameState.moneyPerTick;
            lastTick = now;
            play("click", { volume: 0.5 });
            updateUI();
        }

        if (gameState.multiplierActive && now >= gameState.multiplierEndTime) {
            gameState.multiplier = 1.0;
            gameState.multiplierActive = false;
            upg4.line2.text = `(30s | Price = $${gameState.tickEfficiencyPrice})`;
            updateUI();
        }
    });

    updateUI();
});

// Start
go("menu");
