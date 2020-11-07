<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="desserts"
      :items-per-page="5"
      class="elevation-1"
      @click:row="rowClick"
      :loading="loadingtf"
      loading-text="Loading... Please wait"
      key = "tablekey"
    >
    </v-data-table>
    <v-row>
      <v-btn outlined color="blue" @click="listClick"> 目录<v-icon>mdi-menu</v-icon> </v-btn>
    </v-row>
  </v-container>
</template>
<script>
import axios from "axios";

let created_time;
let time;
let total;
let path;
export default {
  name: "User_View",
  data() {
    return {
        tablekey :0,
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
    console.log(path[1],'ttttt');
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
          console.log(r.data);
          console.log("fuckkkkk");
          total = r.data.total;
          console.log(total);

          this.get_data();
          console.log("fuckkkkk");
        })
        .catch((e) => {
          console.log("not working");
        });
    },
    get_data() {
      let info = {};
      let result_table = [];
      console.log("working????");

      axios
        .get(
          `http://simplebbs.iterator-traits.com/api/v1/post?size=` +total,
          {
            headers: {
              Authorization: this.$store.state.token,
            },
          }
        )
        .then((r) => {
          console.log("working????");

          console.log(r.data);

          for (let i = 0; i < total; i++) {
            info[i] = new Object();
            console.log("new");
          }
          for (let i = 0; i < total; i++) {
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
          for (let i = 0; i < total; i++) {
              if(Number(path[1])===info[i].userId)
            result_table.push(info[i]);
          }
          this.desserts = result_table;
          console.log(this.desserts);

          this.loadingtf = false;
        })
        .catch((e) => {
          console.log("error");
        });
    },
    
    listClick() {
      this.$router.push("/post_list/1");
    },
    rowClick(items) {
      console.log( "post_view/" + items.id);
      this.$router.push("/post_view/" + items.id);

     
    },
  },
};
</script>
