<template>
  <div>
    统计所有设备被租借的记录
    <vue-bar-graph
      :points="[1, 4, 5, 3, 4]"
      :show-y-axis="true"
      :show-x-axis="true"
      :width="400"
      :height="200"
      :show-values="true"
      :use-custom-labels="false"
      :labels="['1', 'aaa', 'Mar', 'Abr', 'Mai']"
    />
    
    {{list}}
  </div>
</template>

<script>
//여기서 user 정보를 받아서 나태내는걸 다르게
import NotificationBell from "vue-notification-bell";
import axios from "axios";
import VueBarGraph from 'vue-bar-graph';

export default {
  components: {
    NotificationBell,
    VueBarGraph,
  },
  data() {
    return {
      num:0,
      list: [],
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
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem('super')
      this.$router.push({ name: "Main" });
      alert("logout");
    },
  },
  mounted: function () {
     axios
      .post("api/equip/equiplist/", localStorage.getItem("token"))
      .then((r) => {

        axios.post("api/data_ana/").then((r) => {
          console.log(r);
          data = r.data
        });

        axios.get("api/data_ana/").then((r) => {
          console.log(r);
        });
        // console.log(r.data.list);
        list = data
        }



      )}
      .catch(
        (e) => {
          alert("wrong user");
        })
        // alert3ing();
 
 
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
