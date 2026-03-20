<script setup>
import Headtop from '@/components/headtop.vue'
import Footerbuttom from '@/components/footerbuttom.vue'
import {Search} from "@element-plus/icons-vue";
import QrcodeVue from 'vue-qrcode';
// 导入自定义图标
import IconBaiduCloud from '@/icon/百度网盘.ico';
import IconOtherCloud from '@/icon/其他网盘.ico';
import IconAliCloud from '@/icon/阿里云盘.ico';
import IconQuarkCloud from '@/icon/夸克网盘.png';

const input = ref('');
import axios from 'axios';

const value = ref(true) // 是否隐藏换页图标
const showEmpty = ref(false) // 是否展示空页面
const searchword = ref() // 用于判断用户是否输入了新关键词
const movies = ref([]); // 使用ref定义响应式状态movies，并初始化为空数组
const isMobile = ref(false); // 监听屏幕大小
const poster = ref();
const searching = ref(false); //进度条显示

// 使用 ref 创建响应式数据
const currentPage = ref(1);
const totalMovies = ref(0);
const isBackground = ref(true);


const mainStyle = ref({
  backgroundColor: '#322C2B',
  padding: '25.3vh 0',
  height: '100%',
});

const selectedLink = ref('全部');

const selectLink = (link) => {
  selectedLink.value = link;
  if (input.value !== '' && searchword.value === input.value) {
    // 输入框不为空时执行 handleCurrentChange(1) 函数
    handleCurrentChange(1)
  }
};

// 改变屏幕布局
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 600;
};

// 挂载时执行
onMounted(() => {
  window.addEventListener('resize', checkMobile);
  checkMobile(); // 初始化时执行一次
});

// 卸载时执行
onUnmounted(() => {
  window.removeEventListener('resize', checkMobile);
});

const networkIcon=(movie)=>{
  // 根据电影网盘类型返回对应的图标类名
  switch (movie) {
    case '百度':
      return IconBaiduCloud;
    case '夸克':
      return IconQuarkCloud;
    case '阿里':
      return IconAliCloud;
    default:
      return IconOtherCloud;
  }
}

// 处理页码变化事件
const handleCurrentChange = (page) => {
  // 更新当前页码
  currentPage.value = page;
  fetchMovies(input.value,(currentPage.value - 1) * 10, selectedLink.value);
};

// 从后端获取电影列表数据的方法，需要根据实际情况实现
const fetchMovies = (search_name,offset,selectedLink) => {
  axios.get('http://127.0.0.1:8000/getmovie/?search_keyword='+search_name+'&network='+selectedLink+'&offset='+offset)
      .then(response => {
        if(response.data.success){
          searching.value = false;
          poster.value = "http://127.0.0.1:8000"+response.data.poster;
          totalMovies.value = response.data.total;
          if (totalMovies.value>10){value.value = false}
          // 解构响应中的数据，并赋值给movies
          movies.value = response.data.movie_info_list
          console.log(poster.value)
          console.log(movies.value)
          if (totalMovies.value<1){value.value = true;showEmpty.value = true;}
        }
        else{
          // 如果从后端获取的success为false，则调用爬虫函数
          crawlMovies(search_name).then(success=> {
            if (success) {
              // 如果爬虫函数成功，重新开始fetchMovies
              fetchMovies(search_name, offset,selectedLink);
            } else {
              console.log(success)
              searching.value = false;
              showEmpty.value = true;
              console.error('爬虫函数执行失败或未找到电影资源');
            }
          });
        }

      })
      .catch(error => {
        searching.value = false;
        showEmpty.value = true;
        console.error('获取电影数据时出错:', error);
      });
};

const crawlMovies = (search_name) => {
  return new Promise((resolve, reject) => {
    const data = {
      search_keyword: search_name
    };
    console.log(search_name)
    axios.post('http://127.0.0.1:5000/movie', data)
        .then(response => {
          console.log(response.data);
          if (response.data.success === false) {
            showEmpty.value = true;
          }
          resolve(response.data.success);
        })
        .catch(error => {
          console.error('获取电影数据时出错:', error);
          showEmpty.value = true;
          reject(error);
        });

  });
};


