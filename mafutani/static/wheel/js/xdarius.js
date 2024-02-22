    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/spinx/";
    console.log("Connecting to " + ws_path);


    const spinSocket = new WebSocket(ws_path);

    spinSocket.onmessage = function(e) {
        
        const data = JSON.parse(e.data);

        // console.log(data.ipointer)
        if (data.ipointer == 888){
            alert('Place a Bet to Spin!, Enter amount and click BET.Click on Real Cash button to use real money.Finally click SPIN.');
        };

        if (data.ipointer<30){
            startSpinB(data.ipointer);
            winPrice=data.win_a;
        } ;
        if (data.bet_s=="NC"){
            ssg='You Bet more than your account balance of '+data.bal +'.Deposit cash to place such a bet and start winning!';
            alert(ssg)
        } ;

        if (data.bet_s=="MM"){
            ssg='Try Again.Minimum bet is '+data.bet +'';
            alert(ssg)
        } ;  
        if (data.bet_s=="BET"){
            ssg='You place a bet of '+data.bet + '.Click SPIN BUTTON NOW!';
            alert(ssg)
        } ; 
        
       // document.querySelector('#chat-log').value += ('You place a bet of '+data.bet_a + '.SPIN NOW!'+'\n');
    };

    spinSocket.onclose = function(e) {
        console.error('spin socket closed unexpectedly');
    };

    document.querySelector('#bet-input').focus();
    document.querySelector('#real_cash-input').focus();
    document.querySelector('#bet-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#bet-input');
        const real_cashInputDom = document.querySelector('#real_cash-input');
        const message = messageInputDom.value;
        const real_cash = real_cashInputDom.checked;
        const ipointer = 'None';
        //wheelSpinning = false;
    
        spinSocket.send(JSON.stringify({
                'message': message,
                'ipointer': ipointer,
                'real_cash': real_cash
            }));
            
      
            
       messageInputDom.value = '';
       //real_cashInputDom.value = 'off';
    };
       

    document.querySelector('#spin_button').onclick = function(e) {
        // const pointerInputDom = document.querySelector('#spin-pointer-input');
        const ipointer = '';
        const message = 'None';
        const real_cash = 'None';
        if (wheelSpinning == false) {
          spinSocket.send(JSON.stringify({
            'ipointer': ipointer,
            'message': message,
            'real_cash': real_cash
        }));
        
        
        };

        // pointerInputDom.value = '';
    };

