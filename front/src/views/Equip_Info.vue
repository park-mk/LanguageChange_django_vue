<template>
  <v-parallax dark src="../../public/images/main_5.jpg" class="par">
    <v-container>
      <router-link :to="{ name: 'home' }">
        <img
          id="dog"
          src="../../public/images/logo.svg"
          height="150"
          width="150"
        />
      </router-link>
      <h2>设备信息</h2>

      <v-card class="mx-auto" max-width="500">
        <v-card-text>
          <p class="display-1 text--primary">
            {{ name }}
          </p>
          <p>设备状态：{{ equip_status }}</p>
          <div class="text--primary">
            设备说明：{{ description }}<br />
            出借地址：{{ location }}<br />
            联系方式：{{ phone_number }}
          </div>
        </v-card-text>
      </v-card>
      <div v-show="display_list">
        <h2>借租历史</h2>
        <v-card class="mx-auto" max-width="500" style="overflow: visible">
          <v-card-text>
            <div class="text--primary" v-for="(item, i) in list">
              <h4>租借人：{{ item.user_name }}</h4>
              租借开始：{{ item.rent_start }}<br />
              租借结束：{{ item.rent_exp }}<br />
              联系方式：{{ item.phone_number }}<br />
              用途：{{ item.reason }}
              <v-divider></v-divider>
            </div>
          </v-card-text>
        </v-card>
      </div>
      <div v-show="display_waiting_list">
        <h2>等候者名单</h2>
        <v-card class="mx-auto" max-width="500" style="overflow: visible">
          <v-card-text>
            <div class="text--primary" v-for="(item, i) in waiting_list">
              <h4>租借申请人：{{ item.user_name }}</h4>
              租借开始：{{ item.rent_start }}<br />
              租借结束：{{ item.rent_exp }}<br />
              联系方式：{{ item.phone_number }}<br />
              用途：{{ item.reason }}
              <v-row style = "float:right">
                  <v-btn @click="wait_accept(item)" v-if = "item.apply_succes == false" >Accept</v-btn>
                  <v-btn @click="wait_deny(item)" v-if = "item.apply_succes == false"> Deny</v-btn>
              </v-row>
              <v-divider></v-divider>
            </div>
          </v-card-text>
        </v-card>
      </div>
      <h2>评分 <v-rating v-model="rating" readonly
      ></v-rating></h2>
      <h2>留言</h2>

      <div v-show="provider_display">
        <router-link :to="{ name: 'my_equip' }">
          <v-btn v-on:click="rent_manage">目录</v-btn>
        </router-link>
        <router-link :to="{ name: 'rent_equip' }" v-show="manager_display">
          <v-btn v-on:click="rent_manage">目录</v-btn>
        </router-link>
      </div>
    </v-container>
  </v-parallax>
</template>
<script>
import axios from "axios";
import Post_View from "./Post_View.vue";

import VueHotelDatepicker from "@northwalker/vue-hotel-datepicker";

