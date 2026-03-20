<style>
.center {
  width: 100%;
  height: 100vh;
  background-image: url("/src/background/电脑背景2.jpg");
  background-size: 100% 100%;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

h1 {
  font-size: 30px;
  color: black;
}

.logon {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  /* position: relative;
  overflow: hidden; */
  width: 768px;
  max-width: 100%;
  min-height: 480px;
  margin-top: 20px;
  display: flex;
  background: -webkit-linear-gradient(right, #4284db, #29eac4);
}

.overlaylong {
  border-radius: 10px 0 0 10px;
  width: 50%;
  height: 100%;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlaylongleft {
  border-radius: 0px 10px 10px 0px;
  width: 50%;
  height: 100%;
  background-color: #fff;
  transform: translateX(100%);
  transition: transform 0.6s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlaylongright {
  border-radius: 10px 0 0 10px;
  width: 50%;
  height: 100%;
  background-color: #fff;
  transform: translateX(0%);
  transition: transform 0.6s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlaytitle {
  border-radius: 0px 10px 10px 0px;
  width: 50%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
}


.overlaytitleH2 {
  font-size: 30px;
  color: #fff;
  margin-top: 20px;
  text-align: center;
}

.overlaytitleP {
  display: flex;
  font-size: 15px;
  color: #fff;
  margin-top: 20px;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  text-align: center;
}

.overlaytitleP::before {
  content: "欢迎加入JUST搜搜!";
}


.overlaytitleleft {
  border-radius: 0px 10px 10px 0px;
  width: 50%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: center;
  transform: translateX(0%);
  transition: transform 0.6s ease-in-out;
}

.overlaytitleright {
  border-radius: 0px 10px 10px 0px;
  width: 50%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: center;
  transform: translateX(-100%);
  transition: transform 0.6s ease-in-out;
}

.overlaytitle-Signin {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.overlaytitle-Signup {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.buttongohs {
  width: 180px;
  height: 40px;
  border-radius: 50px;
  border: 1px solid #fff;
  color: #fff;
  font-size: 15px;
  text-align: center;
  line-height: 40px;
  margin-top: 40px;
}

.overlaylongH2 {
  font-size: 25px;
  color: black;
  /* width: 250px; */
}

.overlaylong-Signin {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.overlaylong-Signup {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

}

.sendCode{
  display: flex;
  flex-direction: row;
  align-items: center;
}

.sendCode input{
  background-color: #eee;
  border: none;
  width: 10rem;
}

.sendCode button{
  margin-left: 1rem;
  width: 4rem;
  height: 40px;
}

input {
  background-color: #eee;
  border: none;
  padding: 12px 14px;
  margin: 10px 0;
  width: 15rem;
}

h3{
  font-size: 10px;
  margin-top: 10px;
  cursor: pointer;
}

.inupbutton{
  background-color: #29eac4;
  border: none;
  width: 180px;
  height: 40px;
  border-radius: 50px;
  font-size: 15px;
  color: #fff;
  text-align: center;
  line-height: 40px;
  margin-top: 30px;
}

@media screen and (max-width: 600px) {

  .center {
    background-image: url("/src/background/手机背景.jpg");
  }


  input {
    background-color: #eee;
    border: none;
    padding: 12px 14px;
    width: 100%;
    margin: 10px;
    max-width: 10rem;
    box-sizing: border-box;
  }

  .inupbutton {
    background-color: #29eac4;
    border: none;
    width: 90%;
    height: 40px;
    border-radius: 50px;
    font-size: 15px;
    color: #fff;
    text-align: center;
    line-height: 40px;
    margin-top: 20px;
  }

  .sendCode {
    display: flex;
    flex-direction: row;
    align-items: center;
    max-width: 10rem;
    width: 100%;
  }

  .sendCode input {
    background-color: #eee;
    border: none;
    width: 70%;
    margin-left: 0px;
  }

  .sendCode button {
    margin-left: 0px;
    width: 4rem;
    height: 40px;
  }

  .logon {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
    width: 768px;
    max-width: 98%;
    min-height: 25rem;
    margin-top: 20px;
    display: flex;
    background: -webkit-linear-gradient(right, #4284db, #29eac4);
  }

}

</style>

<template>
  <div class="center">
    <div class="logon">
      <div :class="overlaylong">
        <div class="overlaylong-Signin" v-if="disfiex == 0">
          <h2 class="overlaylongH2">登 录</h2>
          <input type="email" placeholder="邮箱账号" v-model="email_input">
          <input type="password" placeholder="密码" v-model="password_input">
          <h3>忘记密码?</h3>
          <button class="inupbutton"  @click="login">登录</button>
        </div>
        <div class="overlaylong-Signup" v-if="disfiex == 1">
          <h2 class="overlaylongH2">账号注册</h2>
          <input type="text" placeholder="昵称" v-model="username_input">
          <input type="email" placeholder="邮箱" v-model="email_input">
          <input type="password" placeholder="密码" v-model="password_input">
          <div class="sendCode">
          <input type="text" placeholder="验证码" v-model="code_input">
          <button @click="sendCode">发送</button>
          </div>
          <button class="inupbutton" @click="register">注册</button>
        </div>

      </div>
      <div :class="overlaytitle">
        <div class="overlaytitle-Signin" v-if="disfiex == 0">
          <h2 class="overlaytitleH2">你好！</h2>
          <p class="overlaytitleP"></p>

          <div class="buttongohs" @click="Signin">注册</div>
        </div>
        <div class="overlaytitle-Signup" v-if="disfiex == 1">
          <h2 class="overlaytitleH2">欢迎回来！</h2>
          <p class="overlaytitleP"></p>
          <div class="buttongohs" @click="Signup">登录</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>

import axios from "axios";


export default {
  data() {
    return {
      overlaylong: 'overlaylong',
      overlaytitle: 'overlaytitle',
      disfiex: 0,
      username_input:'',
      password_input:'',
      email_input:'',
      code_input:'',
    }
  },
  methods: {
    Signin() {
      this.overlaylong = "overlaylongleft"
      this.overlaytitle = "overlaytitleright"
      setTimeout(() => {
        this.disfiex = 1
      }, 200)
    },
    Signup() {
      this.overlaylong = "overlaylongright"
      this.overlaytitle = "overlaytitleleft"

      setTimeout(() => {
        this.disfiex = 0
      }, 200)
    },

    login() {

      axios.post('http://localhost:8000/login/',{
        email: this.email_input,
        password: this.password_input,
      })
      .then(response => {
        console.log('Response:', response.data);
        if(response.data.status){
          // 登录成功，跳转到首页
          this.$router.push('/');
          this.login_success();
        }else{
          return Promise.reject('登录异常!'),
          this.login_password_error();
        }
      })
      .catch(error => {
        console.error('获取登录数据时出错:', error);
        this.login_error(); // 登录出现问题时自动触发错误提示弹窗
      });
    },

    register() {

      axios.post('http://localhost:8000/register/',{
        username: this.username_input,
        email: this.email_input,
        password: this.password_input,
        code: this.code_input,
      })
      .then(response => {
        console.log('Response:', response.data);
        if(response.data.status){
          this.register_success()
        }
        else if(response.error === '邮箱已被注册'){
          this.register_email_error()
        }
        else{
          this.register_code_error()
        }
      })
      .catch(error => {
        console.error('注册时出错:', error);
        this.register_error(); // 登录出现问题时自动触发错误提示弹窗
      });
    },

    sendCode() {
      axios.post('http://localhost:8000/sendcode/',{
        email:this.email_input,
      })
      .then(response => {
        console.log('Response:', response.data);
        if(response.data.status){
          this.send_success();
        }
        else if(response.data.msg === '该用户已存在，请登录'){
          this.send_login_error();
        }
        else{
          console.error('发送验证码时出错:', error);
          this.send_error();
        }
      })
      .catch(error => {
        console.error('发送验证码时出错:', error);
        this.send_error();
      });
    },
    login_error() {
      this.$notify.error({
        title: '登录异常',
        message: '请检查网络连接！',
        showClose: false,
        duration: 1500,
      });
    },
    login_password_error() {
      this.$notify.error({
        title: '登录异常',
        message: '账号或者密码错误，请重新输入！',
        showClose: false,
        duration: 1500,
      });
    },
    login_success() {
      this.$notify.success({
        title: '登录成功',
        message: '欢迎回来！',
        showClose: false,
        duration: 1500,
      });
    },
    send_error() {
      this.$notify.error({
        title: '发送异常',
        message: '请检测网络连接！',
        showClose: false,
        duration: 1500,
      });
    },
    send_login_error() {
      this.$notify.error({
        title: '发送异常',
        message: '该用户已存在，请登录！',
        showClose: false,
        duration: 1500,
      });
    },
    send_success() {
      this.$notify.success({
        title: '发送成功',
        message: '请注意查收！',
        showClose: false,
      });
    },
    register_success() {
      this.$notify.success({
        title: '注册成功',
        message: '恭喜您，注册成功！现在可以登录啦！',
        showClose: false,
        duration: 1500,
      });
    },
    register_error() {
      this.$notify.error({
        title: '注册异常',
        message: '请检测网络连接！',
        showClose: false,
        duration: 1500,
      });
    },
    register_code_error() {
      this.$notify.error({
        title: '注册异常',
        message: '验证码错误！',
        showClose: false,
        duration: 1500,
      });
    },
    register_email_error() {
      this.$notify.error({
        title: '注册异常',
        message: '邮箱已注册！',
        showClose: false,
        duration: 1500,
      });
    },

  }

}
</script>