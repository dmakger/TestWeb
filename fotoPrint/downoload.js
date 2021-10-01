// if (window.innerWidth < 430) {
// 	//let arr_links = document.getElementById("links");
// 	let arr_links = document.getElementsByClassName('rectangle');
// 	arr_links.setAttribute('a', download);
// 	console.log(arr_links);
// }

/*
var bruh = document.getElementsByClassName('block2')
console.log(bruh);
var blocksFild2 = document.getElementsByClassName('block2__content');
var content__boxFild = document.getElementsByClassName('content__box');
console.log(blocksFild2[0]);
console.log(blocksFild2[1]);
*/
var blocksFild = document.getElementsByClassName('block');
console.log(blocksFild[0]);
console.log(document.getElementById('link'));
if (window.innerWidth < 430) {
	document.getElementById('links').style.display = "none";
	document.getElementById('downloads').style.display = "block";
} else{
	document.getElementById('links').style.display = "block";
	document.getElementById('downloads').style.display = "none";
}