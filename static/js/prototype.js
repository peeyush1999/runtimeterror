$(document).ready(function(){
	loadStoredNotes();	
	$(document).on('click', '#crteStkyBtn', addNote);
	$(document).on('click', '#addBtn', showOvrly);
	$(document).on('click', '#cnclStkyBtn', cnclOvrly);
	$(document).on('click', '#clnStorge', cleanNotes);
	$(document).on('click', '#wrapper', cnclOvrly);


$("textarea").on("change keyup input",function(){
	if($(this).val().length>0)$("#crteStkyBtn").removeClass("ntActv");
	else if($(this).val().length>100)
	this.value=this.value.substring(0,max);
	else $("#crteStkyBtn").addClass("ntActv")});

	console.log(localStorage.length);
});

function cleanNotes(){
	localStorage.clear();
	$('#stkyNts').empty();	
}

function getStoredNotes(){
	var storedNotes= new Array();
	for(var i =0; i< localStorage.length; i++){
		 storedNotes.push(localStorage[localStorage.key(i)]);
	}
	return storedNotes;
}

function loadStoredNotes(){
	var pastNotes= getStoredNotes()
	console.log(getStoredNotes());
	if(pastNotes.length > 1){
		var i=1;
		for (item in pastNotes){
			createSticky(i);
			i++;
		}
	}else if(pastNotes.length > 0){
			createSticky(pastNotes);
	}
}

function showOvrly(){
	$('#stkyOvrly').removeClass('hidden');
	$('#wrapper').addClass('hideOvrly');
}

function cnclOvrly(){
	$('#stkyOvrly').addClass('hidden');
	$('#wrapper').removeClass('hideOvrly');
	$('.txtBox').val('');
}

function addNote(){
    //  var usrInput = $('.txtBox').val();
	 //console.log(usrInput);
	//  var usrInput = "Hi";

	// if(usrInput.length > 0){
		
		addtoSticky();
		
		//console.log(notes);
	// }else{

	// }
}


function addtoSticky(){
	// if(note.length > 0){
	// 	console.log(note);
		var cnt=document.getElementsByClassName("screen").length;

		createSticky(cnt+1);
		//localStorage.setItem('note_'+note.length, note);
	
}














function select(id)
{
	console.log("select pressed ",id);
	var myCanvas = document.getElementById("myCanvas"+id);
	myCanvas.style.cursor = "crosshair"; 
	var ctx = myCanvas.getContext("2d");
    
    // Fill Window Width and Height
    myCanvas.width = 320;
	myCanvas.height = 360;
	
	// Set Background Color
    ctx.fillStyle="#eab676";
    ctx.fillRect(0,0,myCanvas.width,myCanvas.height);
	
    // Mouse Event Handlers
	if(myCanvas){
		var isDown = false;
		var canvasX, canvasY;
		ctx.lineWidth = 2.5;
		
		$(myCanvas)
		.mousedown(function(e){
			isDown = true;
			ctx.beginPath();
			canvasX = e.pageX - myCanvas.offsetLeft;
			canvasY = e.pageY - myCanvas.offsetTop;
			ctx.moveTo(canvasX, canvasY);
		})
		.mousemove(function(e){
			if(isDown !== false) {
				canvasX = e.pageX - myCanvas.offsetLeft;
				canvasY = e.pageY - myCanvas.offsetTop;
				ctx.lineTo(canvasX, canvasY);
				ctx.strokeStyle = "#000";
				ctx.stroke();
			}
		})
		.mouseup(function(e){
			isDown = false;
			ctx.closePath();
		});
	}
	
	// Touch Events Handlers
	draw = {
		started: false,
		start: function(evt) {

			ctx.beginPath();
			ctx.moveTo(
				evt.touches[0].pageX,
				evt.touches[0].pageY
			);

			this.started = true;

		},
		move: function(evt) {

			if (this.started) {
				ctx.lineTo(
					evt.touches[0].pageX,
					evt.touches[0].pageY
				);

				ctx.strokeStyle = "#000";
				ctx.lineWidth = 5;
				ctx.stroke();
			}

		},
		end: function(evt) {
			this.started = false;
		}
	};
	
	// Touch Events
	myCanvas.addEventListener('touchstart', draw.start, false);
	myCanvas.addEventListener('touchend', draw.end, false);
	myCanvas.addEventListener('touchmove', draw.move, false);
	
	// Disable Page Move
	document.body.addEventListener('touchmove',function(evt){
		evt.preventDefault();
	},false);

}





