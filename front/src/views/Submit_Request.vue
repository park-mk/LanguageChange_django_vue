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
          <h3>申请为提供者</h3>
        </span>
        <v-row>
          <v-col style="text-align: center">
              <v-form>
            <label for="pw"
              ><h5><b>实验室名称</b></h5></label
            >
            <v-text-field
              v-model="form.name"
              label="name"
              outlined
              shaped
              background-color="grey"
            ></v-text-field>
            <label for="pw"
              ><h5><b>能提供的设备</b></h5></label
            >
            <v-textarea
              v-model="form.description"
              label="description"
              outlined
              shaped
              background-color="grey"
            >
            </v-textarea>
            <label for="pw"
              ><h5><b>出借方地址</b></h5></label
            >

            <v-text-field
              v-model="form.location"
              label="location"
              outlined
              shaped
              background-color="grey"
            ></v-text-field>
            <label for="pw"
              ><h5><b>联系方式</b></h5></label
            >

            <v-text-field
              v-model="form.phone_number"
              label="phone_number"
              outlined
              shaped
              background-color="grey"
            ></v-text-field>
            </v-form>
            <v-btn @click="submit">submit</v-btn>
          </v-col>
        </v-row>
      </div>
    </div>
  </v-parallax>
</template>

<script>

import axios from 'axios'
export default {
  data() {
    return {
        form:{
            name:'',
            location:'',
            description:'',
            phone_number:''
        }
    };
  },
  methods: {
    submit() {
      //post
      console.log(this.$http)
      console.log(this.form);
      this.form['provider_id'] = 19
      console.log(this.form)
      axios
        .post('api/equip/add',this.form)
        .then((response) => {
          console.log(response)
        })
        .catch((ex) => {
          console.warn("ERROR!!!!! : ", ex);
        });
    },
  },
};
</script>

<style scoped>
/* Bordered form */

v-text-area {
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
