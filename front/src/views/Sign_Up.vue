<template>
  <div id="app">
    <section class="banner-area" id="home">
      <div class="container">
        <div class="about-content col-lg-12">
          <h1
            class="text-white"
            style="font-size: 40px; color: white; line-height: 200px"
          >
            Become a User
          </h1>
          <p class="text-white"><span class="lnr lnr-arrow-right"></span></p>
          <router-link :to="{ name: 'Main' }">Go to Login</router-link>
        </div>
      </div>
    </section>
    <h2 style="line-height: 100px">Want to help? Become a User.</h2>
    <div id="join_form">
      <label for="id"><b>清华工号</b></label>
      <input type="text" v-model="id" placeholder="Enter ID" required="" />
      <br />
      <label for="pw"><b>密码</b></label>
      <input
        type="password"
        v-model="pw"
        placeholder="Password length must be 6 to 12"
        required=""
      />

      <br />
      <label for="user_name"><b>名字</b></label>
      <input
        type="text"
        v-model="user_name"
        placeholder="Enter User name"
        required=""
      />
      <br />

      <label for="email"><b>邮箱</b></label>
      <input
        type="text"
        v-model="email"
        placeholder="Enter email"
        maxlength="100"
        required=""
      />
      <br />
      <button type="submit" id="submit" v-on:click="sign_up_button">
        Sign Up
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      id: "",
      pw: "",
      pw2: "",
      user_name: "",
      nickname: "",
      address: "",
      detail_address: "",
      p_num: "",
      email: "",
    };
  },

  methods: {
    sign_up_button() {
        let form = {}
        form['username'] = this.user_name
        form['userid'] = this.id
        form['email'] = this.email
        form['password'] = this.pw
        console.log(form)
        axios.post('api/register/',form)
        .then((r) => {
            console.log(r)
            alert('可以在邮箱继续进行账户验证')
        }).catch((e)=>{console.log('error')})
        
    },
  },
};
</script>

<style scoped>
* {
  text-align: center;
}
.banner-area {
  background: url(../../public/images/banner-bg.jpg) center;
  background-size: cover;
  width: 100%;
  height: 400px;
  line-height: 100px;
  margin: 0 auto;
}
#submit {
  background-color: gray;
  border-radius: 15px;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 80px;
  height: 30x;
}
input {
  margin: 5px 0px 10px 5px;
  width: 200px;
  border-radius: 8px;
  border: 1px solid burlywood;
}
</style>
