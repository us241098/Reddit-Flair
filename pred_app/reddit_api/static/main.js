    //location.reload();
    var ress = window.location.pathname.split("/");
    let tokenn = ress[5];
    const req = new XMLHttpRequest();

    req.open('GET', 'https://zuzu.ai/api/v1/boards');

    req.setRequestHeader("Authorization", "Bearer " + tokenn);
    req.send();

    req.onload = () => {
      if (req.status === 200) {
        console.log("Success"); // So extract data from json and create table
        var data = JSON.parse(req.response);

        //console.log(data['data']);
        data = data['data']
        var data = JSON.parse(data)
        for (var i = 0; i < data.length; i++) {
          console.log(data[i]['_id']['$oid']);
          console.log(data[i]['name']);

          var select_row = document.createElement('option');
          select_row.setAttribute("id", data[i]['_id']['$oid']);
          select_row.innerHTML = data[i]['name'];
          mnm = data[i]['_id']['$oid'];
          document.getElementById("boardMenu").appendChild(select_row);

        }

      }
    }



var res = window.location.pathname.split("/");
let orgID = res[3];
let token = res[5];

var mnm;

function reply_click(clicked_id) {
  const request = new XMLHttpRequest();
  request.open('GET', 'https://gtsfiqqxu6.execute-api.us-east-1.amazonaws.com/dev/' + orgID + '/' + clicked_id + '/deleteJob');
  request.send();
  request.onload = () => {
  if (request.status === 200) {
    location.reload();
  }
}
  
}



function toggle(element) {
console.log('in toggle');
  console.log(element.attributes.syncid.value);
  clicked_id=element.attributes.syncid.value;
  var newstatus='n';

  if (element.checked==false){
    console.log('disabled');
    newstatus='disabled';
  }

  if (element.checked==true){
    console.log('enabled');
    newstatus='enabled';
  }


  const request = new XMLHttpRequest();
  request.open('GET', 'https://gtsfiqqxu6.execute-api.us-east-1.amazonaws.com/dev/' + orgID + '/' + clicked_id + '/updateJob/' + newstatus);
  request.send();
 
}

      
console.log('############')
console.log(mnm);


  document.addEventListener('DOMContentLoaded',function(){
    
  const request = new XMLHttpRequest();
request.open('GET', 'https://gtsfiqqxu6.execute-api.us-east-1.amazonaws.com/dev/' + orgID + '/getJob');
request.send();

request.onload = () => {
  if (request.status === 200) {
    console.log("Success"); // So extract data from json and create table
    var data = JSON.parse(request.response);
    console.log(data.length);
    for (var i = 0; i < data.length; i++) {
      console.log(data[i]);
      var table_row = document.createElement('tr');
      var status=data[i].syncAttributes.jobStatus;
      
      if (status=='enabled'){
        status='checked';

      }

      if (status=='disabled'){
        status=' ';

      }
      var ff;
      
      var a = parseInt(data[i].syncAttributes.lastRun.__Decimal__)
      console.log(a);
      var dd = new Date(a* 1000);
      
      if (data[i].syncAttributes.frequency=='1'){
        ff='Periodic';
      }

      if (data[i].syncAttributes.frequency=='0'){
        ff='One Time'
      }

      
      var ctg=data[i].syncAttributes.filterMetadata.category;
      var sct=data[i].syncAttributes.filterMetadata.section;
      
      if (ctg=='null'){
        ctg='-';
      }

      if (sct=='null'){
        sct='-'
      }


      var bb = data[i].syncAttributes.boardName;
      console.log(bb);


      var str = `          <th scope="row">1</th>
      <td>`+ data[i].syncID + `</td>
      <td>`+ ff + `</td>
      <td>`+ bb + `</td>
      <td>`+ dd + `</td>
      <td>`+ ctg + `</td>
      <td>`+ sct + `</td>
      <td> <button onClick = "reply_click(this.id)" id=` + data[i].syncID + ` type="button" class="btn"> Delete </button> </td>
      <td> <div class="custom-control custom-switch">
      <input onClick = "toggle(this)" ` + status + ` type="checkbox" class="custom-control-input" id = "customSwitch1"  syncid=` + data[i].syncID + `>
      <label class="custom-control-label" for="customSwitch1">Toggle this switch element</label>
    </div></td>`

//button class="btn"><i class="fa fa-trash"></i></button>
  
table_row.innerHTML = str;

      document.getElementById("mydivs").appendChild(table_row);

      }


     
     
     // check every 100ms
        //console.log(data[i].syncAttributes.boardID);
        //var bb = document.getElementById("5e61274e421aa93e39a7d373");
        //console.log(bb);
    }

    //Showing the table inside table

  }


request.onerror = () => {
  console.log("error")
};

    console.log("second function executed");
  }, false);
  








