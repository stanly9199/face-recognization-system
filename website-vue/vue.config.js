const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
// module.exports = {
//   devServer: {
//     historyApiFallback: true,
//     allowedHosts: 'all',
//    },
// };

module.exports = {
  devServer: {
    https: false,
    port: 8080,  // 你的端口
    client: {
      webSocketURL: 'wss://0.0.0.0/ws',  // 使用 wss 协议，确保 WebSocket 是安全的
    },
    allowedHosts: 'all',  // 允许来自任何主机的请求
  }
}
