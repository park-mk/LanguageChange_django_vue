<template>
  <v-form>
    <v-container>
      <v-row> 标题 </v-row>
      <v-row>
        <v-text-field
          :counter="50"
          label="제목"
          name="title"
          required
          v-model="title"
          maxlength="50"
        ></v-text-field>
      </v-row>
      <v-row>
       
          <v-row>内容 </v-row>
      </v-row>
      <v-row>
      <v-col>
          <v-btn block outlined color="blue" @click="codeClick"> 代码段的插入 </v-btn>
        </v-col>
        <v-col>
          <v-text-field
            v-model="message"
            :append-outer-icon="message ? 'mdi-send' : 'mdi-send'"
            :prepend-icon="icon"
            filled
            clear-icon="mdi-close-circle"
            clearable
            label="img-url"
            type="text"
            @click:append="toggleMarker"
            @click:append-outer="sendMessage"
            @click:prepend="changeIcon"
            @click:clear="clearMessage"
          ></v-text-field>
        </v-col>
        
      </v-row>
      <v-row>
        <div class="example">
          <quill-editor
            class="editor"
            ref="myTextEditor"
            :value="content"
            :options="editorOption"
            @change="onEditorChange"
            @blur="onEditorBlur($event)"
            @focus="onEditorFocus($event)"
            @ready="onEditorReady($event)"
          />
        </div>
      </v-row>
      <v-row>
        <v-btn block outlined color="blue" @click="writeClick"> 发帖 <v-icon>mdi-comment-processing-outline</v-icon></v-btn>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import dedent from "dedent";
import hljs from "highlight.js";
import debounce from "lodash/debounce";
import { quillEditor } from "vue-quill-editor";
import axios from "axios";

import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

import Vue from "vue";
let path;
let prevent = 0;
export default {
  name: "Edit_View",
  components: {
    quillEditor,
  },
  
   created() {
    
    path = window.location.href;
    path = path.split("#");
    path[1] = path[1].slice(11);
   console.log(path[1])
 
    this.fetch();
   
  },
  methods: {
    fetch() {
      axios
        .get(`http://simplebbs.iterator-traits.com/api/v1/post/` + path[1], {
          headers: {
            Authorization: this.$store.state.token,
          },
        })
        .then((r) => {
          

          this.title = r.data.title;
          this.content = r.data.content;
          console.log(this.title)
          console.log(this.content)
  
   })
        .catch((e) => {
          console.log(e);
          alert('error')
        });
    },
  
  
  

      
    toggleMarker() {
      this.marker = !this.marker;
    },
    sendMessage() {
      this.content =
        this.content +
        '<img src="' +
        this.message +
        '" style="max-width: 100%;">';
      // this.content += this.tem_content;
      // tem_content = [];
      this.resetIcon();
      this.clearMessage();
    },
    clearMessage() {
      this.message = "";
    },
    resetIcon() {
      this.iconIndex = 0;
    },
    changeIcon() {
      this.iconIndex === this.icons.length - 1
        ? (this.iconIndex = 0)
        : this.iconIndex++;
    },
    codeClick(){
       
          this.content=this.content+"<pre>  <br>insert your code code " +"</pre>"; 

      
        console.log('code:',this.code)
    },
    writeClick() {
      ////emoji
      this.content = this.content.replace("😀", "#笑");

      axios
        .put(`http://simplebbs.iterator-traits.com/api/v1/post/`+path[1], this.$data, {
          headers: {
            Authorization: this.$store.state.token,
          },
        })
        .then((response) => {
          console.log(response);
          this.$router.push("/post_list/1");
        })
        .catch((error) => {
            alert('error')
          console.log(error);
        });
    },
    onEditorChange: debounce(function (value) {
     
             
          //console.log('fail')
      this.content = value.html;
      
     
      this.content = this.content.replace("#笑", "😀");
      console.log(this.content);

    }, 466),
    onEditorBlur(editor) {
      console.log("editor blur!", editor);
    },
    onEditorFocus(editor) {
      console.log("editor focus!", editor);
    },
    onEditorReady(editor) {
      console.log("editor ready!", editor);
    },
  },
  computed: {
    editor() {
      return this.$refs.myTextEditor.quill;
    },
    contentCode() {
      return hljs.highlightAuto(this.content).value;
    },
  },
  mounted() {
    console.log("this is Quill instance:", this.editor);
  },
  
  
  
  data() {
    return {
        code:0,
      tem_content: "",
     
      password: "Password",
      show: false,
      message: "",
      marker: true,
      iconIndex: 0,
      icons: [
        "mdi-emoticon",
        "mdi-emoticon-cool",
        "mdi-emoticon-dead",
        "mdi-emoticon-excited",
        "mdi-emoticon-happy",
        "mdi-emoticon-neutral",
        "mdi-emoticon-sad",
        "mdi-emoticon-tongue",
      ],
      title: "",
      editorOption: {
        modules: {
          toolbar: [
            ["bold", "italic", "underline", "strike"],
            ["blockquote", "code-block"],
            [{ header: 1 }, { header: 2 }],
            [{ list: "ordered" }, { list: "bullet" }],
            [{ script: "sub" }, { script: "super" }],
            [{ indent: "-1" }, { indent: "+1" }],
            [{ direction: "rtl" }],
            [{ size: ["small", false, "large", "huge"] }],
            [{ header: [1, 2, 3, 4, 5, 6, false] }],
            [{ font: [] }],
            [{ color: [] }, { background: [] }],
            [{ align: [] }],
            ["clean"],
            ["link", "image", "video"],
          ],
          syntax: {
            highlight: (text) => hljs.highlightAuto(text).value,
          },
        },
      },
      content: dedent``,
    };
  },
  
};
</script>

<style lang="scss" scoped>
.example {
  display: flex;
  flex-direction: column;

  .editor {
    height: 40rem;
    overflow: hidden;
  }

  .output {
    width: 100%;
    height: 20rem;
    margin: 0;
    border: 1px solid #ccc;
    overflow-y: auto;
    resize: vertical;

    &.code {
      padding: 1rem;
      height: 16rem;
    }

    &.ql-snow {
      border-top: none;
      height: 24rem;
    }
  }
}
</style>
