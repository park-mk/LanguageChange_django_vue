<template>
  <v-form>
    <v-container>
      <v-row> <h1>标题 </h1></v-row>
      <v-row>
        <v-text-field
          :counter="50"
          label="标题"
          name="title"
          required
          v-model="title"
          maxlength="50"
        ></v-text-field>
      </v-row>
      <v-row>
        <v-row><h1>内容</h1> </v-row>
      </v-row>
      <v-row>
        <v-col>
          <v-btn block outlined color="blue" @click="codeClick">
          
            代码段的插入
          </v-btn>
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
        <v-btn block outlined color="blue" @click="writeClick"> 发帖<v-icon>mdi-comment-processing-outline</v-icon> </v-btn>
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

export default {
  name: "post_writer",
  components: {
    quillEditor,
  },
  data() {
    return {
      code: 0,
      tem_content: "",
      img:
        "< img src='https://iknow-pic.cdn.bcebos.com/9213b07eca806538288cd37e95dda144ad34827c" +
        "style='max-width: 100%;'>",
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
  methods: {
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
    codeClick() {
      this.content =
        this.content + "<pre>  <br>insert your code code " + "</pre>";

      console.log("code:", this.code);
    },
    writeClick() {
      ////emoji
      this.content = this.content.replace("😀", "#笑");
      this.content = this.content.replace("😷", "#生病");
      this.content = this.content.replace("😂", "#哭笑");
      this.content = this.content.replace("😝", "#调皮");
      this.content = this.content.replace("😳", "#惊讶");
      this.content = this.content.replace("😱", "#恐怖");
      this.content = this.content.replace("😔", "#忧郁");
      this.content = this.content.replace("😒", "#不耐烦");
      this.content = this.content.replace("🙄", "#哇");
      this.content = this.content.replace("😩", "#好累");
      this.content = this.content.replace("🤔", "#想一想");
      this.content = this.content.replace("👻", "#鬼");
      this.content = this.content.replace("🙈", "#猴子");
      this.content = this.content.replace("🙏", "#谢谢");
      this.content = this.content.replace("💪", "#强壮");
      this.content = this.content.replace("👊", "#拳头");
      this.content = this.content.replace("💯", "#一百分");
      this.content = this.content.replace("🍻", "#啤酒");
      this.content = this.content.replace("🎁", "#礼物");
  this.content=this.content.replace(' <img src=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT-r-V49N0wM_Fmz8djUiCJPaBur4883lv5Dg&usqp=CAU  style="max-width: 100%;">','#我的自定义表情#',)
      axios
        .post(`http://simplebbs.iterator-traits.com/api/v1/post`, this.$data, {
          headers: {
            Authorization: this.$store.state.token,
          },
        })
        .then((response) => {
          console.log(response);
          this.$router.push("/post_list/1");
        })
        .catch((error) => {
          alert("error");
          console.log(error);
        });
    },
    onEditorChange: debounce(function (value) {
      //console.log('fail')
      this.content = value.html;

      this.content = this.content.replace("#笑", "😀");
      this.content = this.content.replace("#生病","😷");
      this.content = this.content.replace( "#哭笑","😂");
      this.content = this.content.replace( "#调皮","😝");
      this.content = this.content.replace( "#惊讶","😳");
      this.content = this.content.replace( "#恐怖","😱");
      this.content = this.content.replace( "#忧郁","😔");
      this.content = this.content.replace( "#不耐烦","😒");
      this.content = this.content.replace( "#哇","🙄");
      this.content = this.content.replace( "#好累","😩");
      this.content = this.content.replace( "#想一想","🤔");
      this.content = this.content.replace( "#鬼","👻");
      this.content = this.content.replace( "#猴子","🙈");
      this.content = this.content.replace( "#谢谢","🙏");
      this.content = this.content.replace( "#强壮","💪");
      this.content = this.content.replace( "#拳头","👊");
      this.content = this.content.replace( "#一百分","💯");
      this.content = this.content.replace( "#啤酒","🍻");
      this.content = this.content.replace( "#礼物","🎁");
  this.content=this.content.replace('#我的自定义表情#',' <img src=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT-r-V49N0wM_Fmz8djUiCJPaBur4883lv5Dg&usqp=CAU style="max-width: 100%;">')

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
