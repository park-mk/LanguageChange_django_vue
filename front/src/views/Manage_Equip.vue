<template>
  <v-parallax dark src="../../public/images/main_5.jpg" id="par">
    <router-link :to="{ name: 'home' }">
      <img
        id="dog"
        src="../../public/images/logo.svg"
        height="150"
        width="150"
        style="float: left"
      />
    </router-link>
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
            <v-toolbar-title>设备管理</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
<v-dialog v-model="dialog_new" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.name"
                        label="设备名称"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.location"
                        label="地址"
                      ></v-text-field>
                    </v-col>
                    <v-text-field
                      v-model="editedItem.description"
                      label="用途"
                    ></v-text-field>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.phone_number"
                        label="联系方式"
                      ></v-text-field>
                    </v-col>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close"
                    >Cancel</v-btn
                  >
                  <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.confirm="{ item }">
          <v-icon
            small
            @click="confirm_return(item)"
            v-if="item.is_return == true"
          >
            mdi-check-circle
          </v-icon>
        </template>
          





        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon
            small
            class="mr-2"
            @click="down_staff(item)"
            v-if="
              item.is_on == true &&
              item.is_active == true &&
              item.is_rent == '未租借'
            "
          >
            mdi-arrow-down-thick
          </v-icon>
          <v-icon
            small
            class="mr-2"
            v-if="item.is_on == true && item.is_active == false"
            @click="up_staff(item)"
          >
            mdi-dots-horizontal
          </v-icon>

          <v-icon class="mr-2" small @click="deleteItem(item)">
            mdi-delete
          </v-icon>
          <v-icon small class="mr-2" @click="rowClick(item)">
            mdi-account-details
          </v-icon>
          <v-icon small v-if="item.is_apply == true"> mdi-alert-circle </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-parallax>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    search: "",
    dialog: false,
    dialog_new: false,
    headers: [
      { text: "设备名称", value: "name" },
      { text: "设备状态", value: "equiptype" },
      { text: "是否租借", value: "is_rent" },

      { text: "确认归还", value: "confirm" },

      { text: "Actions", value: "actions", sortable: false },
    ],
    desserts: [],
    d: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      location: "",
      description: "",
      phone_number: "",
    },
    defaultItem: {},
    name: "",
    phone_number: "",
    description: "",
    location: "",
    is_return: false,
    borrow_from: "",
    user_id: "",
    list: [],
    is_gelai: 0,
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

    confirm_return(item) {
      let com_start;
      let data = {};
      let com_reason;
      console.log("아이템아이디", item);
      let set = {};
      let wrap = {};
      set["equipid"] = item.id;
      set["aaa"] = 0;
      axios.post("api/equip/view_wait/", set).then((r) => {
        console.log("제발", r.data.list);
        console.log(item);
        let today = new Date();
        let year = today.getFullYear();
        let month = today.getMonth() + 1;
        let date = today.getDate();
        if (Number(month) < 10) {
          month = "0" + month;
        }
        let this_day = year + "/" + month + "/" + date;
        data["equip_name"] = item.name;

        data["equip_id"] = item.id;
        data["borrow_till"] = this_day;
        com_start = r.data.list[0].rent_start.split("T");
        data["borrow_from"] = com_start[0];
        data["user_id"] = r.data.list[0].user_id;
        data["borrow_from"] = data["borrow_from"].replace(/-/g, "/");
        console.log(data);

        ///이큅히스토리
        axios.post("api/equip/view_wait/", set).then((r) => {
          console.log(r);
          //wrap = data;
          com_reason = r.data.list[0].reason.split("#");
          wrap["reason"] = com_reason[0];
          wrap["userid"] = data["user_id"];
          wrap["rent_start"] = data["borrow_from"];
          wrap["rent_exp"] = data["borrow_till"];
          wrap["user_name"] = r.data.list[0].user_name;
          wrap["equip_name"] = item.name;
          wrap["equip_id"] = item.id;
          data["user_name"] = r.data.list[0].user_name;
          axios.post("api/equip/return_equip_check/", data).then((r) => {
            console.log(r);
            console.log("wrap", wrap);

            axios.post("api/allow_return/", wrap).then((r) => {
              console.log(r);

              let info = {};

              info["is_rent"] = false;
              info["rent_status"] = 0;
              info["userid"] = wrap["userid"];
              console.log("info", info);
              axios.post("api/update_user_status/", info).then((r) => {
                let equip_info = {};
                equip_info["is_rent"] = false;
                equip_info["is_return"] = false;
                equip_info["is_gelai"] = 1;
                equip_info["equip_id"] = item.id;
                axios.post("api/equip/wujun_is/", equip_info).then((r) => {
                  console.log(r);
                });

                item.is_return = "";
                item.is_rent = "未租借";
                console.log(r);
              });
            });
          });
        });
      });
    },

    editItem(item) {
      ///////////////////장비 수정
      console.log(item);
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog_new = true;
    },

    pendingItem(item) {
      let form = {};
      let reason;
      form["equipid"] = item.id;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/equip/rentdescription/", form)
        .then((r) => {
          console.log(r);
          this.description = r.data.description;
          this.location = r.data.location;
          this.name = r.data.name;
          this.phone_number = r.data.phone_number;
        })
        .catch((e) => {
          alert("wrong user");
        });
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog_new = true;
    },

    deleteItem(item) {
      const index = this.desserts.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.desserts.splice(index, 1);
      let form = {};
      form["equipid"] = item.id;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/equip/delete/", form)
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
      form["equipid"] = item.id;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/equip/deny/", form)
        .then((r) => {
          console.log(r);
        })
        .catch((e) => {
          alert("wrong user");
        });
      this.dialog_new = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
      //location.reload();
    },
    close() {
      this.dialog_new = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    save() {
      console.log(this.editedItem);
      let wrap = {};
      //wrap['equipid'] = this.editedItem.id
      //console.log(this.editedItem.id)
      wrap["name"] = this.editedItem.name;
      wrap["description"] = this.editedItem.description;
      wrap["location"] = this.editedItem.location;
      wrap["provider_id"] = localStorage.getItem("userid");

      console.log(wrap);

      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
        this.close();

        axios
          .post("api/equip/update/" + this.editedItem.id, wrap)
          .then((r) => {
            console.log(r);
            //location.reload()
          })
          .catch((e) => console.log(e));
      } else {
        axios
          .put("api/equip/equiplist/", wrap)
          .then((r) => {
            console.log(r);
            location.reload();
          })
          .catch((e) => console.log(e));
        this.desserts.push(this.editedItem);
      }
    },
    down_staff(item) {
      //   let form = {};
      //   form["userid"] = Number(item.userid);
      //   form["token"] = localStorage.getItem("token");
      //   console.log(form);
      axios
        .get("api/equip/off/" + item.id)
        .then((r) => {
          console.log(r);
          location.reload();
        })
        .catch((e) => {
          alert("wrong user");
        });
    },
    up_staff(item) {
      console.log(item.id);
      //let form = {};
      // form["userid"] = Number(item.id);
      //form["token"] = localStorage.getItem("token");
      //console.log(form);
      axios
        .get("api/equip/super_on_equip/" + item.id)
        .then((r) => {
          console.log(r);
          this.dialog_new = false;
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
      console.log("equip_info/" + items.id);
      this.$router.push("/equip_info/" + items.id);

      // this.$router.push("/post_view/" + items.id);
      //this.$router.push({ params:{id:items.id}});
    },
  },
  mounted: function () {
    axios
      .post("api/equip/equiplist/", localStorage.getItem("token"))
      .then((r) => {
        console.log(r);
        this.d = r.data.list;
        console.log("aaaa", this.d.length);
        //console.log(this.d[0].is_staff)

        for (let i = 0; i < this.d.length; i++) {
          if (this.d[i].is_on == true && this.d[i].is_active == true) {
            this.d[i]["equiptype"] = "上架";
            console.log("2 success");
          } else if (this.d[i].is_on == true && this.d[i].is_active == false) {
            this.d[i]["equiptype"] = "上架申请中";
            console.log("2 success");
          } else {
            this.d[i]["equiptype"] = "下架";
            console.log("fail");
          }
          if (this.d[i].is_rent == true) {
            this.d[i]["is_rent"] = "租借中";
          } else {
            this.d[i]["is_rent"] = "未租借";
          }
          // if (this.d[i].waiting_list.length > 0) {
          //   this.d[i].is_apply = true;
          // } else {
          //   this.d[i].is_apply = false;
          // }
        }
        this.desserts = this.d;

        console.log(this.d);
        console.log(typeof r.data);
        axios.post("api/data_ana/").then((r) => {
          console.log(r);
        });
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
