function configureDialogHello() {
    var dialogHello = $('#dialogHello').caphDialog({
        center: true,
        focusOption: {
			depth: 1
		}
     });
    
    return dialogHello;
};

function gameStart() {
    var game;
    var gameHeight = window.innerHeight;
    var gameWidth = window.innerWidth;
    var score = 0;
    var dead = false;
    var mainState = {
        preload: function () {
        	game.load.bitmapFont('myfont', 'fonts/font.png', 'fonts/font.fnt');
            game.load.spritesheet('flyingPingus', 'img/flying_pingus.png', 100, 100, 3); 
            game.load.image('ice', 'img/ice.png');
            game.load.audio('jump', 'audio/jump.wav');
        },
        create: function () {
        	score = 0;
        	dead = false;
        	
            game.stage.backgroundColor = '#71c5cf';
            this.pingus = game.add.sprite(gameWidth / 2, gameHeight / 4, 'flyingPingus');
            this.pingus.anchor.setTo(-0.2, 0.5);
            this.pingusFly = this.pingus.animations.add('fly');

            this.iceWall = game.add.group();
            this.nBlocks = Math.floor(gameHeight / 100);
            
            game.physics.startSystem(Phaser.Physics.ARCADE);
            game.physics.arcade.enable(this.pingus);
            this.pingus.body.gravity.y = 1000;  
            
            this.jumpSound = game.add.audio('jump'); 
            this.jumpAnimation = game.add.tween(this.pingus);
            this.jumpAnimation.to({angle: -20}, 100);

            var upKey = game.input.keyboard.addKey(38);
            upKey.onDown.add(this.jump, this); 
            
            this.labelScore = game.add.text(gameWidth / 2, 5, score, {font: '60px Arial', fill: '#fff'});
            
            this.timer = game.time.events.loop(2000, this.addIceWall, this); 
        },
        update: function () {
        	console.log('('+this.pingus.x+', '+this.pingus.y+')');
            if (this.pingus.y < 0 || this.pingus.y > gameHeight) {
            	this.loose();
            }
            if (this.pingus.angle < 20)
                this.pingus.angle += 1; 
            game.physics.arcade.overlap(this.pingus, this.iceWall, this.loose, null, this);
        },
        jump: function () {
        	if (! dead) {
                this.pingus.body.velocity.y = -350;
                //game.add.tween(this.pingus).to({angle: -20}, 100).start();
                this.jumpAnimation.start();
                this.pingus.animations.play('fly', 30, 1);
                this.jumpSound.play();
        	}
        },
        restartGame: function () {
            game.state.start('main');
        },
        addIceBlock: function (x, y) {
            var iceBlock = game.add.sprite(x, y, 'ice');
            this.iceWall.add(iceBlock); 
            game.physics.arcade.enable(iceBlock);
            iceBlock.body.velocity.x = -200;  
            iceBlock.checkWorldBounds = true;
            iceBlock.outOfBoundsKill = true;
        },
        addIceWall: function () {
            var hole = Math.floor(Math.random() * (this.nBlocks - 3)) + 1;
            var correction = 0;

            for (var i = 0; i < this.nBlocks; i++) {
                if (i != hole && i != hole + 1) { 
                    this.addIceBlock(gameWidth, i * 100 + 5 + correction);
                }
                if (i == hole + 1) {
                	correction = gameHeight - this.nBlocks * 100 - 15;   	
                }
            }
            
            score += 1;
            this.labelScore.text = score; 
        },
        loose: function () {
        	dead = true;
        	
        	game.time.events.remove(this.timer);
            this.iceWall.forEach(function (p) {p.body.velocity.x = 0;}, this);
        	
        	var looseText = game.add.bitmapText(gameWidth / 2, gameHeight / 2 - 50, 'myfont', 'Bravo, votre score est de', 64);
        	looseText.anchor.x = 0.5;
        	looseText.anchor.y = 0.5;
        	game.add.text(gameWidth / 2, gameHeight / 2 + 50, score, {font: '150px Arial'});
        	game.add.text(gameWidth / 2, gameHeight - 50, 'Appuyez sur OK pour une nouvelle partie...', {font: '30px Arial'});
            
        	var okKey = game.input.keyboard.addKey($.caph.focus.Constant.DEFAULT.KEY_MAP.ENTER);
            okKey.onDown.add(this.restartGame, this);
        },
    }

    game = new Phaser.Game(gameWidth, gameHeight, Phaser.CANVAS, '');
    game.state.add('main', mainState); 
    game.state.start('main');
}



$(document).ready(function () {
    var dialogHello = configureDialogHello();
    dialogHello.caphDialog('open');

  	$.caph.focus.activate(function(nearestFocusableFinderProvider, controllerProvider) {
  		controllerProvider.addBeforeKeydownHandler(function(context, controller) {
  			console.log(context.event.keyCode);
  			if (context.event.keyCode === $.caph.focus.Constant.DEFAULT.KEY_MAP.ENTER) {
  				dialogHello.caphDialog('close');
  				gameStart();
 				return false;
 			}
 		});
  	});
});