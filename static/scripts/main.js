


document.querySelector("#loginButton").onclick= (event) => {
			const inputUsername = document.querySelector("#inputName");
			const inputPassword = document.querySelector("#inputPassword");
			// this.login(inputUsername, inputPassword);
            fetch("login")
            .then(console.log("redirect"))
            .then(window.location.href = "./main")
            .catch((err) => {
				console.log(err);
			});
		};