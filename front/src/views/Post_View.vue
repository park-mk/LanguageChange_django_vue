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
      <v-card class="mx-auto" max-width="500">
        <v-card-text>
          <div>设备信息</div>
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
    <br>
      <div v-show="user_display || provider_display">
        <label for="pw"
          ><h5><b>使用日子</b></h5></label
        >
        <v-col style="text-align: center">
          <VueHotelDatepicker
            :disabledDates="date"
            :maxNight="14"
            @update="data"
          />

          <label for="pw"
            ><h5><b>使用目的</b></h5></label
          >
          <v-textarea
            v-model="form.reason"
            label="reason"
            outlined
            shaped
            background-color="grey"
          >
          </v-textarea>
          <label for="pw"
            ><h5><b>联系方式</b></h5></label
          >

          <v-text-field
            v-model="form.phone_number"
            label="phone_number"
            outlined
            shaped
            background-color="grey"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-btn v-on:click="send">request</v-btn>
        </v-col>
        <v-col>
          <router-link :to="{ name: 'rent_equip' }">
            <v-btn v-on:click="rent_manage">目录</v-btn>
          </router-link>
        </v-col>
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
      provider_id:'',
      rating: 3,
      is_staff: 0,
      rent_status: 0,
      is_rent: false,
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
    };
  },
  created() {
    this.my_display = false;
    path = window.location.href;
    path = path.split("#");
    console.log(path);
    path[1] = path[1].slice(11);
    console.log("what is postid", path[1]);
    //this.fetch();
  },
  methods: {
    data(value) {
      this.form.start = value.start;
      this.form.end = value.end;
      console.log(value);
    },
    send() {
      // sub['reason'] = this.form.description
      //sub['phone_number'] = this.form.phone_number
      let wrap = {};
      let sub = {}
      let info ={}
     if (this.is_rent == false && this.rent_status == 0) {
        console.log('fuck')
        wrap["userid"] = localStorage.getItem("userid");
        wrap["is_rent"] = this.is_rent;
        wrap["rent_status"] = this.rent_status;
        this.form.user_id = localStorage.getItem("userid");
        this.form.equipid = path[1];
        this.form.user_name = localStorage.getItem("username");
        console.log(this.form);
        axios
          .put(`api/equip/waitlist/`, this.form)
          .then((r) => {
            console.log(r);
            console.log('fuckyou')
                    wrap["rent_status"] = this.rent_status;
                    
                    
                  this.rent_status = 1
            info = {}
              info["userid"] = localStorage.getItem("userid");
        info["is_rent"] = this.is_rent;
        info["rent_status"] = this.rent_status;
        info["rent_start"] = this.form.start
        info["rent_end"] = this.form.end
        console.log('넣기전',info)
             axios.post("api/update_user_status/", info)
             .then((r) => {
               
               
              console.log(r) 
              
              
              
              
                      
            sub['equipid']  = path[1]
            sub['equip_name']   =  this.name
            sub['provider_id'] = this.provider_id
            sub['userid'] = localStorage.getItem("userid");
                  console.log('pleassssssseeeee',sub)
            axios.post('api/user_rent_apply/',sub)
            .then((r)=>{
              console.log(r)
              alert('已提交')
             })

                    
                    
            
            })
            
            
            
            
            
            
            
          
          })
          .catch((e) => console.log(e));
     } 
     else {
       alert("您有还没处理的设备");

     }
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
          console.log('aaaaaaaaaaaaaaaaaaaaaaaa',r);
          this.provider_id = r.data.provider_id
          this.name = r.data.name;
          this.phone_number = r.data.phone_number;
          this.location = r.data.location;
          this.description = r.data.description;
          if (r.data.is_rent == false) {
            this.equip_status = "可借";
            console.log("2 success");
          } else {
            this.equip_status = "租借中";
            console.log("2 success");
          }

          this.set.equipid = path[1];

          this.set.aaa = "0";
          console.log(this.set);
          axios.post("api/equip/waitlist/", this.set).then((r) => {
            console.log(r);
            axios.patch("api/equip/waitlist/", this.set).then((r) => {
              console.log(r);
              console.log(r.data.sucess);
              this.date = r.data.sucess;
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
  height: 1500px !important;
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
#par {
  height: 1000px !important;
}
</style>
