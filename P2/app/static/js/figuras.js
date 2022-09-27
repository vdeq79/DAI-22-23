const SVG_NS = "http://www.w3.org/2000/svg";
let svg = document.createElementNS(SVG_NS, 'svg');

function randomIntFromInterval(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
}

svg.setAttributeNS(null, "width", "300");
svg.setAttributeNS(null, "height", "300");

svg.style.position = "relative";
svg.style.left = randomIntFromInterval(0,700)+'px';
svg.style.top = randomIntFromInterval(0,300)+'px';


let color = [randomIntFromInterval(0,255),randomIntFromInterval(0,255),randomIntFromInterval(0,255)];
console.log(color);

let r = randomIntFromInterval(20,150);
let rx = randomIntFromInterval(20,150);
let ry = randomIntFromInterval(10,150);


let objectCircle = {r:r,cx:r,cy:r, fill:"rgb("+color[0]+","+color[1]+","+color[2]+")"};
let objectRect = {width:randomIntFromInterval(20,300),height:randomIntFromInterval(20,300),fill:"rgb("+color[0]+","+color[1]+","+color[2]+")"};
let objetcEllip = {rx:rx, ry:ry,cx:rx,cy:ry,fill:"rgb("+color[0]+","+color[1]+","+color[2]+")"};

let objectos = [ ['circle',objectCircle], ['rect', objectRect], ['ellipse', objetcEllip] ];

let i = randomIntFromInterval(0,2);
let figura = document.createElementNS(SVG_NS, objectos[i][0]);

for(var nombre in objectos[i][1]){
    if(objectos[i][1].hasOwnProperty(nombre)){
        figura.setAttributeNS(null,nombre,objectos[i][1][nombre]);
    }
}

svg.appendChild(figura);
document.body.appendChild(svg);