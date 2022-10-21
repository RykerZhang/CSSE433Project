var pokemondb = pokemondb || {};
pokemondb.indexPageController = null;
pokemondb.mainPageController = null;

//From https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro/35385518#35385518
function htmlToElement(html) {
  var template = document.createElement("template");
  html = html.trim();
  template.innerHTML = html;
  return template.content.firstChild;
}

pokemondb.indexPageController = class {
  constructor() {
    document.querySelector("#loginButton").onclick = (event) => {
      this.login();
    };
  }
  login() {
    const inputUsername = document.querySelector("#inputName");
    const inputPassword = document.querySelector("#inputPassword");
    let data = {
      username: document.querySelector("#username").value,
      password: document.querySelector("#password").value,
    };
    fetch("/main", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.redirected) {
        window.location.href = response.url;
      }
    });
  }
};

pokemondb.mainPageController = class {
  constructor() {
    this.init();
  }
  init() {
    fetch("/getall", { method: "GET" })
      .then((respnse) => respnse.json())
      .then((data) => {
        for (var key in data) {
          var pokemon = data[key];
          pokemon["name"] = pokemon["name-form"].split("-")[0];
          var card = this.create_card(pokemon);
          document.querySelector("#main").append(card);
        }
      });
  }
  create_card(data) {
    return htmlToElement(` <span class="picContainer d-inline-block">
            <img src="${data.img}">
            <p class=caption>${data["name"]}</p>
        </span>`);
  }
};

pokemondb.initialize = function () {
  if (document.querySelector("#indexPage")) {
    console.log("index page");
    new pokemondb.indexPageController();
  }
  if (document.querySelector("#mainPage")) {
    console.log("main page");
    new pokemondb.mainPageController();
  }
};

pokemondb.initialize();
