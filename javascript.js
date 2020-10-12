var list = null;

var xhrdata = null;

window.onload = function() {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "getJobs", true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      console.log(xhr.responseText);
      try {
        var responseData = JSON.parse(xhr.responseText);
      } catch (e) {
        console.log(e);
      } finally {
        list = new entitieList('jobTable', responseData);
        list.list();
      };
    };
  };
  xhr.send();
};

class entitieList {
  constructor(tableId, data) {
    this.table = document.getElementById(tableId);
    this.data = data;
    this.editDiv;
    this.editing = false;
  };
  list() {
    console.log(this.data);
    this.table.innerHTML = "";
    xhrdata = this.data;
    var data = this.data;
    for (var j = 0; j < data.length; j++) {
      var job = data[j];
      var tr = document.createElement("tr");
      var td = [];
      for (var i = 0; i <= 8; i++) td.push(document.createElement("td")); //creating tds
      var editBtn = document.createElement("button"); //button for editing the job
      var self = this;
      const jobId = job.id; // save it for the onlick handle install, const in order to let it be constant and individual for every button
      editBtn.onclick = function() {
        self.edit(jobId);
      }
      editBtn.innerHTML = "Job bearbeiten";
      var deleteBtn = document.createElement("button"); //delete button
      var self = this;
      deleteBtn.onclick = function() {
        self.delete(jobId);
      }
      deleteBtn.innerHTML = "Job löschen";
      var pauseChk = document.createElement("input");
      pauseChk.setAttribute("type", "checkbox");
      if (job.running) pauseChk.setAttribute("checked", "true");
      var self = this;
      pauseChk.onchange = function() {
          self.toggle(jobId);
        }
        // pauseBtn.innerHTML = "Job barbeiten";
      td[0].innerHTML = job.id;
      td[1].innerHTML = job.name;
      td[2].innerHTML = job.args[0] === undefined ? "" : job.args[0];
      td[3].innerHTML = job.args[1] === undefined ? "" : job.args[1];
      td[4].innerHTML = job.trigger;
      var triggerArgsStr = "";
      for (var argument in job.triggerargs) {
        if (job.triggerargs.hasOwnProperty(argument)) {
          // console.log(argument + ": " + job.triggerargs[argument]);
          triggerArgsStr += argument + ": " + job.triggerargs[argument] + ", ";
          // console.log(triggerArgsStr);
        };
      };
      td[5].innerHTML = triggerArgsStr.substring(0, triggerArgsStr.length - 2);
      td[6].appendChild(editBtn);
      td[7].appendChild(deleteBtn);
      td[8].appendChild(pauseChk);
      td[8].style.backgroundColor = (job.running) ? "green" : "red";
      for (var i = 0; i < td.length; i++) tr.appendChild(td[i]);
      this.table.appendChild(tr);
    };
  };
  edit(jobId) {
    this.createModal(jobId);
  }
  delete(jobId) {
    if (!confirm("Willst du das wirklich löschen?")) return;
    console.log("delete: " + jobId);
    var xhr = new XMLHttpRequest();
    const json = {id: jobId};
    xhr.open("POST", "deleteJob", true);
    xhr.onreadystatechange = function() {
      if (xhr.status == 200 && xhr.readyState == 4) {
        console.log(xhr.responseText);
        window.onload();
      }
    };
    xhr.setRequestHeader("Content-Type","application/json");
    xhr.send(JSON.stringify(json));
  }
  toggle(jobId) {
    console.log("toggle: " + jobId);
    var xhr = new XMLHttpRequest();
    const json = {
        id: jobId
    };
    xhr.open("POST", "toggleJob", true);
    xhr.onreadystatechange = function() {
      if (xhr.status == 200 && xhr.readyState == 4) {
        console.log(xhr.responseText);
        window.onload();
      }
    };
    xhr.setRequestHeader("Content-Type","application/json");
    xhr.send(JSON.stringify(json));
  }
  createModal(jobId = null) {
      console.log("jobid: " + String(jobId));
      var job;
      if (jobId == null) {
        this.editing = false;
        var idint = Date.now();
        job = {
          id: idint.toString(),
          name: "",
          args: [""],
          trigger: "date",
          triggerargs: {
            run_date: ""
          }
        };
        // job.id = Date.now();
        // job.name = "";
        // job.args[0] = "";
        // job.trigger = "date";
        // job.triggerargs.run_date = "";
      } else {
        this.editing = true;
        var dataId;
        for (var i = 0; i < this.data.length; i++) {
          if (this.data[i].id == jobId) {
            dataId = i;
            break;
          };
        };
        job = this.data[dataId];
      }
      this.spawnModal(job);
    } //preparing the job for prefilling
  spawnModal(job) {
    var inputVariants = {
      "cron": {
        "jitter": "number",
        "year": "text",
        "month": "text",
        "week": "text",
        "day": "text",
        "day_of_week": "text",
        "hour": "text",
        "minute": "text",
        "second": "text",
        "start_date": "datetime-local",
        "end_date": "datetime-local"
      },
      "interval": {
        "jitter": "number",
        "weeks": "number",
        "days": "number",
        "hours": "number",
        "minutes": "number",
        "seconds": "number",
        "start_date": "datetime-local",
        "end_date": "datetime-local"
      },
      "date": {
        "run_date": "datetime-local"
      }
    };
    var triggerSelect = Object.keys(inputVariants); //possibilities for the selectbox
    this.editDiv = document.createElement("div");
    this.editDiv.setAttribute("id", "editDiv");
    document.body.appendChild(this.editDiv);
    var divs = [];
    for (var i = 0; i < 6; i++) {
      divs.push(document.createElement("div"));
      var descriptions = ["id", "name", "objectName", "args", "trigger", "triggerargs"];
      var descriptionDiv = document.createElement("div");
      descriptionDiv.innerText = descriptions[i] + ": ";
      divs[i].appendChild(descriptionDiv);
      this.editDiv.appendChild(divs[i]);
    };
    var id = document.createTextNode(job.id);
    divs[0].appendChild(id);
    var name = document.createElement("input");
    name.setAttribute("type", "text");
    name.setAttribute("id", "editName");
    name.setAttribute("value", job.name);
    divs[1].appendChild(name);
    var objectname = document.createElement("input");
    objectname.setAttribute("type", "text");
    objectname.setAttribute("id", "editName");
    objectname.setAttribute("value", job.args[0]);
    divs[2].appendChild(objectname)
    var args = document.createElement("input");
    args.setAttribute("type", "text");
    args.setAttribute("id", "editArgs");
    args.setAttribute("value", job.args[1] === undefined ? "" : job.args[1]);
    divs[3].appendChild(args);
    var trigger = document.createElement("select");
    for (var i = 0; i < triggerSelect.length; i++) {
      var option = document.createElement("option");
      option.setAttribute("value", triggerSelect[i]);
      option.innerText = triggerSelect[i];
      if (triggerSelect[i] == job.trigger) option.setAttribute("selected", "");
      trigger.appendChild(option);
    };
    var inputDiv = document.createElement('div');
    divs[4].appendChild(trigger);
    divs[5].appendChild(inputDiv);
    var selectorInput = trigger;
    var triggerargs;
    var triggerargdata; //prepare pointers for saving
    var elems;
    selectorInput.onchange = function() { //creating all input fields according to inputVariants
      triggerargs = [];
      console.log(this.value);
      var inputs = inputVariants[this.value];
      inputDiv.innerHTML = "";
      for (var id in inputs) {
        if (inputs.hasOwnProperty(id)) {
          var container = document.createElement("div");
          var caption = document.createTextNode(id + ": ");
          triggerargs[id] = (document.createElement("input"));
          triggerargs[id].setAttribute("type", inputs[id]);
          triggerargs[id].setAttribute("id", "trigger_" + id);
          container.appendChild(caption);
          container.appendChild(triggerargs[id]);
          inputDiv.appendChild(container);
        }
      }
      triggerargdata = []; //refreshing the pointers to the data fields
      for (var triggerName in triggerargs) {
        if (triggerargs.hasOwnProperty(triggerName)) {
          triggerargdata[triggerName] = triggerargs[triggerName];
        }
      }
      elems = {
        id: job.id,
        name: name,
        objectName: objectname,
        args: args,
        trigger: trigger,
        triggerargs: triggerargdata
      };
      // console.log(triggerargdata);
    }
    selectorInput.onchange(); //run onchange once
    for (var triggerName in job.triggerargs) { //prefill when editing
      if (job.triggerargs.hasOwnProperty(triggerName)) {
        triggerargs[triggerName].value = job.triggerargs[triggerName];
      }
    }


    var saveBtn = document.createElement('button'); //create savebtn
    saveBtn.innerHTML = "Speichern";
    var self = this;
    saveBtn.onclick = function() {
      self.save(elems);
    };
    this.editDiv.appendChild(saveBtn);

    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = "Schließen";
    closeBtn.onclick = function() {
      self.editDiv.parentElement.removeChild(self.editDiv);
    }
    this.editDiv.appendChild(closeBtn);
  }; //spawning the actual modal
  save(elems) {
    // console.log(elems);
    var integers = ['hours', 'weeks', 'days', 'jitter', 'minutes', 'seconds'];
    var triggerargs = elems.triggerargs
    var triggerargdata = {};
    for (var triggerName in triggerargs) {
      if (triggerargs.hasOwnProperty(triggerName)) {
        triggerargdata[triggerName] = (triggerargs[triggerName].value == "") ? undefined : triggerargs[triggerName].value;
        if (triggerargs[triggerName].type == "datetime-local" && triggerargs[triggerName].value != "") {
          // console.log("converting date");
          // console.log(triggerargdata[triggerName]);
          // console.log(triggerargdata[triggerName].replace("T"," ") + ":00");
          // var rundate = new Date(triggerargdata[triggerName]);
          // var str = rundate.getFullYear() + "-" + rundate.getMonth() + "-" + rundate.getDate() + " " + rundate.getHours() + ":" + rundate.getMinutes() + ":" + rundate.getSeconds();
          triggerargdata[triggerName] = triggerargdata[triggerName].replace("T", " ") + ":00";
          console.log(triggerargdata);
        }
        for (var i = 0; i < integers.length; i++) {
          if (triggerargs[triggerName].id == 'trigger_' + integers[i] && triggerargs[triggerName].value != "") {
            triggerargdata[triggerName] = parseInt(triggerargdata[triggerName]);
          }
        }
      }
    }
    var data = {
      id: elems.id,
      name: elems.name.value,
      object: elems.objectName.value,
      args: [elems.args.value],
      trigger: elems.trigger.value,
      triggerargs: triggerargdata
    };
    console.log(data);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "newJob.php", true);
    const json = {data: JSON.stringify(data)}
    xhr.onreadystatechange = function() {
      if (xhr.status == 200 && xhr.readyState == 4) {
        console.log(xhr.responseText);
        window.onload();
        self.editDiv.parentElement.removeChild(self.editDiv);
      }
    };
    xhr.setRequestHeader("Content-Type","application/json");
    xhr.send(JSON.stringify(json));
  }
};
