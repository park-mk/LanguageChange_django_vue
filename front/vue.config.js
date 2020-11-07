module.exports = {
  chainWebpack: config => {
    config.module.rules.delete('eslint');
},
  devServer:{
    proxy:{
       '/api/':{
        target:'http://192.168.43.184:8000',
        ws:true,
        changeOrgin:true
      }
    }
  },
  
  "transpileDependencies": [
    "vuetify"
  ],
  
}