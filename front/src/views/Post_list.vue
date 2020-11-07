<template>
  <v-container>
   <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
  
    <v-data-table
      :headers="headers"
      :items="desserts"
      :items-per-page="15"
      hide-default-footer
      class="elevation-1"
      @click:row="rowClick"
      :loading="loadingtf"
      loading-text="Loading... Please wait"
     key = "tablekey"
     :search="search"
    >
    </v-data-table>
   
    <v-row>
      <v-btn outlined color="blue" @click="writeClick"> 创建<v-icon>mdi-pen</v-icon> </v-btn>
      <v-btn outlined color="blue" @click="previousClick"> <v-icon>mdi-skip-previous</v-icon>下一页 </v-btn>
      <v-btn outlined color="blue" @click="nextClick"> 上一页 <v-icon>mdi-skip-next</v-icon></v-btn>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import Vue from "vue";

let created_time;
let time;
let total;
let path;
export default {
  name: "Post_List",
  data() {
    return {
        search: '',
        tablekey:0,
      loadingtf: true,
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
      desserts: [{}],
    };
  },
  created() {
    path = window.location.href;
    path = path.split("#");
    path[1] = path[1].slice(11);
    //console.log(path[1]);
    this.fetch();
  },
  methods: {
    fetch() {
      axios
        .get(`http://simplebbs.iterator-traits.com/api/v1/post?page=1&size=1`, {
          headers: {
            Authorization: this.$store.state.token,
          },
        })
        .then((r) => {
          total = r.data.total;
            localStorage.setItem('total',total);

          this.get_data();
        })
        .catch((e) => {
             alert('error')

          console.log("not working");
        });
    },
    get_data() {
                this.loadingtf = true;

      let info = {};
      let result_table = [];

      axios
        .get(
          `http://simplebbs.iterator-traits.com/api/v1/post?page=` +
            path[1] +
            "&size=15",
          {
            headers: {
              Authorization: this.$store.state.token,
            },
          }
        )
        .then((r) => {


          for (let i = 0; i < 15; i++) {
            info[i] = new Object();
          }
          for (let i = 0; i < 15; i++) {
            info[i].id = r.data.posts[i].id;

            info[i].content = r.data.posts[i].content;
            created_time = r.data.posts[i].created.split("T");
            time = created_time[1].split("+");
            info[i].created = created_time[0] + "/" + time[0];
            info[i].nickname = r.data.posts[i].nickname;
            info[i].title = r.data.posts[i].title;
            info[i].updated = r.data.posts[i].updated;
            info[i].userId = r.data.posts[i].userId;
          }
          for (let i = 0; i < 15; i++) {
            result_table.push(info[i]);
          }
          this.desserts = result_table;
         // console.log(this.desserts);

          this.loadingtf = false;
                 

        })
        .catch((e) => {
                       alert('error');

          console.log("error");
        });
    },
    forceRerender(){
        this.tablekey +=1;
        console.log('forcererender')
    },
    nextClick() {
      if (total / 15 > Number(path[1])) {
        path[1] = Number(path[1]) + 1;
        //console.log(path[1]);
        this.$router.push("/post_list/" + path[1]);
        this.get_data();
      }
    },
    previousClick() {
      if (Number(path[1]) > 1) {
        path[1] = Number(path[1]) - 1;
        //console.log(path[1]);
        this.$router.push("/post_list/" + path[1]);
        this.get_data();
      }
    },
    writeClick() {
      this.$router.push("/post_write");
    },
    rowClick(items) {
      console.log( "post_view/" + items.id);
      this.$router.push("/post_view/" + items.id);

      // this.$router.push("/post_view/" + items.id);
      //this.$router.push({ params:{id:items.id}});
    },
  },
};
</script>
