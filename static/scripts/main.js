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
    document.querySelector("#homeButton").onclick = (event) =>{
      window.location.href="/main"
    }
    document.querySelector("#searchBtn").onclick = (event) => {
      var InfoType = document.querySelector("#selectSearch").value;
      var info = document.querySelector("#condition").value;
      this.search(InfoType, info);
    };
    document.querySelector("#refreshButton").onclick = (event) => {
      this.init();
    };
  }
  init() {
    fetch("/getall", { method: "GET" })
      .then((respnse) => respnse.json())
      .then((data) => {
        for (var key in data) {
          var pokemon = data[key];
          pokemon["name"] = pokemon["name-form"].split("-")[0];
          // pokemon["form"] = pokemon["name-form"].split("-")[1];
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
  search(InfoType, info) {
    var node = document.querySelector("#main");
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
    if (info == "") {
      window.alert("condition can't be null");
    } else {
      fetch("/HomeSearch/" + InfoType + "/" + info, { method: "GET" })
        .then((respnse) => respnse.json())
        .then((data) => {
          if (Object.keys(data).length == 0) {
            window.alert("No such result. Please search again");
          } else {
            for (var key in data) {
              var pokemon = data[key];
              pokemon["name"] = pokemon["name-form"].split("-")[0];
              var card = this.create_card(pokemon);
              document.querySelector("#main").append(card);
            }
          }
        });
    }
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
