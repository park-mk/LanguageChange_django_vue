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
            <v-toolbar-title>租借管理</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      设备名称： {{ equip_name }}
                      <br />
                      租借人： {{ rent_user_name }}
                      <br />
                      用途： {{ reason }}
                      <br />
                      租借开始： {{ rent_start }}
                      <br />
                      租借结束： {{ rent_exp }}
                    </v-row>
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
                    @click="save(editedItem)"
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
           <v-icon
        small
        class="mr-2"
        @click="rowClick(item)"
      >
        mdi-account-details
      </v-icon>
          <v-icon small @click="editItem(item)" v-if="item.is_apply == true">
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
    search: "",
    dialog: false,
    headers: [
      { text: "出借人", value: "id" },
      { text: "租借人", value: "rent_user_name" },
      { text: "设备名称", value: "name" },
      { text: "状态", value: "rent_status" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    desserts: [],
    d: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {},
    name: "",
    phone_number: "",
    description: "",
    location: "",
    reason:'',
    rent_user_name:'',
    equip_name:'',
    rent_start:'',
    rent_exp:''
    
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

    editItem(item) {
      let form = {};
      form["equipid"] = item.id;
      form["token"] = localStorage.getItem("token");
      console.log(form);
      axios
        .post("api/equip/rentdescription/", form)
        .then((r) => {
          console.log(r);
          this.reason = r.data.reason;
          this.rent_user_name = r.data.rent_user_name;
          this.equip_name = r.data.name;
          this.rent_start = r.data.rent_start;
          this.rent_exp = r.data.rent_exp
        })
        .catch((e) => {
          alert("wrong user");
        });
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
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
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
      location.reload();
    },

    save(item) {
         let form = {};
      form["equipid"] = item.id;
      form["token"] = localStorage.getItem("token");
         axios
        .post("api/equip/accept_rent_apply/" ,form)
        .then((r) => {
          console.log(r);
          location.reload();
        })
        .catch((e) => {
          alert("wrong user");
        });
    //   if (this.editedIndex > -1) {
    //     Object.assign(this.desserts[this.editedIndex], this.editedItem);
    //   } else {
    //     this.desserts.push(this.editedItem);
    //   }
    //   this.close();
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
        .get("api/equip/on/" + item.id)
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
      console.log( "post_view/" + items.id);
      this.$router.push("/post_view/" + items.id);

      // this.$router.push("/post_view/" + items.id);
      //this.$router.push({ params:{id:items.id}});
    },
  },
  mounted: function () {
    axios
      .post("api/equip/rentlist/", localStorage.getItem("token"))
      .then((r) => {
        console.log(r.data.list);
        this.d = r.data.list;
        console.log("aaaa", this.d.length);
        //console.log(this.d[0].is_staff)
        for (let i = 0; i < this.d.length; i++) {
          if (this.d[i].is_apply == true) {
            this.d[i]["rent_status"] = "待审核";
            console.log("2 success");
          } else if (this.d[i].is_apply == false) {
            this.d[i]["rent_status"] = "租借中";
            console.log("2 success");
          } else {
            console.log("fail");
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