const search = () => {

  // 设置搜索状态为 true
  searching.value = true;

  searchword.value = input.value;
  handleCurrentChange(1);
  mainStyle.value = {
    backgroundColor: '#322C2B',
    height: '100%',
};

}

</script>


<template>

  <div class="homeBox" >
    <headtop></headtop>

    <el-container >

      <el-main :style="mainStyle">

        <div class="title">
          <label >JUST 搜搜</label>
        </div>

        <div>
          <ul>
            <li>
              <el-button
                  :class="{ active: selectedLink === '全部' }"
                  @click="selectLink('全部')"
              >
                全部
              </el-button>
            </li>
            <li>
              <el-button
                  :class="{ active: selectedLink === '阿里' }"
                  @click="selectLink('阿里')"
              >
                阿里网盘
              </el-button>
            </li>
            <li>
              <el-button
                  :class="{ active: selectedLink === '百度' }"
                  @click="selectLink('百度')"
              >
                百度网盘
              </el-button>
            </li>
            <li>
              <el-button
                  :class="{ active: selectedLink === '夸克' }"
                  @click="selectLink('夸克')"
              >
                夸克网盘
              </el-button>
            </li>
          </ul>
        </div>

        <div class="input-div">
          <el-input v-model="input" class="input-class" size="large" placeholder="请输入搜索关键字" @keyup.enter="search">
            <template #prepend>
              <el-icon><Search/></el-icon>
            </template>
            <template #append>
              <el-button type="primary" @click="search">搜索</el-button>
            </template>
          </el-input>
        </div>

        <div class="progress">
        <el-progress v-if="searching" :percentage="100" :show-text="false" color="#803D3B" :indeterminate="true" :duration="3"/>
        </div>

        <div v-if="movies.length > 0" v-for="movie in movies" :key="movie.id" class="box-cards">
          <el-card shadow="hover">
            <div class="movie-content">
              <span class="mobile-top">
              <el-image :src="poster" class="movie-picture"></el-image>
              <template v-if="isMobile">
                <span class="moblie-text">
                <h2>{{ movie.name }}</h2>
                  <!-- 别名字段，只有在 movie.alias 不为空时才展示 -->
                <p v-if="movie.alias">别名：{{ movie.alias }}</p>
                </span>
              </template>
              </span>
              <div class="movie-info">
                <template v-if="!isMobile">
                <span class="moblie-text">
                <h2>{{ movie.name }}</h2>
                <!-- 别名字段，只有在 movie.alias 不为空时才展示 -->
                <p v-if="movie.alias">别名：{{ movie.alias }}</p>
                </span>
                </template>
                <!-- 时长字段 -->
                <p v-if="movie.detail">时长：{{ movie.detail }}</p>
                <!-- 描述字段 -->
                <p v-if="movie.description">描述：{{ movie.description }}</p>
                <!-- 豆瓣评分字段 -->
                <p v-if="movie.rate">豆瓣评分：{{ movie.rate }}</p>
                <!-- 网盘类型字段 -->
                <p v-if="movie.network">
                  网盘类型：
                  <span class="icon-wrapper">
                    <img :src="networkIcon(movie.network)" style="width: 1.2rem; height: 1.2rem;">
                  </span>
                    {{ movie.network }}网盘
                  </p>
                  <!-- 资源大小字段 -->
                  <p v-if="movie.size">资源大小：<span style="font-weight: bold; font-size: 15px;">{{ movie.size }}</span></p>
                  <!-- 链接字段 -->
                  <p>
                  <span class="link" v-if="movie.link">
                    链接：
                    <a :href="movie.link" target="_blank" style="border-radius: 99px; margin-right: 1rem">
                      <el-button :class="{ 'link_button': movie.access, 'link_button_disabled': !movie.access }" :disabled="!movie.access">点击跳转</el-button>
                    </a>
                    <span style="color: #436850; font-weight: bold">{{ movie.access ? '链接可访问' : '链接已失效' }}</span>
                  </span>
                </p>
              </div>

            </div>
          </el-card>
        </div>
        <div v-else-if="showEmpty">
          <el-empty description="暂无数据"></el-empty>
        </div>

        <div class="pagination">
          <el-pagination layout="prev, pager, next"
                         :background="isBackground"
                         @current-change="handleCurrentChange"
                         :current-page="currentPage"
                         :hide-on-single-page="value"
                         :total="totalMovies"/>
        </div>

      </el-main>

    </el-container>

    <footerbuttom style="bottom: 0; align-self: flex-end;"></footerbuttom>

  </div>

