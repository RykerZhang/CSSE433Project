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
    document.querySelector("#addbtn").onclick = (event) => {
      this.add();
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
    var pokemon;
    for (var key in pokemondb.db) {
      var tmp = pokemondb.db[key];
      // var pokemon = key;
      if (tmp["name-form"] == info) {
        pokemon = tmp;
        finded = true;
      }
    }
    if (!finded) {
      window.alert("Pokemon Not exits");
    } else {
      console.log("deleted");
      fetch("/Delete/" + pokemon["id"], { method: "DELETE" }).then((data) => {
        window.location.reload();
      });
    }
  }
  add() {
    var id = String(
      Number(Object.keys(pokemondb.db)[Object.keys(pokemondb.db).length - 1]) +
        10
    );
    var name = document.querySelector("#name_form").value;
    if (!name) {
      window.alert("name can't be null");
    }
    var type1 = document.querySelector("#type1").value || "-";
    var type2 = document.querySelector("#type2").value || "-";
    var species = document.querySelector("#species").value || "-";
    var height = document.querySelector("#height").value || "0";
    var weight = document.querySelector("#weight").value || "0";
    var ability = document.querySelector("#ability").value || "-";
    var catch_rate = document.querySelector("#catch_rate").value || "0";
    var base_exp = document.querySelector("#base_exp").value || "0";
    var grow_rate = document.querySelector("#grow_rate").value || "0";
    var male_rate = document.querySelector("#male_rate").value || "0";
    var female_rate = document.querySelector("#female_rate").value || "0";
    var hp = document.querySelector("#hp").value || "0";
    var attack = document.querySelector("#attack").value || "0";
    var defense = document.querySelector("#defense").value || "0";
    var sp_atk = document.querySelector("#sp_atk").value || "0";
    var sp_def = document.querySelector("#sp_def").value || "0";
    var speed = document.querySelector("#speed").value || "0";
    var total =
      Number(hp) +
      Number(attack) +
      Number(defense) +
      Number(sp_atk) +
      Number(sp_def) +
      Number(speed);
    var img = document.querySelector("#img").value || "-";
    var url =
      "/Insert/" +
      id +
      "/" +
      name +
      "/" +
      type1 +
      "/" +
      type2 +
      "/" +
      species +
      "/" +
      height +
      "/" +
      weight +
      "/" +
      ability +
      "/" +
      catch_rate +
      "/" +
      base_exp +
      "/" +
      grow_rate +
      "/" +
      male_rate +
      "/" +
      female_rate +
      "/" +
      hp +
      "/" +
      attack +
      "/" +
      defense +
      "/" +
      sp_atk +
      "/" +
      sp_def +
      "/" +
      speed +
      "/" +
      String(total) +
      "/" +
      img;
    console.log(url);
    fetch(url, { method: "GET" }).then((response) => {
      window.location.reload();
    });
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