// Create new wheel object specifying the parameters at creation time.
let theWheel = new Winwheel({
    'outerRadius'     : 212,        // Set outer radius so wheel fits inside the background.
    'innerRadius'     : 45,   // Make wheel hollow so segments don't go all way to center.
    'responsive'      : false, 
    'textFontSize'    : 24,         // Set default font size for the segments.
    'textOrientation' : 'vertical', // Make text vertial so goes down from the outside of wheel.
    'textAlignment'   : 'outer',    // Align text to outside of wheel.
    'numSegments'     : 28,         // Specify number of segments.
    'segments'        :             // Define segments including colour and text.
    [                               

        {'fillStyle' : '#fff200', 'text' : '20','textFontSize' : 28, 'textFillStyle' : '#4bd890'},
        {'fillStyle' : '#ee1c24', 'text' : '6', 'textFontSize' : 28, 'textFillStyle' : '#000000'},
        {'fillStyle' : '#bfea88', 'text' : '5', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#ffffff', 'text' : ''},
        {'fillStyle' : '#abcde0', 'text' : '100', 'textFontSize' : 28, 'textFillStyle' : '#db9863'},

        {'fillStyle' : '#fedcba', 'text' : '50', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#fff200', 'text' : '20','textFontSize' : 28, 'textFillStyle' : '#4bd890'},
        {'fillStyle' : '#ffffff', 'text' : ''},
        {'fillStyle' : '#fff200', 'text' : '3', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#ee1c24', 'text' : '2', 'textFontSize' : 28, 'textFillStyle' : '#000000'},

        {'fillStyle' : '#fff200', 'text' : '1','textFontSize' : 28, 'textFillStyle' : '#4bb890'},
        {'fillStyle' : '#abffff', 'text' : ''},
        {'fillStyle' : '#bbee44', 'text' : '500', 'textFontSize' : 28, 'textFillStyle' : '#4bb890'},
        {'fillStyle' : '#abffff', 'text' :  ''},
        {'fillStyle' : '#fff200', 'text' : '20', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},

        {'fillStyle' : '#ee1c24', 'text' : '10', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#bfea88', 'text' : '5', 'textFontSize' : 28, 'textFillStyle' : '#000000'},
        {'fillStyle' : '#ffffff', 'text' : ''},
        {'fillStyle' : '#cc9933', 'text' : '200', 'textFontSize' : 28, 'textFillStyle' : '#abede0'},
        {'fillStyle' : '#ee1c24', 'text' : '25'},

        {'fillStyle' : '#fff200', 'text' : '30', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#ffffff', 'text' : ''},                  
        {'fillStyle' : '#fff200', 'text' : '4', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},
        {'fillStyle' : '#ee1c24', 'text' : '2', 'textFontSize' : 28, 'textFillStyle' : '#000000'},
        {'fillStyle' : '#fff200', 'text' : '1', 'textFontSize' : 28, 'textFillStyle' : '#3cb878'},

        {'fillStyle' : '#abff90', 'text' : ''},
        {'fillStyle' : '#adee00', 'text' : '1000', 'textFontSize' : 28, 'textFillStyle' : '#ee1c24'},
        
        {'fillStyle' : '#abff90', 'text' : ''},
    ],
    'animation' :           // Specify the animation to use.
    {
        'type'     : 'spinToStop',
        'duration' : 15,    // Duration in seconds.
        'spins'    : 6,     // Default number of complete spins.
        'callbackFinished' : alertPrize,
        'callbackSound'    : playSound,   // Function to call when the tick sound is to be triggered.
        'soundTrigger'     : 'pin'   ,     // Specify pins are to trigger the sound, the other option is 'segment'.
        // 'callbackAfter' : 'drawTriangle()'
    },
    'pins' :				// Turn pins on.
    {
        'number'     : 28,
        'fillStyle'  : 'silver',
        'outerRadius': 4,
    }
});

// Loads the tick audio sound in to an audio object.
let audio = new Audio('/static/wheel/sounds/ticko.mp3');

// This function is called when the sound is to be played.
function playSound()
{
    // Stop and rewind the sound if it already happens to be playing.
    audio.pause();
    audio.currentTime = 0;

    // Play the sound.
    audio.play();
}
function alertPrize()
{
    // Stop and rewind the sound if it already happens to be playing.

    wheelSpinning = false;
       
    
    ssg='You WON '+winPrice;
    alert(ssg)

    // Play the sound.
 
}
// Vars used by the code in this page to do power controls.
let wheelPower    = 10;
let wheelSpinning = false;
let winPrice    = "X";

function startSpin()
{ 
    if (wheelSpinning == false) {
    // Stop any current animation.
    theWheel.stopAnimation(false);
    // Reset the rotation angle to less than or equal to 360 so spinning again
    // works as expected. Setting to modulus (%) 360 keeps the current position.
    theWheel.rotationAngle = 0;//theWheel.rotationAngle % 360;
    // Start animation.
    theWheel.startAnimation();
    wheelSpinning = true;
    }

}

function startSpinB(seg){
    if (wheelSpinning == false) {

    theWheel.stopAnimation(false);
    theWheel.rotationAngle = 0;
    segmentNumber = seg;
    let stopAt = theWheel.getRandomForSegment(segmentNumber);
    theWheel.animation.stopAngle = stopAt;

    theWheel.startAnimation();
    wheelSpinning = true;

    }
    }
