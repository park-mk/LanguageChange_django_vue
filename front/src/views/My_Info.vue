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
      <h2>用户信息</h2>

      <v-card class="mx-auto" max-width="500">
        <v-card-text>
          <p class="display-1 text--primary">
            {{ username }}
          </p>
          <p>学号：{{ userid }}</p>
          <div class="text--primary">
            邮箱：{{ email }}<br />
            <div v-if="info_status == 0 && rent_status == 1">
              在租借<br />
              设备名称：{{ equip_name }}<br />
              还剩余：{{ days }}天
              <br />
              租借开始：{{ rent_start }}
              <br />
              租借结束：{{ rent_end }}
            </div>
            <div v-if="info_status == 1 && rent_status == 1">
              即将租借<br />
              设备名称：{{ equip_name }}<br />
              距离租借：{{ days }}天
              <br />
              租借开始：{{ rent_start }}
              <br />
              租借结束：{{ rent_end }}
            </div>
            <div v-if="info_status == 2 && rent_status == 1">
              即将租借<br />
              设备名称：{{ equip_name }}<br />
              已经到期了！赶紧返还
              <br />
              租借开始：{{ rent_start }}
              <br />
              租借结束：{{ rent_end }}
            </div>
          </div>
        </v-card-text>
      </v-card>
      <br />
      <v-btn
        v-if="info_status == 0 && rent_status == 1"
        v-on:click="return_equip"
        >返还</v-btn
      >
      <v-btn
        v-if="info_status == 1 && rent_status == 1"
        v-on:click="cancel_equip"
        >取消申请</v-btn
      >
      <v-btn
        v-if="info_status == 2 && rent_status == 1"
        v-on:click="return_equip"
        >返还</v-btn
      >
      <br /><br />
      <div v-show="display_list">
        <h2>借租历史</h2>
        <v-card class="mx-auto" max-width="500" style="overflow: visible">
          <v-card-text>
            <div class="text--primary" v-for="(item, i) in list">
              <h4>租借设备：{{ item.equip_name }}</h4>
              租借开始：{{ item.rent_start }}<br />
              租借结束：{{ item.rent_exp }}<br />

              <v-divider></v-divider>
            </div>
          </v-card-text>
        </v-card>
      </div>
      <div v-if="rent_status == 2">
        <h2>
          评分
          <v-rating
            v-model="rating"
            half-increments
            hover
            @input="addRating($event)"
          ></v-rating>
        </h2>

        <h2>留言</h2>
        <v-textarea
          v-model="comment"
          label="comment"
          outlined
          shaped
          background-color="grey"
        >
        </v-textarea>
        <v-btn v-on:click="post_ex">提交</v-btn>
      </div>
      <div>
        <v-col>
          <v-btn
            v-show="user_display"
            v-if="is_apply_a == false &&supervisor == false"
            @click="apply_provider"
            >申请成为提供者</v-btn
          >

          <div v-show="display_reason">
            <h5><b>申请理由</b></h5>

            <v-textarea
              v-model="description"
              label="申请理由，包括实验室信息"
              outlined
              shaped
              background-color="grey"
            >
            </v-textarea>
            <br />
            <v-btn @click="apply_submit">提交</v-btn>
          </div>
          <v-btn
           v-show="user_display"
            v-if="is_apply_a == true &&supervisor == false"
            >正在申请成为提供者</v-btn
          >
        </v-col>
        <v-col>
          <router-link :to="{ name: 'home' }" v-if ="supervisor ==false">
            <v-btn>home</v-btn>
          </router-link>
          <router-link :to="{ name: 'manage_user' }" v-if= "supervisor==true">
            <v-btn>目录</v-btn>
          </router-link>
        </v-col>
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
    VueHotelDatepicker,
  },

  data() {
    return {
      date: ["2020/09/25", "2020/09/26"],
      comment: "",
      rating: 4,
      is_staff: 0,
      username: "",
      rent_equip_id: "",
      days: "",
      email: "",
      userid: "",
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
      is_rent: true,
      equip_name: "",
      rent_end: "",
      info_status: -999,
      user_display: false,
      rate: 0,
      is_apply_a: false,
      display_reason: false,
      supervisor:false
    };
  },

  created() {
    this.my_display = false;
    path = window.location.href;
    path = path.split("#");
    console.log(path);
    path[1] = path[1].slice(9);
    console.log("what is postid", path[1]);
    //this.fetch();
  },
  methods: {
    history_view() {},
    apply_provider() {
      this.display_reason = true;
    },
    apply_submit() {
      let form = {};
      form["reason_pro"] = this.description;
      form["userid"] =  path[1]
      console.log(form);
      axios.post("api/user_apply_status_up", form).then((r) => {
        console.log(r);
        location.reload()
      });
    },

    return_equip() {
      console.log("whyyyy");
      let info = {};
      info["userid"] =  path[1]
      info["is_rent"] = true;
      info["rent_status"] = 2;
      info["rent_start"] = this.rent_start;
      info["rent_end"] = this.rent_end;
      console.log("넣기전", info);
      axios.post("api/equip/return_equip/", this.rent_equip_id).then((r) => {
        console.log("return");
        axios.post("api/update_user_status/", info).then((r) => {
          alert("请你评价一下这个设备的使用经验吧");
          location.reload();
          console.log(r);
        });
      });
    },

    cancel_equip() {
      console.log("whyyyy");
      let info = {};
      let wrap = {};
      info["userid"] =  path[1]
      info["is_rent"] = false;
      info["rent_status"] = 0;
      info["rent_start"] = this.rent_start;
      info["rent_end"] = this.rent_end;
      console.log("넣기전", info);
      wrap["equipid"] = this.rent_equip_id;
      wrap["user_id"] =  path[1]
      console.log(wrap);
      axios.post("api/equip/cancel_waitlist/", wrap).then((r) => {
        console.log(r);
        axios.post("api/update_user_status/", info).then((r) => {
          console.log(r);
        });
      });
    },
    addRating(value) {
      console.log(value);
      this.rate = value;
    },
    post_ex() {
      let wrap = {};
      wrap["grade"] = this.rate;
      wrap["user_name"] = this.username;
      wrap["user_id"] =  path[1]
      wrap["comment"] = this.comment;
      wrap["equip_id"] = this.rent_equip_id;
      console.log(wrap);

      let info = {};

      info["userid"] =  path[1]
      info["is_rent"] = true;
      info["rent_status"] = 3;

      axios.post("api/equip/equip_grade/", wrap).then((r) => {
        console.log(r);
        axios.post("api/update_user_status/", info).then((r) => {
          console.log(r);
          alert("谢谢你的参与");
          location.reload();
        });
      });
    },
  },
  mounted: function () {
    if(localStorage.getItem('super')==1)
    {
      this.supervisor = true
    }
    axios
      .post("api/send_user_status/",  path[1])
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
          console.log("user_display", this.user_display);
        }
        axios.post("api/render",  path[1]).then((r) => {
          console.log(r.data);
          console.log("실행되긴 하는겨");
          this.username = r.data.info.username;
          this.userid = r.data.info.userid;
          this.email = r.data.info.email;
          this.rent_equip_id = r.data.info.apply_equip_id;
          this.days = r.data.days;
          this.is_rent = r.data.info.is_rent;
          this.equip_name = r.data.info.apply_equip_name;
          this.rent_start = r.data.info.rent_start;
          this.rent_end = r.data.info.rent_end;
          console.log("is_rent", this.is_rent);
          console.log("ㅁㅁㅁㅁ", this.days);
          this.is_apply_a = r.data.info.is_apply_a;
          if (this.days > 0 && Number.isInteger(this.days)) {
            this.info_status = 0;
          } else if (this.days < 0 && Number.isInteger(this.days)) {
            this.info_status = 1;
            this.days = Math.abs(this.days);
          } else if (this.days == "availabe") {
            this.info_status = 4;
            console.log("aaaaaaaaaaaaaaaaaaaaa");
          } else {
            this.info_status = 2;
            this.days = parseInt(this.days);
          }
          let wrapper = {};

          wrapper["user_id"] =  path[1]
          wrapper["gelai"] = 0;

          axios.post("api/user_history/", wrapper).then((r) => {
            console.log(r);
          
              this.list = r.data.list
            if (this.list.length > 0) 
            this.display_list = true;
            for (let i = 0; i < this.list.length; i++) {
              //com_start = .split("T");
              this.list[i].rent_start =this.list[i].borrow_from
              //com_exp = this.list[i].rent_exp.split("T");
              this.list[i].rent_exp = this.list[i].borrow_till
              this.list[i].equip_name = this.list[i].equip_name
              //com_reason = this.list[i].reason.split("#");
              //this.list[i]["phone_number"] = com_reason[1];
              //this.list[i].reason = com_reason[0];
            }
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
