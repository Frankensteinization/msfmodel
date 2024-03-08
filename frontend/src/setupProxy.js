const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/run-python',
    createProxyMiddleware({
      target: 'http://localhost:10000',
      changeOrigin: true,
    })
  );
};
