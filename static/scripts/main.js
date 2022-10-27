// const fs = require("fs");
var pokemondb = pokemondb || {};
pokemondb.indexPageController = null;
pokemondb.mainPageController = null;
pokemondb.db = null;

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
    username = document.querySelector("#username").value;
    password = document.querySelector("#password").value;
    fetch("/login?username=" + username + "&password=" + password, {
      method: "GET",
    }).then((response) => {
      if (response.redirected) {
        window.location.href = response.url;
      } else {
        window.alert("login failed");
      }
    });
  }
};

pokemondb.mainPageController = class {
  constructor() {
    this.init();
    document.querySelector("#searchBtn").onclick = (event) => {
      var InfoType = document.querySelector("#selectSearch").value;
      var info = document.querySelector("#condition").value;
      this.search(InfoType, info);
    };
    document.querySelector("#homeButton").onclick = (event) => {
      window.location.href = "/main";
    };
    document.querySelector("#logOutButton").onclick = (event) => {
      this.logOut();
    };
    document.querySelector("#deleteBtn").onclick = (event) => {
      this.delete(document.querySelector("#deleteInput").value);
    };
  }
  init() {
    fetch("/getall", { method: "GET" })
      .then((respnse) => respnse.json())
      .then((data) => {
        pokemondb.db = data;
        for (var key in data) {
          let pokemon = data[key];
          var card = this.create_card(pokemon);
          card.onclick = (event) => {
            window.location.href = "detail?id=" + pokemon["id"];
          };
          document.querySelector("#main").append(card);
        }
      });
  }
  logOut() {
    // TODO: add log out
    window.location.href = "/index";
  }
  create_card(data) {
    return htmlToElement(` <span class="picContainer d-inline-block">
            <img src="${data.img}">
            <p class=caption>${data["name-form"]}</p>
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
            window.alert("No such result.");
          } else {
            for (var key in data) {
              var pokemon = data[key];
              var card = this.create_card(pokemon);
              document.querySelector("#main").append(card);
            }
          }
        });
    }
  }
  delete(info) {
    // console.log(pokemondb.db);
    var finded = false;
    for (var key in pokemondb.db) {
      var pokemon = pokemondb.db[key];
      if (pokemon["name-form"] == info) {
        finded = true;
      }
    }
    if (!finded) {
      window.alert("Pokemon Not exits");
    } else {
      console.log("deleted");
      fetch("/Delete/" + pokemon["id"], { method: "DELETE" }).then((data) => {
        // console.log(data);
      });
    }
  }
};

pokemondb.detailPageController = class {
  constructor() {
    console.log("detail page");
    document.querySelector("#updateButton").onclick = (event) => {
      console.log("update");
    };
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
  if (document.querySelector("#detailPage")) {
    console.log("detail page");
    new pokemondb.detailPageController();
  }
};

pokemondb.initialize();