/*window.onload = function() {
	var myCanvas = document.getElementById("myCanvas1");
	var ctx = myCanvas.getContext("2d");
    
    // Fill Window Width and Height
    myCanvas.width = 300;
	myCanvas.height = 300;
	
	// Set Background Color
    ctx.fillStyle="#fff";
    ctx.fillRect(0,0,myCanvas.width,myCanvas.height);
	
    // Mouse Event Handlers
	if(myCanvas){
		var isDown = false;
		var canvasX, canvasY;
		ctx.lineWidth = 5;
		
		$(myCanvas)
		.mousedown(function(e){
			isDown = true;
			ctx.beginPath();
			canvasX = e.pageX - myCanvas.offsetLeft;
			canvasY = e.pageY - myCanvas.offsetTop;
			ctx.moveTo(canvasX, canvasY);
		})
		.mousemove(function(e){
			if(isDown !== false) {
				canvasX = e.pageX - myCanvas.offsetLeft;
				canvasY = e.pageY - myCanvas.offsetTop;
				ctx.lineTo(canvasX, canvasY);
				ctx.strokeStyle = "#000";
				ctx.stroke();
			}
		})
		.mouseup(function(e){
			isDown = false;
			ctx.closePath();
		});
	}
	
	// Touch Events Handlers
	draw = {
		started: false,
		start: function(evt) {

			ctx.beginPath();
			ctx.moveTo(
				evt.touches[0].pageX,
				evt.touches[0].pageY
			);

			this.started = true;

		},
		move: function(evt) {

			if (this.started) {
				ctx.lineTo(
					evt.touches[0].pageX,
					evt.touches[0].pageY
				);

				ctx.strokeStyle = "#000";
				ctx.lineWidth = 5;
				ctx.stroke();
			}

		},
		end: function(evt) {
			this.started = false;
		}
	};
	
	// Touch Events
	myCanvas.addEventListener('touchstart', draw.start, false);
	myCanvas.addEventListener('touchend', draw.end, false);
	myCanvas.addEventListener('touchmove', draw.move, false);
	
	// Disable Page Move
	document.body.addEventListener('touchmove',function(evt){
		evt.preventDefault();
	},false);
};

*/




// function createSticky(id){
    
// 	$('#stkyNts').append('<li class="box">'+'<div><canvas id="myCanvas'+id+'">s</canvas></div><button onclick="select('+id+');">use</button></li>');
// }







function createSticky(id){

	console.log('called with id',id);
	var str=`<div class='screen' id='mobilescreen'>
      <div id='speaker'></div>
        <div id='maincontainer'>
        <canvas id='myCanvas`+id+`'></canvas>
        </div>

      <div style="display:flex">
       <div class='controlder' onclick='select(`+id+`)'></div>
       <div class='controlder' onclick='upload_sticky(`+id+`)'>SAVE</div>
       </div>

   </div>`;
    
	$('#stkyNts').append(str);
}

//'<li class="box">'+'<div><canvas id="myCanvas'+id+'">s</canvas></div><button onclick="select('+id+');">use</button></li>'
































// BACKGROUND



const bg = new MousemoveBGColors();
/* const bg = new MousemoveBGColors({
       target : 'body' //(string) element selector // default : 'body'
      ,transition : .2 //(float|int) transition duration // default: .09
      ,delay:.03 //(float|int) transition delay // default: 0 
      ,center: [255, 255, 255] //(array) rgb color in the center // default : [168, 218, 218]
      ,topMiddle: [168, 218, 218]  //(array) rgb color in top middle // default : [168, 218, 218]
      ,leftMiddle: [236, 236, 236]  //(array) rgb color in the center // default : [168, 218, 218]
      ,rightMiddle: [255, 120, 63] //(array) rgb color in the center // default : [255, 128, 63]
      ,bottomMiddle: [0, 107, 107] //(array) rgb color in the center // default : [168, 218, 218]
      });
*/
const initButtons = (function(){
    const btn= document.getElementById('destroyInit');
          btn.addEventListener('click',(e) => { 
            e.currentTarget.classList.toggle('init')
            e.currentTarget.classList.toggle('destroy');
            if(e.currentTarget.classList.contains('destroy')){
              bg.destroy();
            }else{
              bg.init();
            }
            
          })
}());


