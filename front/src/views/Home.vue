<template>
  <v-parallax dark src="../../public/images/main_5.jpg" id="par">
    <div id="login_page">
      <div class="container">
        <v-row>
          <notification-bell
            iconColor="yellow"
            counterLocation="lowerRight"
            count="1"
            style="float: right"
          />
          <v-btn v-on:click="logout">登出</v-btn>
        </v-row>
        <span key="first" id="logo">
          <img
            id="dog"
            src="../../public/images/logo.svg"
            height="150"
            width="150"
          />
          <h3>清华设备借组系统</h3>
        </span>
        <div class="manager" v-show="manager_display">
          <v-col>
            <router-link :to="{ name: 'manage_user' }">
              <v-btn v-on:click="user_manage">用户管理</v-btn>
            </router-link>
          </v-col>

          <v-col>
            <router-link :to="{ name: 'manage_equip' }">
              <v-btn v-on:click="equip_manage">设备管理</v-btn>
            </router-link>
          </v-col>
          <v-col>
            <router-link :to="{ name: 'analysis' }">
            <v-btn>数据统计</v-btn>
            </router-link>
          </v-col>
        </div>
        <div class="user" v-show="user_display">
          <v-col>
              <v-btn @click = my_info>我的信息</v-btn>
          </v-col>
          <v-col>
            <router-link :to="{ name: 'rent_equip' }">
              <v-btn v-on:click="rent_manage">租借设备</v-btn>
            </router-link>
          </v-col>
        </div>
        <div class="provider" v-show="provider_display">
          <v-col>
              <v-btn @click = my_info>我的信息</v-btn>
          </v-col>
          <v-col>
            <router-link :to="{ name: 'my_equip' }">
              <v-btn v-on:click="equip_manage">我的设备</v-btn>
            </router-link>
          </v-col>
          <v-col>
            <router-link :to="{ name: 'rent_equip' }">
              <v-btn>租借设备</v-btn>
            </router-link>
          </v-col>
        </div>
      </div>
    </div>
  </v-parallax>
</template>

<script>
//여기서 user 정보를 받아서 나태내는걸 다르게
import NotificationBell from "vue-notification-bell";
import axios from "axios";
export default {
  components: {
    NotificationBell,
  },
  data() {
    return {
      id: "",
      pw: "",
      token1: {
        token: "11",
        token3: "",
      },
      is_staff: 0,
      ttt: "",
      user: {
        userid: 0,
      },
      manager_display: false,
      user_display: false,
      provider_display: false,
    };
  },
  methods: {
    my_info(){
      this.$router.push("/my_info/" + localStorage.getItem("userid"));
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem('super')
      this.$router.push({ name: "Main" });
      alert("logout");
    },
  },
  mounted: function () {
    axios
      .post("api/send_user_status/", localStorage.getItem("userid"))
      .then((r) => {
        console.log(r.data);
        this.is_staff = r.data.is_staff;
        if (this.is_staff == 1) {
          this.manager_display = true;
          localStorage.setItem('super',1)
        } else if (this.is_staff == 2) {
          this.provider_display = true;
        } else {
          this.user_display = true;
        }
      })
      .catch(
        (e) => {
          alert("wrong user");
        }
        // alert3ing();
      ); //에러뜨면 알람
  },
};
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
#login_page:after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  margin: 0px 0px 60px 0px;
  width: 100%;
  height: 155%;
  opacity: 0.5;
  z-index: -1;
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
notification-bell {
}
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