let path;
export default {
  name: "Post_View",
  components: {
    Post_View,
    VueHotelDatepicker,
  },

  data() {
    return {
      date: ["2020/09/25", "2020/09/26"],
      rating: 3,
      is_staff: 0,
      name: "",
      equip_status: "",
      phone_number: "",
      location: "",
      description: "",
      form: {
        reason: "",
        phone_number: "",
        start: "",
        end: "",
        equipid: 0,
        user_id: "",
        user_name: "",
      },
      set: {
        equipid: "",
        aaa: "",
      },
      history_name: "",
      rent_start: "",
      rent_exp: "",
      reason: "",
      list: [],
      display_list: false,
      display_waiting_list: false,
      waiting_list: [],
      rent_status: 0,
      is_rent: false,
      provider_id:''
    };
  },
  created() {
    this.my_display = false;
    path = window.location.href;
    path = path.split("#");
    console.log(path);
    path[1] = path[1].slice(12);
    console.log("what is postid", path[1]);
    //this.fetch();
  },
  methods: {
      wait_accept(item){
          let wrap ={}
          let info= {}
          wrap['equipid'] = path[1]
          wrap['id'] = item.id
          
         // info["userid"] = localStorage.getItem("userid");
         
        //info["is_rent"] = this.is_rent;
        //info["rent_status"] = this.rent_status;
          console.log('아이템이에요',item)
          axios.post('api/equip/wait_allow/',wrap)
          .then((r)=>{
              console.log(r)
             // this.is_rent = true
              info["is_rent"] = true
              info['rent_status'] = 1
              info['userid'] = item.user_id
                        console.log('지금 상태',info)

               axios.post("api/update_user_status/", info).then((r) => {
              console.log(r);
              console.log('motherfucker')
              location.reload()
            });
            
            

          }).catch((e)=>console.log(e))
      },
      wait_deny(item){
          
                    let info= {}

         info["is_rent"] = false
              info['rent_status'] = 0
              info['userid'] = item.user_id
          let wrap ={}
          wrap['equipid'] = path[1]
          wrap['id'] = item.id
          axios.put('api/equip/wait_allow/',wrap)
          .then((r)=>{
              console.log(r)
              
             
                        console.log('지금 상태',info)

               axios.post("api/update_user_status/", info).then((r) => {
              console.log(r);
              console.log('motherfucker')
              location.reload()
              
               })
              
          }).catch((e)=>console.log(e))
      },
      
      
      
    data(value) {
      this.form.start = value.start;
      this.form.end = value.end;
      console.log(value);
    },
    send() {
      // sub['reason'] = this.form.description
      //sub['phone_number'] = this.form.phone_number
      this.form.user_id = localStorage.getItem("userid");
      this.form.equipid = path[1];
      this.form.user_name = localStorage.getItem("username");
      console.log(this.form);
      axios
        .put(`api/equip/waitlist/`, this.form)
        .then((r) => {
          console.log(r);
          location.reload();
        })
        .catch((e) => console.log(e));
    },
  },
  mounted: function () {
    axios
      .post("api/send_user_status/", localStorage.getItem("userid"))
      .then((r) => {
        console.log(r.data);
        this.is_staff = r.data.is_staff;
        this.is_rent = r.data.is_rent;
        this.rent_status = r.data.rent_status;
        if (this.is_staff == 1) {
          this.manager_display = true;
        } else if (this.is_staff == 2) {
          this.provider_display = true;
        } else {
          this.user_display = true;
          console.log(this.user_display);
        }

        axios.get(`api/equip/equip` + "/" + path[1]).then((r) => {
          let mingi = {}
          console.log('aaaaaaaaaaaaaaaa',r);
          mingi['equip_id'] = r.data.id
          mingi['gelai'] = 0
        axios.patch('api/equip/equip_grade/',mingi)
        .then((r)=>{
          
          let total = r.data.total
          this.rating = total
          console.log('mingi',r)
        })
          this.name = r.data.name;
          this.phone_number = r.data.phone_number;
          this.location = r.data.location;
          this.description = r.data.description;
          this.provider_id = r.data.provider_id
          if (r.data.is_rent == false) {
            this.equip_status = "可借";
            console.log("2 success");
          } else {
            this.equip_status = "租借中";
            console.log("2 success");
          }

          this.set.equipid = path[1];
          console.log(path[1]);
          this.set.aaa = "0";
          console.log(this.set);
          axios.post("api/equip/waitlist/", this.set).then((r) => {
            console.log(r);
            axios.patch("api/equip/waitlist/", this.set).then((r) => {
              console.log(r);
              console.log('제발이거여야해',r.data.sucess);
              this.date = r.data.sucess;
              axios.post("api/equip/equip_history/", this.set).then((r) => {
                let com_start;
                let com_exp;
                let com_reason;
                console.log(r);

                this.list = r.data.list;
                if (this.list.length > 0) this.display_list = true;
                console.log(this.list);
                for (let i = 0; i < this.list.length; i++) {
                  com_start = this.list[i].rent_start.split("T");
                  this.list[i].rent_start = com_start[0];
                  com_exp = this.list[i].rent_exp.split("T");
                  this.list[i].rent_exp = com_exp[0];
                  com_reason = this.list[i].reason.split("#");
                  this.list[i]["phone_number"] = com_reason[1];
                  this.list[i].reason = com_reason[0];
                }
                axios.post("api/equip/view_wait/", this.set).then((r) => {
                  console.log(r);

                  this.waiting_list = r.data.list;
                  if (this.waiting_list.length > 0)
                    this.display_waiting_list = true;
                  console.log(this.waiting_list.length)
                  for (let i = 0; i < this.waiting_list.length; i++) {
                      com_start = this.waiting_list[i].rent_start.split("T");
                  this.waiting_list[i].rent_start = com_start[0];
                  com_exp = this.waiting_list[i].rent_exp.split("T");
                  this.waiting_list[i].rent_exp = com_exp[0];
                    com_reason = this.waiting_list[i].reason.split("#");
                    this.waiting_list[i]["phone_number"] = com_reason[1];
                    this.waiting_list[i].reason = com_reason[0];
                  }
                  console.log('aaaaa',this.waiting_list);
                });
              });
            });
          });
        });
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
* {
  text-align: center;
}
.par {
  height: 2000px !important;
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
