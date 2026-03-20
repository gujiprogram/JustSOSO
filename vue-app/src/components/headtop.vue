<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const UserLogin = () => {
      router.push('/login'); // 跳转到登录页面
    };

    return {
      UserLogin
    };
  }
}
</script>


<template>

    <el-header>
      <div>
        <a href="/">JUST搜搜-网盘资源搜索</a>
      </div>
      <div>
        <ul>
          <li>
            <a @click="UserLogin">
              <el-icon><UserFilled /></el-icon>
            </a>
          </li>
          <li>
            <a href="#" @click="handleClick">
              <el-icon><Menu /></el-icon>
            </a>
          </li>
          <li>
            <a href="#" @click="handleClick">
              <el-icon><Promotion /></el-icon>
            </a>
          </li>
        </ul>
      </div>
    </el-header>


</template>

<style scoped>

.el-header{
  overflow: hidden;
  background-color: #803D3B;
  display: flex;
  justify-content: space-between; /* 水平居左和水平居右 */
  align-items: center; /* 垂直居中子元素 */
  padding: 2rem 0.75rem;
}


/* 导航条链接 */
.el-header a {
  border-radius: 10px; /* 设置导航条的圆角 */
  font-size: 1.25rem;
  font-weight: 600;
  float: left;
  display: block;
  color: #f2f2f2;
  padding: 0.6rem 0.5rem;
  text-decoration: none;
}

/* 链接颜色修改 */
.el-header a:hover {
  background-color: #999;
  color: black;
}

/* 图标的顺序 */
.el-header ul{
  float:right;
  list-style-type: none;
  padding: 0;
}

.el-header li{
  float:right;
  display: inline-block;
  margin: 0 1rem; /* 设置左右边距 */
}

@media screen and (max-width: 600px) {

  /* 导航条链接 */
  .el-header a {
    border-radius: 10px; /* 设置导航条的圆角 */
    font-size: 1.3rem;
    font-weight: 600;
    float: left;
    display: block;
    color: #f2f2f2;
    padding: 0.6rem 0.5rem;
    text-decoration: none;
  }

  .el-header li{
    float:right;
    display: inline-block;
    margin: 0 5px; /* 设置左右边距 */
  }

}
@media screen and (max-width: 400px) {

  /* 导航条链接 */
  .el-header a {
    border-radius: 10px; /* 设置导航条的圆角 */
    font-size: 1.1rem;
    font-weight: 600;
    float: left;
    display: block;
    color: #f2f2f2;
    padding: 0.5rem 0.4rem;
    text-decoration: none;
  }

  .el-header li{
    float:right;
    display: inline-block;
    margin: 0 5px; /* 设置左右边距 */
  }

}


</style>