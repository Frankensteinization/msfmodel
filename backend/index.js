const express = require('express');
const { exec } = require('child_process');
const cors = require('cors'); // 导入 CORS 包
const path = require('path');

const app = express();
const port = 10000;
// const helmet = require('helmet');


app.use(cors()); // 启用 CORS
app.use(express.json());

// app.use(helmet.contentSecurityPolicy({
//     directives: {
//         defaultSrc: ["'self'"],
//         scriptSrc: ["'self'", "https://cdnjs.cloudflare.com"],
//         styleSrc: ["'self'", "'unsafe-inline'"],
//         imgSrc: ["'self'", "data:"],
//         // 其他必要的资源类型和源
//     },
// }));


// 定义一个路由来运行 Python 脚本并返回结果
app.post('/run-python', (req, res) => {
  exec('python MSF_Model_v1.0.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`执行 Python 文件时出错: ${error}`);
      res.status(500).send('执行 Python 文件时出错');
      return;
    }

    // 将 Python 脚本生成的输出内容发送给前端
    res.send({ output: stdout });
  });
});

app.use(express.static(path.join(__dirname, '..')));

app.listen(port, () => {
  console.log(`后端服务器运行在 http://localhost:${port}`);
});
