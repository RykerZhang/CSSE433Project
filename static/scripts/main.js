var pokemondb = pokemondb || {}
pokemondb.indexPageController = null;
pokemondb.mainPageController = null;



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