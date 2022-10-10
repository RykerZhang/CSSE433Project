var pokemondb = pokemondb || {}
pokemondb.indexPageController = null;
pokemondb.mainPageController = null;



pokemondb.indexPageController = class{
    constructor(){
        document.querySelector("#loginButton").onclick= (event) => {
			const inputUsername = document.querySelector("#inputName");
			const inputPassword = document.querySelector("#inputPassword");
			// this.login(inputUsername, inputPassword);
            this.login();
		};
    }
    login(){
        fetch("login")
            .then(console.log("redirect"))
            .then(window.location.href = "./main")
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