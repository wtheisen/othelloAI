
$(document).ready(function() {

  $("#logout-button").click(function() {
    console.log("yo");
    $.ajax({
      type: "POST",
      url: "http://group02.dhcp.nd.edu:" + location.port + "/othello/logout",
      success: function(data){
        console.log(data);
        if (data['result'] == 'success') {
          $("#username-p").text("You have been logged out.");
        } else {
          $("#username-p").text("Logout Failed"); 
        }
      }
    }); 
  });

  $("#reg-button").click(function() {

    name = $("#login_username").val();

    data = {
      username: $("#login_username").val(),
      password: $("#login_password").val()
    }

    if (data['password'].length < 5) {
      console.log("here");
      $("#username-p").text("register failed. Password needs to be at least 5 characters long");
      return;
    }
    
    console.log(data);
    console.log("click");
    $.ajax({
      type: "POST",
      url: "http://group02.dhcp.nd.edu:" + location.port + "/othello/register",
      data: data, 
      success: function(data){
        console.log(data);
        if (data['result'] == 'success') {
          $("#username-p").text("Welcome, " + name);
        } else {
          $("#username-p").text("Registration failed"); 
        }
      }
    });
  });

  $("#login-button").click(function() {
    name = $("#login_username").val();
    data = {
      username: $("#login_username").val(),
      password: $("#login_password").val()
    }
    
    if (data['password'].length < 5) {
      console.log("password too short login");
      $("#username-p").text("login failed. Password needs to be at least 5 characters long");
      return;
    }

    console.log(data);
    console.log("click");
    $.ajax({
      type: "POST",
      url: "http://group02.dhcp.nd.edu:" + location.port + "/othello/login",
      data: data, 
      success: function(data){
        console.log(data);
        if (data['result'] == 'success') {
          $("#username-p").text("Welcome, " + name);
        } else {
          $("#username-p").text("Login failed"); 
        }
      }
    });
  });


});

function get_user_stats() {
    $.ajax({
      type: "GET",
      url: "http://group02.dhcp.nd.edu:" + location.port + "/othello/userinfo",
      success: function(data){
        console.log(data);
        if (data['result'] == 'success') {
          $("#username-p").text(data["username"]);
        } else {
          $("$username-p").text("failure");
          //$("#username-p").text("Login failed"); 
        }
      }
    });
}
