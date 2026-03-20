# 使用 Nginx 作为基础镜像
FROM nginx:alpine

# 将本地的 my_vue.conf 拷贝到容器的配置目录中
COPY my_vue.conf /etc/nginx/conf.d/default.conf

# 拷贝构建后的 Vue.js 项目到 Nginx 的 html 目录
COPY my_vue/dist /usr/share/nginx/html

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx 服务
CMD ["nginx", "-g", "daemon off;"]