</template>

<style lang="less">

.homeBox{
  height: 100vh;
  width: 100vw;
}


.el-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


// 图标颜色
.title{
  width: 100%;
  text-align: center;
  font-size: 5rem;
  color: #803D3B;
  font-weight: bolder;
}

.el-main ul{
  width: auto;
  display: flex;
  flex-direction: row;
  justify-content: center;
  list-style-type: none;
  padding: 0 0;
}

.el-main ul{
  width: 40%;
  margin: 1rem auto; /* 使用 margin: 0 auto; 来水平居中 */
  display: flex;
  flex-direction: row;
  justify-content: center;
  list-style-type: none;
  padding: 0 0;
}

.el-main li{
  margin: 0 auto;
  color:whitesmoke;
}

// 进度条设置
.progress{
  justify-items: center;
  align-items: center;
}
.el-progress{
  width: 90%;
  margin: 0 auto;
}

.el-button{
  border-radius: 99px;
  background-color: transparent; /* 设置背景颜色为透明 */
  color: inherit;
  border: none;
}


.el-button:hover{
  border-radius: 99px;
  background: #E4C59E;
  color: inherit;
  border: none;
}


// 网盘选择
.active {
  pointer-events: none;
  background: #E4C59E;
  color: black;
}


.input-div {
  display: flex;
  margin: 2rem auto;
  width: 50%;
  height: 5.5vh;
  border-radius: 95px;
  background-color: #fff;
}

.icon-wrapper {
  display: flex; /* 使用flex布局 */
  align-items: center; /* 垂直居中 */
  margin-right: 0.3rem;
}

.input-class {
  .el-input-group__prepend {
    border-radius: 95px;
    border: 0;
    background-color: #fff;
    box-shadow: 0 0 0 0;
  }

  .el-input__wrapper {
    border-radius: 95px;
    border: 0;
    box-shadow: 0 0 0 0;
  }

  .el-input-group__append {
    border-radius: 95px;
    width: 5rem;
    border: 0;
    box-shadow: 0 0 0 0;
  }

  .el-input-group__append:hover {
    background-color: #B4B4B8; /* 鼠标悬停时的背景颜色 */
    color: white;
  }
}

