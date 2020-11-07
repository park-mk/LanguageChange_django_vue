import Vue from "vue";
import Router from "vue-router";
import Sign from "./views/Sign.vue";
import Info_me from "./views/Info_me";
import Post_list from "./views/Post_list";
import Post_View from "./views/Post_View";
import Post_Write from "./views/Post_Write";
import User_View from './views/User_View';
import Edit_View from './views/Edit_View';
import Sign_Up from './views/Sign_Up'
import Home from './views/Home'
import Manage_User from './views/Manage_User'
import Manage_Equip from './views/Manage_Equip'
import Manage_Rent from './views/Manage_Rent'
import My_Info from './views/My_Info'
import My_Equip from './views/My_Equip'
import Rent_Equip from './views/Rent_Equip'
import Analysis from './views/Analysis'
import Equip_Info from './views/Equip_Info'



import Submit_Request from './views/Submit_Request'



//import History_View from './views/History_View';

Vue.use(Router); //플러그인 등록
export default new Router({
  routes: [
    {
      path: "/",
      component: Sign,
      name: "Main",
    },
    {
      path: "/home",
      component: Home,
      name: "home",
    },
    {
      path: "/my_info/:num",
      component: My_Info,
      name: "my_info",
    },
    {
      path: "/my_equip",
      component: My_Equip,
      name: "my_equip",
    },
    {
      path: "/rent_equip",
      component: Rent_Equip,
      name: "rent_equip",
    },
    {
      path: "/analysis",
      component: Analysis,
      name: "analysis",
    },
    {
      path: "/submit_request",
      component: Submit_Request,
      name: "submit_request",
    },
    {
      path: "/manage_user",
      component: Manage_User,
      name: "manage_user",
    },
    {
      path: "/manage_equip",
      component: Manage_Equip,
      name: "manage_equip",
    },
    {
      path: "/manage_rent",
      component: Manage_Rent,
      name: "manage_rent",
    },
    {
      path: "/sign_up",
      component: Sign_Up,
      name: "sign_up",
    },
    {
      path: "/info",
      component: Info_me,
      name: "info",
    },
    {
      path: "/post_list/:num",
      component: Post_list,
      name: "post_list/",
    },
    {
      path: "/post_view/:id",
      name: "post_view",
      component: Post_View,
      props: true,
    },
    {
      path: "/equip_info/:id",
      name: "equip_info",
      component: Equip_Info,
      props: true,
    },
    {
      path: "/post_write",
      name: "post_write",
      component: Post_Write,
    },
    {
        path:"/user_view/:userid",
        name:"user_view",
        component:User_View,
    },
    {
        path:"/edit_view/:postid",
        name:"edit_view",
        component:Edit_View,
    },
  ],
});
