var questionFild = document.getElementsByClassName('question');
var len_question = questionFild.length;

questionFild[0].style.display = "flex"; //Первому блоку делаем display: "block"
//Всем блокам ставим display: "none"
for (var i = 1; i < len_question; ++i)
    questionFild[i].style.display = "none";

//Для перехода к следующему блоку
function swapDisplay(before_element_id, after_element_id){
	document.getElementsByClassName(before_element_id)[0].style.display = "none";
	document.getElementsByClassName(after_element_id)[0].style.display = "flex";
}