// 导航框样式
.pagination{
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 修改分页样式 */
.el-pagination.is-background .el-pager li {
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  text-align: center;
  border-radius: 4px;
  background-color: #E4C59E;
  color: black;
}

/* 激活后的样式 */
.el-pagination.is-background .btn-next.is-active, .el-pagination.is-background .btn-prev.is-active, .el-pagination.is-background .el-pager li.is-active {
  background-color: #803D3B;
  color: white;
}


.el-pagination.is-background .el-pager li:hover{
  color: white !important;/*hover时候的文字颜色*/
}


/* 修改左右箭头样式 */
.el-pagination .btn-next ,
.el-pagination .btn-prev {
  border-radius: 4px;
  background-color: #E4C59E !important;
}
/* 修改左右箭头样式 */
.el-pagination .btn-next:disabled ,
.el-pagination .btn-prev:disabled {
  border-radius: 4px;
  background-color: #B2936C !important;
}

/* 修改左右箭头样式 */
.el-pagination .btn-next .el-icon,
.el-pagination .btn-prev .el-icon {
  /* background-color: red; */
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  text-align: center;
  background-color: #E4C59E;
  color: black;
  border: 1px;
}
/* 当箭头不能点击时的样式 */
.el-pagination .btn-next:disabled .el-icon,
.el-pagination .btn-prev:disabled .el-icon {
  color: black; /* 箭头颜色变为灰色 */
  background-color: #B2936C;
}

// 卡片背景颜色
.el-card{
  background-color: #E4C59E;
  height: auto;
}

.box-cards {
  width: 95%;
  margin: 2rem auto;
  height: auto;
}

.el-empty{
  padding: 10vh 0;
}

.movie-content{
  display: flex;
  height: auto;
}


.movie-picture{
  display: flex;
  margin-right: 3rem;
  height: auto;
}

.movie-info{
  width: 80%;
  padding-top: 0;
  height: auto;
}

.movie-info h2{
  margin-top: 0;
}

.movie-info p{
  margin-top: 0;
  display: flex; /* 使用flex布局 */
}

.link{
  display: flex;
  justify-content: center;
  align-items: center;
}

.link_button_disabled {
  color: wheat !important;
  background:  #803D3B !important;
  border-radius: 99px;
  position: relative;
  overflow: hidden;
  pointer-events: none /* 禁用按钮点击事件 */ !important;
  opacity: 0.6; /* 降低按钮透明度 */
  cursor: not-allowed /* 鼠标样式为禁止 */ !important;
  text-decoration: line-through; /* 文本添加删除线 */
}


.link_button {
  color: wheat !important;
  background:  #803D3B !important;
  border-radius: 99px;
  position: relative;
  overflow: hidden;
}

.link_button::before {
  content: "";
  position: absolute;
  width: 50px;
  height: 200%;
  background-color: rgba(255, 255, 255, .6);
  transform: skew(45deg) translate3d(-200px, 0, 0);
  transition: transform 0.5s ease-in-out;
}

.link_button:hover::before {
  transform: skew(45deg) translate3d(300px, 0, 0);
}

.link_button:hover {
  border-radius: 99px !important;
  background: #8B322C !important;
  color: wheat !important;
}


@media screen and (max-width: 600px) {

  html {
    /* 设置缩放初始化为 100% */
    zoom: 100%;
  }

  .movie-content{
    display: flex;
    height: auto;
    flex-direction: column;
  }


  /* 忽略 .el-input-group__append:hover 的样式定义 */
  .el-input-group__append:not(:active):not(:focus) {
    background-color: #F1F1F1;
    color: #524C42;
  }

  // 图标颜色
  .title{
    width: 100%;
    text-align: center;
    font-size: 4rem;
    color: #803D3B;
    font-weight: bolder;
  }

  .mobile-top {
    display: flex;
    flex-direction: row; /* 横向排列 */
    justify-content: center; /* 在水平方向上居中 */
    align-items: center; /* 在垂直方向上居中 */

  }
  .mobile-top h2{
    margin-top: 0;
  }

  .mobile-top p{
    margin-top: 0;
  }

  .movie-info{
    width: 98%;
    padding-top: 0;
    height: auto;
  }

  .movie-picture {
    width: auto; /* 设置宽度自动调整 */
    max-width: 40%; /* 最大宽度为40% */
    display: block; /* 将照片设置为块级元素 */
    margin: 0.5rem 0; /* 调整图片与下方文字之间的间距 */
    margin-right: 1.5rem;
  }


  .moblie-text{
    max-width: 60%;
  }

  .el-main ul{
    width: 85%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    list-style-type: none;
    padding: 0 0;
  }
  .input-div {
    display: flex;
    margin: 2rem auto;
    width: 80%;
    height: 5.5vh;
    border-radius: 95px;
    background-color: #fff;
  }

}

</style>
