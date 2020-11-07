<template>
  <v-parallax dark src="../../public/images/main_5.jpg" id="par">
    <img id="dog" src="../../public/images/logo.svg" height="150" width="150" />
    <v-card>
      <v-card-title>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="desserts"
        sort-by="username"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>用户管理</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="headline">用户申请内容</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-container>
                      <v-row>
                        <h4>申请用户： {{ name }}</h4>
                      </v-row>

                      <br />
                      <v-row>
                        <h4>学号： {{ userid }}</h4>
                      </v-row>

                      <br />
                      <v-row>
                        <h4>申请理由： {{ reason }}</h4>
                      </v-row>
                    </v-container>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="deny(editedItem)"
                    >Deny</v-btn
                  >
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="up_staff(editedItem)"
                    >Accept</v-btn
                  >
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          
          <v-icon class="mr-2" small @click="deleteItem(item)">
            mdi-delete
          </v-icon>
          <v-icon small class="mr-2" @click="rowClick(item)">
            mdi-account-details
          </v-icon>
          <v-icon
            small
            class="mr-2"
            @click="down_staff(item)"
            v-if="item.is_staff == 2"
          >
            mdi-arrow-down-thick
          </v-icon>
          <v-icon
            small
            class="mr-2"
            @click="up_staff(item)"
            v-if="item.is_apply_a == true"
          >
            mdi-dots-horizontal
          </v-icon>

          <v-icon
            small
            class="mr-2"
            @click="searching(item)"
            v-if="item.is_apply_a == true"
          >
            mdi-alert-circle
          </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-parallax>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    reason: "",
    name: "",
    userid: "",
    lab: "",
    phone_number: "",
    search: "",
    dialog: false,
    headers: [
      { text: "名字", value: "username" },
      { text: "学号", value: "userid" },
      { text: "用户类型", value: "usertype" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    desserts: [],
    d: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {},
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.desserts = [];
    },
    searching(item) {
      console.log(item);
      this.name = item.username;
      this.userid = item.userid;
      this.reason = item.reason_pro;
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    editItem(item) {
      let form = {};
      let reason;
      form["userid"] = item.userid;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/apply_userinfo/", form)
        .then((r) => {
          //console.log(r)
          this.reason_pro = r.data.reason_pro;
          //this.lab = r.data.reason_a.split('#')[1]
          //  this.phone_number = r.data.reason_a.split('#')[2]
          //console.log(reason[0])
        })
        .catch((e) => {
          alert("wrong user");
        });
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      //this.editedItem['reason'] = reason[0]
      //console.log( reason)
      // this.editedItem['lab'] = reason[1]
      // this.editedItem['phone_number'] = reason[2]
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.desserts.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.desserts.splice(index, 1);
      let form = {};
      form["userid"] = item.userid;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/delete/", form)
        .then((r) => {
          console.log(r);
        })
        .catch((e) => {
          alert("wrong user");
        });
      //location.reload();
    },

    deny(item) {
      let form = {};
      form["userid"] = item.userid;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/deny_apply_a/", form)
        .then((r) => {
          console.log(r);
        })
        .catch((e) => {
          alert("wrong user");
        });
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
      location.reload();
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
      } else {
        this.desserts.push(this.editedItem);
      }
      this.close();
    },
    down_staff(item) {
      let form = {};
      form["userid"] = item.userid;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/statusdown/", form)
        .then((r) => {
          console.log(r);
          location.reload();
        })
        .catch((e) => {
          alert("wrong user");
        });
    },
    up_staff(item) {
      console.log(item);
      let form = {};
      form["userid"] = item.userid;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/statusup/", form)
        .then((r) => {
          console.log(r);
          this.dialog = false;
          this.$nextTick(() => {
            this.editedItem = Object.assign({}, this.defaultItem);
            this.editedIndex = -1;
            location.reload();
          });
        })
        .catch((e) => {
          alert("wrong user");
        });
    },
    rowClick(items) {
      console.log("post_view/" + items.id);
      this.$router.push("/my_info/" + items.userid);

      // this.$router.push("/post_view/" + items.id);
      //this.$router.push({ params:{id:items.id}});
    },
  },
  mounted: function () {
    axios
      .post("api/userslist/", localStorage.getItem("token"))
      .then((r) => {
        console.log(r.data.list);
        this.d = r.data.list;
        console.log("aaaa", this.d.length);
        console.log(this.d[0].is_staff);
        for (let i = 0; i < this.d.length; i++) {
          if (this.d[i].is_apply_a == true) {
            this.d[i]["usertype"] = "普通用户申请设备提供者";
          } else if (this.d[i].is_staff == 2) {
            this.d[i]["usertype"] = "设备提供者";
            console.log("2 success");
          } else if (this.d[i].is_staff == 3) {
            this.d[i]["usertype"] = "普通用户";
            console.log("2 success");
          }
        }
        this.desserts = this.d;

        console.log(this.d);
        console.log(typeof r.data);
        //  let parsing = JSON.parse(r.data)
        //  console.log (parsing)
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

<style>
#par {
  height: 1000px !important;
}
</style>