function sendJSONNewJob() {

  var e = document.getElementById("freq");
  var result = e.options[e.selectedIndex];
  var frequency = result.innerHTML;

  e = document.getElementById("boardMenu");
  result = e.options[e.selectedIndex];
  //boardID=result.innerHTML;
  boardID = result.id;
  boardName = result.innerHTML;

  //alert(result.id);

  var res = window.location.pathname.split("/");

  let orgID = res[3];
  let systemID = res[4];
  //let token = res[5];

  result = document.querySelector('.result');
  //let orgID = document.querySelector('#orgID'); 
  //let systemID = document.querySelector('#systemID'); 

  //let boardID = document.querySelector('#boardID');

  let category = document.querySelector('#filterCategory');
  let section = document.querySelector('#filterSection');
  category = category.value;
  section = section.value;

  category = category.split(",");
  section = section.split(",");

  if (frequency === 'One Time') {
    frequency = '0';
  }


  if (frequency === 'Periodic') {
    frequency = '1';
  }


  if (systemID === 'zendesk') {
    systemID = '1';
  }



  var data = JSON.stringify({
    "syncAttributes": {
      "orgID": orgID,
      "boardID": boardID,
      "boardName": boardName,
      "frequency": frequency,
      "systemID": systemID,
      "jobStatus": 'enabled',
      "filterMetadata": {
        "category": category, "section": section
      },
    }
  }
  );

  console.log(data);

  // Creating a XHR object 
  let xhr = new XMLHttpRequest();
  let url = "https://gtsfiqqxu6.execute-api.us-east-1.amazonaws.com/dev/setJob";



  xhr.open("POST", url, true);

  // Set the request header i.e. which type of content you are sending 
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(data);
  console.log('########################################## status')
  // Create a state change callback
  console.log(xhr.status); 

  xhr.onload = () => {
    if (xhr.status === 200) {
      console.log("Success"); // So extract data from json and create table
      var data = JSON.parse(xhr.response);
      console.log(data);
      location.reload();
    }
    
  }



  Swal.fire(
    'Good job!',
    'Job Created',
    'success'
  )

}



function sendJSON() {

  var res = window.location.pathname.split("/");

  let result = document.querySelector('.result');
  let orgID = res[3];
  let systemID = res[4];
  let token = res[5];
  let email = document.querySelector('#email');
  let password = document.querySelector('#password');
  let zendesk = document.querySelector('#zendesk');


  // Creating a XHR object 
  let xhr = new XMLHttpRequest();
  let url = "https://gtsfiqqxu6.execute-api.us-east-1.amazonaws.com/dev/sysConfig";

  // open a connection 
  xhr.open("POST", url, true);

  // Set the request header i.e. which type of content you are sending 
  xhr.setRequestHeader("Content-Type", "application/json");

  // Create a state change callback 
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {

      // Print received data from server 
      result.innerHTML = "System Configured!";

    }
  };

  if (systemID.value === 'zendesk') {
    systemID.value = 1;
  }
  var data = JSON.stringify({
    "sysAttributes": {
      "orgID": orgID,
      "systemID": systemID,
      "status": "enabled",
      "authParam": {
        "email": email.value, "password": password.value, "zendeskDomain": zendesk.value
      },
    }
  }
  );
  console.log(data)
  xhr.send(data);













  let reqToken = new XMLHttpRequest();
  url = "https://gtsfiqqxu6.execute-api.us-east-1.amazonaws.com/dev/tokenConfig";
  reqToken.open("POST", url, true);
  reqToken.setRequestHeader("Content-Type", "application/json");

  reqToken.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {

      // Print received data from server 
      result.innerHTML = "Token Configured!";

    }
  };


  var data = JSON.stringify({
    "orgID": orgID,
    "token": token,
  }
  );

  reqToken.send(data);



} 