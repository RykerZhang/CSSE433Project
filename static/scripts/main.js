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
    console.log("btn");
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
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
    const data = [];
    data[0] = id;
    data[1] = document.querySelector("#name_form").value;
    if (!data[1]) {
      window.alert("name can't be null");
    }
    data[2] = document.querySelector("#type1").value || "-";
    data[3] = document.querySelector("#type2").value || "-";
    data[4] = document.querySelector("#species").value || "-";
    data[5] = document.querySelector("#height").value || "0";
    data[6] = document.querySelector("#weight").value || "0";
    data[7] = document.querySelector("#ability").value || "-";
    data[8] = document.querySelector("#catch_rate").value || "0";
    data[9] = document.querySelector("#base_exp").value || "0";
    data[10] = document.querySelector("#grow_rate").value || "0";
    data[11] = document.querySelector("#male_rate").value || "0";
    data[12] = document.querySelector("#female_rate").value || "0";
    data[13] = document.querySelector("#hp").value || "0";
    data[14] = document.querySelector("#attack").value || "0";
    data[15] = document.querySelector("#defense").value || "0";
    data[16] = document.querySelector("#sp_atk").value || "0";
    data[17] = document.querySelector("#sp_def").value || "0";
    data[18] = document.querySelector("#speed").value || "0";
    data[19] = String(
      Number(hp) +
        Number(attack) +
        Number(defense) +
        Number(sp_atk) +
        Number(sp_def) +
        Number(speed)
    );
    data[20] = document.querySelector("#img").value || "-";
    fetch("/insert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
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
