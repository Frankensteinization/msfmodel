function MapComponent() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100%",
      }}
    >
      <iframe
        src='http://localhost:10000/map.html'
        style={{ width: "600px", height: "400px", border: "none" }}
        title='Map'
      ></iframe>
    </div>
  );
}
export default MapComponent;
