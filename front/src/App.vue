<template>

<v-app>
      <router-view />
    
    </v-app>
  
</template>

<script>
import Sign from "./views/Sign";
import Vue from 'vue'
import VueAudio from 'vue-audio-better'
import axios from 'axios'
// async function move_info(){
//   if(this.$store.state.token)
// {
//   console.log('fuckyou');
//     this.$router.push({ name: 'info'})

// }

// }
// move_info();
Vue.prototype.$http = axios

export default {
  name: "App",
  data() {
    return {
      drawer: null,
      items: [
        {
          icon: "mdi-account-tie",
          title: "信息",
          to: {
            path: "/info",
          },
        },
        {
          icon: "mdi-forum",
          title: "论坛",
          to: {
            path: "/post_list/1",
          },
        },
        
      ],
      title: this.$apiRootPath,
    };
  },
  mounted() {},
  methods: {
    signOut() {
      // localStorage.removeItem('token')
      console.log("logout!!!");
      this.$store.commit("delToken");
      this.$router.push("/");
    },
    play(){
      
    }
 
  },

  
};

</script>
