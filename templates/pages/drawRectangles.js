const Z_KEY = 90;
const WINDOW_WIDTH = 400;
const WINDOW_HEIGHT = 300;
const SIDE_LENGTH = 20;
const FLOOR_LOCATION = 275;

var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

context.clearRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);

context.beginPath();
context.moveTo(0, FLOOR_LOCATION);
context.lineTo(WINDOW_WIDTH, FLOOR_LOCATION);
context.stroke();

context.strokeRect(xPosition, yPosition, SIDE_LENGTH, SIDE_LENGTH);
context.closePath();