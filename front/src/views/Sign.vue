<template>
  <v-parallax dark src="../../public/images/main_5.jpg" id="par">
    <div id="login_page">
      <div class="container">
        <span key="first" id="logo">
          <img
            id="dog"
            src="../../public/images/logo.svg"
            height="150"
            width="150"
          />
          <h3>清华设备借组系统</h3>
        </span>
        <!-- <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>清华BBS</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="form.username"
                label="用户名"
                type="text"
              ></v-text-field>
              <v-text-field
                v-model="form.password"
                label="密码"
                type="password"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="signIn">登录<v-icon>mdi-login</v-icon></v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout> -->
        <label for="id"
          ><h5><b>ID</b></h5></label
        >
        <p></p>
        <input
          type="text"
          v-model="form.userid"
          placeholder="Enter ID"
          name="id"
          required
        />
        <p></p>
        <label for="pw"
          ><h5><b>Password</b></h5></label
        >
        <p></p>
        <input
          type="password"
          v-model="form.password"
          placeholder="Enter Password"
          name="pw"
          required
        />
        <p></p>
        <div id="space"></div>
        <button type="submit" v-on:click="login_button" id="login">
          <b>Login</b>
        </button>
        <router-link :to="{ name: 'sign_up' }">
          <button type="button" class="sign_up">
            <b>Sign up</b>
          </button></router-link
        >
        <p></p>
      </div>
    </div>
  </v-parallax>
</template>

<script>
import axios from "axios";
import Info_me from "./Info_me";
import jwtDecode from "jwt-decode";
import Vue from "vue";

export default {
  name: "Sign",
  data() {
    return {
      form: {
         userid:'',
         password:''
      },
     
    };
  },
  methods: {

    login_button(){
      console.log('aaaa',this.form)
      axios.post('api/login/',this.form)         
      .then((r) => {
           console.log(r.data);
           localStorage.setItem("token", r.data.token);
           localStorage.setItem("userid",r.data.userid);
            localStorage.setItem("username",r.data.username);

           this.$router.push({ name: "home" });
           
    }).catch(
          (e) => {
          alert('wrong user')}
        ); //에러뜨면 알람
    },
  },
      
  
  mounted: function () {
    if (localStorage.getItem('token')!==null) {
      console.log("fuckyou");
      this.$router.push({ name: "home" });
    }
    
    
  }
    
}
    
   
  

</script>

<style scoped>
/* Bordered form */

form {
  border: 3px solid #f1f1f1;
}

* {
  text-align: center;
}

#par {
  height: 1000px !important;
}
#login_page {
  content: "";
  position: relative;
  top: 0;
  left: 0;
  margin: 0px 0px 60px 0px;
  width: 100%;
  height: 100%;
  opacity: 0.5;
  z-index: -1;
  background-repeat: no-repeat;

  background-size: cover;

  background-image: url("../../public/images/main_5.jpg");
}

/* Full-width inputs */

input[type="text"],
input[type="password"] {
  width: 30%;
  padding: 12px 20px;
  margin: 5px 5px 5px 5px;
  display: inline-block;
  border: 2px solid grey;
  box-sizing: border-box;
  border-radius: 8px;
}

/* Set a style for all buttons */

button {
  width: 15%;
  background-color: none;
  color: black;
  padding: 14px 20px;
  margin: 8px 10px;
  border: 2px solid green;
  border-radius: 8px;
  cursor: pointer;
}

/* Add a hover effect for buttons */

button:hover {
  opacity: 0.8;
  background-color: red;
  color: white;
}

#login:hover {
  opacity: 0.8;
  background-color: green;
  color: white;
}

#space {
  margin: 50px 50px 25px 100px;
}

/* Extra style for the cancel button (red) */

.sign_up {
  width: 15%;
  border: 2px solid red;
}

/* Add padding to containers */

/* The "Forgot password" text */

span.psw {
  padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */

@media screen and (max-width: 300px) {
  span.psw {
    display: block;
    float: none;
  }
  .cancelbtn {
    width: 100%;
  }
}

@media (max-width: 768px) /*768 보다 작으면*/ {
  button {
    width: 15%;
    background-color: none;
    color: black;
    padding: 0px 0px;
    margin: 0px 10px;
    border: 2px solid green;
    border-radius: 8px;
    cursor: pointer;
  }
}
</style>
