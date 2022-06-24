

window.onload = onPageLoad;


var i = 0;
var txt = '     To better health and mind all around.';
var speed = 120;


function onPageLoad(){
    
    setActive();
    typeMyText();
}



function typeMyText() {
    if (i < txt.length) {
        document.getElementById("type-text").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeMyText, speed);
    }
}


function setActive() {
    aObj = document.getElementById('navbar').getElementsByTagName('a');
    for(i=0;i<aObj.length;i++) {
      if(document.location.href.indexOf(aObj[i].href)>=0) {
        aObj[i].className='active';
      }
    }
}

function changeImage() {
    var myImage = document.getElementById('changeimage');
    var mySrc = myImage.getAttribute('src');
    if(mySrc === "../static/tennislogos.jpg") {
        myImage.setAttribute('src',"../static/tennisball.jpg");
     } else {
        myImage.setAttribute('src',"../static/tennislogos.jpg");
     }
}

 




  



