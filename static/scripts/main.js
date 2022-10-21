var pokemondb = pokemondb || {}
pokemondb.indexPageController = null;
pokemondb.mainPageController = null;

//From https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro/35385518#35385518
function htmlToElement(html) {
	var template = document.createElement('template');
	html = html.trim();
	template.innerHTML = html;
	return template.content.firstChild;
}

pokemondb.indexPageController = class{
    constructor(){
        document.querySelector("#loginButton").onclick= (event) => {
			const inputUsername = document.querySelector("#inputName");
			const inputPassword = document.querySelector("#inputPassword");
			// this.login(inputUsername, inputPassword);
            document.querySelector("#loginButton").onclick=(event)=>{

            }
            this.login();
		};
    }
    login(){
        window.location.href="./main"
        fetch("login")
            .then(console.log("redirecting..."))
            .then(fetch('127.0.0.1/main'))
            .then(console.log( console.log("{{pokemon}}")))
            .catch((err) => {
				console.log(err);
			});
    }
    
}


pokemondb.mainPageController = class{
    constructor(){

    }
}

pokemondb.initialize = function(){
    if (document.querySelector("#indexPage")){
        console.log("index page")
        new pokemondb.indexPageController();
    }
    if(document.querySelector("#mainPage")){
        console.log("main page")
        new pokemondb.mainPageController();
    }
}

pokemondb.initialize();