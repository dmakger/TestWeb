//second.js file
    //console.log(globalVariable.result); 

function answer() {
	var resultFild = document.getElementById('resultFild');
    var result = localStorage.getItem(result);
    //console.log(localStorage.getItem(result));
    //var localVar = window.storage.globalVar;
    resultFild.innerHTML = result + " / 10";
}