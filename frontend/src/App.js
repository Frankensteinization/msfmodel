import React, { useState } from "react";
import axios from "axios";
import ImageComponent from "./ImageComponent";
import MapComponent from "./MapComponent";

function App() {
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRunPython = () => {
    setResult("");
    setError("");
    setLoading(true);
    axios
      .post("http://localhost:10000/run-python")
      .then((response) => {
        // 假设response.data.output是一个字符串，已经被格式化为多行文本
        const formattedResult = formatResult(response.data.output); // 格式化结果的函数
        setResult(formattedResult);
        setLoading(false);
      })
      .catch((error) => {
        console.error("发送请求时出错:", error);
        setError("发送请求时出错");
        setLoading(false);
      });
  };

  // 格式化结果的函数，可以根据你的需要进行定制
  const formatResult = (rawResult) => {
    // 例如，这里简单地将原始字符串分割为多行
    return rawResult
      .split("\n")
      .map((line, index) => <p key={index}>{line}</p>);
  };

  return (
    <div
      className='App d-flex justify-content-center align-items-center'
      style={{ minHeight: "100vh" }}
    >
      <div className='d-flex flex-column align-items-center'>
        <button
          className='btn btn-primary btn-lgy'
          onClick={handleRunPython}
          disabled={loading}
        >
          {loading ? "正在运行..." : "点击运行 Python"}
        </button>
        {loading && (
          <div className='spinner-border text-primary mt-3' role='status'>
            <span className='visually-hidden'>正在加载...</span>
          </div>
        )}
        {error && <div className='mt-3 text-danger'>{error}</div>}
        {result && (
          <div className='mt-3 text-start'>
            {result}
            <MapComponent />
            <ImageComponent />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
