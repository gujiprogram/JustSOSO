<template>
  <el-footer>
      <div class="footer-content" style="padding-top: 0.5rem;">
        <el-icon size="14px" style="color: #FCF5ED"><Handbag /></el-icon>
        <a href="/" style="color: #FCF5ED; font-weight: bold">商务合作</a>
      </div>
      <div class="footer-content">
        <p>本站资源均来自互联网，如侵犯到您的版权，请及时<a href="/" style="color: #FCF5ED; font-weight: bold">联系我们</a>删除。</p>
      </div>
  </el-footer>
</template>

<script>

</script>

<style scoped>
.el-footer {
  bottom:0;
  align-self: flex-end;
  left:0;
  width: 100%;
  background-color: #803D3B;
  height: 5rem;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

@media screen and (max-width: 600px) {

  .el-footer {
    bottom:0;
    left:0;
    width: auto;
    background-color: #803D3B;
    height: 5rem;
    padding: 0 0;
    margin: 0 0;
  }

  .footer-content {
    display: flex;
    justify-content: center;
    font-size: 14px;
    padding: 0 0;
    margin: 0 0;
    color: whitesmoke;
  }

}

@media screen and (max-width: 430px) {

  .el-footer {
    bottom:0;
    left:0;
    width: 100%;
    background-color: #803D3B;
    height: auto;
  }

  .footer-content {
    display: flex;
    justify-content: center;
    font-size: 12px;
    color: whitesmoke;
  }

}


</style>