function MousemoveBGColors(options){
    const _this = this; 
    const defaultOptions = {
        target: "body"
       ,transition : .09
       ,delay:0
       ,center: [168, 218, 218] // green
       ,topMiddle: [168, 218, 218]
       ,leftMiddle: [236, 236, 236] // gris
       ,rightMiddle: [255, 128, 63] // orange;
      ,bottomMiddle: [204, 177, 218] // purple;

    }
    let colorsAvg = {
      topLeft:null
      ,topRight:null
      ,bottomLeft:null
      ,bottomRight:null
    };

    let ww;
    let wh;
    
    options = {...defaultOptions, ...options};
    
    this.init = function() {
        colorsAvg.topLeft=this.average(options.leftMiddle, options.topMiddle);
        colorsAvg.topRight = this.average(options.topMiddle, options.rightMiddle);
        colorsAvg.bottomLeft = this.average(options.leftMiddle, options.bottomMiddle);
        colorsAvg.bottomRight = this.average(options.bottomMiddle, options.rightMiddle);
        this.getSizes();
        
        window.addEventListener('mousemove',this.mousemove,true);
        window.addEventListener('resize',this.getSizes,true);
        document.querySelector(options.target).classList.add("mousemoveBGColorsInitialized");

    }



    this.destroy = function(){

      window.removeEventListener('mousemove',_this.mousemove,true);
      window.removeEventListener('resize',_this.getSizes,true);
      document.querySelector(options.target).classList.remove("mousemoveBGColorsInitialized");

      const target = document.querySelector(options.target);
      target.style.backgroundColor =null;

      if(options.transition>0){
        target.style.transitionDuration =null;
      }

      if(options.delay>0){
        target.style.transitionDelay =null;
      }
    }

    this.getSizes = function(){
      const win = window;
      const doc = document;
      const docEl = doc.documentElement;
      const body0 = doc.getElementsByTagName('body')[0];
      ww = win.innerWidth||docEl.clientWidth||body0.clientWidth;
      wh = win.innerHeight||docEl.clientHeight||body0.clientHeight;
    }

    this.average = function(a,b){
        return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[1] + b[1])];
    }
    this.interpolate2D = function(x00, x01, x10, x11, x, y) {
        return x00 * (1 - x) * (1 - y) + x10 * x * (1 - y) + x01 * (1 - x) * y + x11 * x * y;
    }
    this.interpolateArray = function(x00, x01, x10, x11, x, y) {
      let result = [0, 0, 0];
      for (let i = 0; i < 3; ++i) {
        result[i] = Math.floor(_this.interpolate2D(x00[i], x01[i], x10[i], x11[i], x, y));
      }
      return result;
    }

    this.mousemove = function(e){
        let positionX = e.pageX / ww;
        let positionY = e.pageY / wh;
        let x00, x01, x11, x10;

        if (positionX > 0.5 && positionY > 0.5) {
        x00 = options.center;
        x01 = options.bottomMiddle;
        x10 = options.rightMiddle;
        x11 = colorsAvg.bottomRight;
        positionX = 2.0 * (positionX - 0.5); // scale position back to [0, 1]
        positionY = 2.0 * (positionY - 0.5);
      } else if (positionX > 0.5 && positionY <= 0.5) {
        x00 = options.topMiddle;
        x01 = options.center;
        x10 = colorsAvg.topRight;
        x11 = options.rightMiddle;
        positionX = 2.0 * (positionX - 0.5);
        positionY = 2.0 * (positionY);
      } else if (positionX <= 0.5 && positionY <= 0.5) {
        x00 = colorsAvg.topLeft;
        x01 = options.leftMiddle;
        x10 = options.topMiddle;
        x11 = options.center;
        positionX = 2.0 * (positionX);
        positionY = 2.0 * (positionY);
      } else if (positionX <= 0.5 && positionY > 0.5) {
        x00 = options.leftMiddle;
        x01 = colorsAvg.bottomLeft;
        x10 = options.center;
        x11 = options.bottomMiddle;
        positionX = 2.0 * (positionX);
        positionY = 2.0 * (positionY - 0.5);
      } else {
        // can't happen
      }
      const rgb=_this.interpolateArray(x00, x01, x10, x11, positionX, positionY);
      
      const target = document.querySelector(options.target);
      target.style.backgroundColor ='rgb(' + rgb.join(',') + ')';

      
      if(options.transition>0){
        target.style.transitionDuration =options.transition+'s';
      }
      if(options.delay>0){
        target.style.transitionDelay =options.delay+'s';
      }
    }
    this.init();
    
}
















// MOBILE VIEW Handlers



















$("#menu").click(function(){
	$("#mainmenu").toggleClass("showmenu");
	
	$("#mainscreen").toggleClass("movemaincontainer");
  });
  
  
  
  $("#menu").click(function(){
   $("#mainmenu2").toggleClass("showmenu2");
	$("#mainscreen").toggleClass("movemaincontainer");
  });