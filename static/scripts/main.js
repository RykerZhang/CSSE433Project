// const fs = require("fs");
var pokemondb = pokemondb || {};
pokemondb.indexPageController = null;
pokemondb.mainPageController = null;
pokemondb.type = "";
pokemondb.species = "";

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
      var info = document.querySelectorAll("#condition")[0].value;
      console.log(info == "");
      if (document.querySelectorAll("#condition")[0].value == "") {
        info = document.querySelectorAll("#condition")[1].value;
      }
      this.search(InfoType, info);
    };
    document.querySelector("#sortBtn").onclick = (event) => {
      var InfoType = document.querySelector("#selectSort").value;
      this.sort(InfoType);
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
    document.querySelector("#selectSearch").onchange = (event) => {
      while (document.querySelectorAll("#condition")[1].options[1]) {
        document.querySelectorAll("#condition")[1].remove(1);
      }
      if (document.querySelector("#selectSearch").value == "type") {
        document.querySelectorAll("#condition")[0].classList.add("d-none");
        document.querySelectorAll("#condition")[1].classList.remove("d-none");
        var tmp = document.querySelectorAll("#condition")[1];
        var x = 1;
        for (var t of pokemondb.type) {
          var option = document.createElement("option");
          option.text = t;
          var sel = tmp.options[x++];
          tmp.add(option, sel);
        }
      } else if (
        document.querySelector("#selectSearch").value == "data_species"
      ) {
        document.querySelectorAll("#condition")[0].classList.add("d-none");
        document.querySelectorAll("#condition")[1].classList.remove("d-none");
        var tmp = document.querySelectorAll("#condition")[1];
        var x = 1;
        for (var t of pokemondb.species) {
          var option = document.createElement("option");
          option.text = t;
          var sel = tmp.options[x++];
          tmp.add(option, sel);
        }
      } else {
        document.querySelectorAll("#condition")[1].classList.add("d-none");
        document.querySelectorAll("#condition")[0].classList.remove("d-none");
      }
    };
  }
  init() {
    fetch("/getall", { method: "GET" })
      .then((respnse) => respnse.json())
      .then((data) => {
        pokemondb.species = "";
        pokemondb.type = "";
        if (data.message == "down") {
          const d = JSON.parse(localStorage.getItem("db"));
          if (document.querySelector("#passId").innerHTML) {
            var rec = document.querySelector("#passId").innerHTML;
          }
          rec = data[rec];
          for (var key in data) {
            pokemondb.species += pokemon["data_species"] + ",";
            pokemondb.type += pokemon["type_1"] + ",";
            pokemondb.type += pokemon["type_2"] + ",";
            let pokemon = data[key];
            if (!rec) {
              let card = this.create_card(pokemon);
              card.onclick = (event) => {
                window.location.href = "detail?id=" + pokemon["id"];
              };
              document.querySelector("#main").append(card);
            } else if (
              rec["data_species"] == pokemon["data_species"] &&
              (rec["type_1"] == pokemon["type_1"] ||
                rec["type_2"] == pokemon["type_1"] ||
                rec["type_1"] == pokemon["type_2"] ||
                rec["type_2"] == pokemon["type_2"])
            ) {
              let card = this.create_card(pokemon);
              card.onclick = (event) => {
                window.location.href = "detail?id=" + pokemon["id"];
              };
              document.querySelector("#main").append(card);
            }
          }
          pokemondb.species = pokemondb.species.split(",");
          pokemondb.species = new Set(pokemondb.species);
          pokemondb.type = pokemondb.type.split(",");
          pokemondb.type = new Set(pokemondb.type);
          const ch = document.querySelector("#main").childNodes;
          for (let t = 1; t <= 48; t++) {
            if (ch[t] != undefined) {
              ch[t].classList.remove("d-none");
            }
          }
          const num = Math.ceil(ch.length / 48);
          for (let k = 1; k <= num; k++) {
            let li = this.create_list(k);
            li.onclick = (event) => {
              const ch = document.querySelector("#main").childNodes;
              for (var tm = 0; tm <= (k - 1) * 48; tm++) {
                if (ch[tm].classList != undefined) {
                  ch[tm].classList.add("d-none");
                }
              }
              for (var t = (k - 1) * 48 + 1; t <= k * 48; t++) {
                if (ch[t] != undefined) {
                  ch[t].classList.remove("d-none");
                }
              }
              for (var t = k * 48 + 1; t <= ch.length; t++) {
                if (ch[t] != undefined) {
                  ch[t].classList.add("d-none");
                }
              }
            };
            document.querySelector(".list-group-horizontal").append(li);
          }
        } else {
          localStorage.setItem("db", JSON.stringify(data));
          const d = JSON.parse(localStorage.getItem("db"));
          if (document.querySelector("#passId").innerHTML) {
            var rec = document.querySelector("#passId").innerHTML;
          }
          rec = data[rec];
          for (var key in data) {
            let pokemon = data[key];
            pokemondb.species += pokemon["data_species"] + ",";
            pokemondb.type += pokemon["type_1"] + ",";
            pokemondb.type += pokemon["type_2"] + ",";
            if (!rec) {
              let card = this.create_card(pokemon);
              card.onclick = (event) => {
                window.location.href = "detail?id=" + pokemon["id"];
              };
              document.querySelector("#main").append(card);
            } else if (
              rec["data_species"] == pokemon["data_species"] &&
              (rec["type_1"] == pokemon["type_1"] ||
                rec["type_2"] == pokemon["type_1"] ||
                rec["type_1"] == pokemon["type_2"] ||
                rec["type_2"] == pokemon["type_2"])
            ) {
              let card = this.create_card(pokemon);
              card.onclick = (event) => {
                window.location.href = "detail?id=" + pokemon["id"];
              };
              document.querySelector("#main").append(card);
            }
          }
          pokemondb.species = pokemondb.species.split(",");
          pokemondb.species = new Set(pokemondb.species);
          pokemondb.type = pokemondb.type.split(",");
          pokemondb.type = new Set(pokemondb.type);
          const ch = document.querySelector("#main").childNodes;
          for (var t = 1; t <= 48; t++) {
            if (ch[t] != undefined) {
              ch[t].classList.remove("d-none");
            }
          }
          const num = Math.ceil(ch.length / 48);
          for (let k = 1; k <= num; k++) {
            let li = this.create_list(k);
            li.onclick = (event) => {
              const ch = document.querySelector("#main").childNodes;
              for (var tm = 0; tm <= (k - 1) * 48; tm++) {
                if (ch[tm].classList != undefined) {
                  ch[tm].classList.add("d-none");
                }
              }
              for (var t = (k - 1) * 48 + 1; t <= k * 48; t++) {
                if (ch[t] != undefined) {
                  ch[t].classList.remove("d-none");
                }
              }
              for (var t = k * 48 + 1; t <= ch.length; t++) {
                if (ch[t] != undefined) {
                  ch[t].classList.add("d-none");
                }
              }
            };
            document.querySelector(".list-group-horizontal").append(li);
          }
        }
      });
  }
  create_card(data) {
    return htmlToElement(` <span class="picContainer d-inline-block d-none">
            <img src="${data.img}">
            <p class=caption>${data["name-form"]}</p>
        </span>`);
  }
  create_list(data) {
    return htmlToElement(
      `<li class="list-group-item" id="list${data}">${data}</li>`
    );
  }

  search(InfoType, info) {
    var node = document.querySelector("#main");
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
    if (info == "" && info == "Open this select menu") {
      window.alert("condition can't be null");
    } else {
      fetch("/HomeSearch/" + InfoType + "/" + info, { method: "GET" })
        .then((respnse) => respnse.json())
        .then((data) => {
          if (Object.keys(data).length == 0) {
            window.alert("No such result.");
          } else {
            for (var key in data) {
              let pokemon = data[key];
              let card = this.create_card(pokemon);
              card.onclick = (event) => {
                window.location.href = "detail?id=" + pokemon["id"];
              };
              card.classList.remove("d-none");
              document.querySelector("#main").append(card);
            }
          }
        });
    }
  }
  sort(infoType) {
    var node = document.querySelector("#main");
    while (node.firstChild) {
      node.removeChild(node.firstChild);
    }
    fetch("/Sort/" + infoType, { method: "GET" })
      .then((respnse) => respnse.json())
      .then((data) => {
        if (Object.keys(data).length == 0) {
          window.alert("No such result.");
        } else {
          for (var key in data) {
            let pokemon = data[key];
            let card = this.create_card(pokemon);
            card.onclick = (event) => {
              window.location.href = "detail?id=" + pokemon["id"];
            };
            card.classList.remove("d-none");
            document.querySelector("#main").append(card);
          }

          const ch = document.querySelector("#main").childNodes;
          for (var t = 1; t <= 48; t++) {
            if (ch[t] != undefined) {
              ch[t].classList.remove("d-none");
            }
          }
          const num = Math.ceil(ch.length / 48);
          document.querySelector(".list-group-horizontal").innerHTML = "";
          for (let k = 1; k <= num; k++) {
            let li = this.create_list(k);
            li.onclick = (event) => {
              const ch = document.querySelector("#main").childNodes;
              for (var tm = 0; tm <= (k - 1) * 48; tm++) {
                if (ch[tm].classList != undefined) {
                  ch[tm].classList.add("d-none");
                }
              }
              for (var t = (k - 1) * 48 + 1; t <= k * 48; t++) {
                if (ch[t] != undefined) {
                  ch[t].classList.remove("d-none");
                }
              }
              for (var t = k * 48 + 1; t <= ch.length; t++) {
                if (ch[t] != undefined) {
                  ch[t].classList.add("d-none");
                }
              }
            };
            document.querySelector(".list-group-horizontal").append(li);
          }
        }
      });
  }
  delete(info) {
    var finded = false;
    var pokemon;
    var k = JSON.parse(localStorage.getItem("db"));
    for (var key in k) {
      var tmp = k[key];
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
      Number(
        Object.keys(JSON.parse(localStorage.getItem("db")))[
          Object.keys(JSON.parse(localStorage.getItem("db"))).length - 1
        ]
      ) + 10
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
    const temp = JSON.parse(localStorage.getItem("db"));
    temp[data[0]] = data;
    localStorage.setItem("db", JSON.stringify(temp));
    fetch("/insert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then((respnse) => {
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
