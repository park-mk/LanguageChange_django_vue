<!--<template>
<div>
 <v-alert type="success">
      I'm a success alert.
    </v-alert> -->
  
<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col><h1>你好 {{ nickname }} </h1></v-col>
        <v-col>
          <v-btn block outlined color="blue" @click="signOut"
            >登出<v-icon>mdi-logout</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        
        <v-col>
          <v-row><h2> 收藏 </h2></v-row>
          <v-row>
            <v-data-table
            :headers="headers"
      :items="bookmark"
       :loading="bookmark_loadingtf"
      loading-text="Loading... Please wait"
      @click:row="rowClick"
      >
            </v-data-table>
          </v-row>
          </v-col>
          <v-col>
          <v-row> <h2>浏览记录</h2> </v-row>
          <v-row>
            <v-data-table
            :headers="headers"
      :items="history"
       :loading="history_loadingtf"
      loading-text="Loading... Please wait"
      @click:row="rowClick"
      >
            </v-data-table>
          </v-row>
          </v-col>
          
      </v-row>
    </v-container>
  </v-form>
</template>
<script>
import axios from "axios";
let created_time;
let time;
export default {
  name: "Info",
  data() {
    return {
      history_loadingtf:true,
      bookmark_loadingtf:true,
      total:localStorage.getItem('total'),
      nickname: "",
      username: "",
      created: "",
      id: "",
       headers: [
        {
          text: "时间",
          value: "created",
        },

        {
          text: "用户名",
          value: "nickname",
        },
        {
          text: "标题",
          value: "title",
        },
      ],
      bookmark:[],
      history:[],

    };
  },
  created() {
    this.fetch();
  },
  methods: {
    fetch() {
      axios
        .get(`http://simplebbs.iterator-traits.com/api/v1/user`, {
          headers: {
            Authorization: this.$store.state.token,
          },
        })
        .then((r) => {
          console.log(r.data);
          this.nickname = r.data.nickname;
          this.username = r.data.username;
          this.created = r.data.created;
          this.id = r.data.id;

        })
        .catch((e) => console.log(e));
        
        
        
    
        
        
        
        axios
        .get(`http://simplebbs.iterator-traits.com/api/v1/post?page=1&size=`+this.total.toString(), {
          headers: {
            Authorization: this.$store.state.token,
          },
        })
        .then((r) => {
             this.history_loadingtf = true;

      let info = {};
      let replace_history = [];
            let replace_bookmark = [];

          //console.log(r.data);
         
         
          for (let i = 0; i < this.total; i++) {
            info[i] = new Object();
            //console.log("new");
          }
          for (let i = 0; i < this.total; i++) {
            info[i].id = r.data.posts[i].id;

            //info[i].content = r.data.posts[i].content;
            created_time = r.data.posts[i].created.split("T");
            time = created_time[1].split("+");
            info[i].created = created_time[0] + "/" + time[0];
            info[i].nickname = r.data.posts[i].nickname;
            info[i].title = r.data.posts[i].title;
            info[i].userId = r.data.posts[i].userId;
          }
         
         let history=localStorage.getItem('history')
         history = history.split(',');
            //console.log(history.length);
            for(var a=0;a<history.length;a++){
              //console.log('hey')
              for( var i=0;i<this.total;i++){
                   if(Number(history[a])===Number(info[i].id)){
                       console.log("my history",info[i].id);
                       replace_history.push(info[i]);
                   }

              }
            }

            this.history = replace_history;
              this.history_loadingtf = false;
              
              
              
              
              
              
              
              let bookmark=localStorage.getItem('bookmark')
         bookmark = bookmark.split(',');
            console.log(bookmark.length);
            for(var a=0;a<bookmark.length;a++){
              console.log('hey')
              for( var i=0;i<this.total;i++){
                   if(Number(bookmark[a])===Number(info[i].id)){
                       console.log("my history",info[i].id);
                       replace_bookmark.push(info[i]);
                   }

              }
            }
              
              
              
              
              
              
              this.bookmark = replace_bookmark;
              this.bookmark_loadingtf = false;

        })
        .catch((e) => {
          console.log("not working");
        });
        
    },
    rowClick(items) {
      console.log( "post_view/" + items.id);
      this.$router.push("/post_view/" + items.id);

      // this.$router.push("/post_view/" + items.id);
      //this.$router.push({ params:{id:items.id}});
    },
    signOut() {
      axios
        .patch(
          `http://simplebbs.iterator-traits.com/api/v1/logout`,
          { username: "2016080044" },
          {
            headers: {
              Authorization: this.$store.state.token,
            },
          }
        )
        .then((r) => {
          //console.log(r.data);
          this.$store.commit("delToken");
          this.$router.push({ name: "Main" });
          alert("logout");
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
