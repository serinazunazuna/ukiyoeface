function startVideo() {
  console.info("入出力デバイスを確認してビデオを開始するよ！");

  Promise.resolve()
    .then(function () {
      return navigator.mediaDevices.enumerateDevices();
    })
    .then(function (mediaDeviceInfoList) {
      console.log("使える入出力デバイスs->", mediaDeviceInfoList);

      var videoDevices = mediaDeviceInfoList.filter(function (deviceInfo) {
        return deviceInfo.kind == "videoinput";
      });
      if (videoDevices.length < 1) {
        throw new Error("ビデオの入力デバイスがない、、、、、。");
      }

      return navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
          deviceId: videoDevices[0].deviceId,
        },
      });
    })
    .then(function (mediaStream) {
      console.log("取得したMediaStream->", mediaStream);
      videoStreamInUse = mediaStream;
      document.querySelector("video").srcObject = mediaStream;
      // 対応していればこっちの方が良い
      // document.querySelector('video').srcObject = mediaStream;
    })
    .catch(function (error) {
      console.error("ビデオの設定に失敗、、、、", error);
    });
}

function stopVideo() {
  console.info("ビデオを止めるよ！");

  videoStreamInUse.getVideoTracks()[0].stop();

  if (videoStreamInUse.active) {
    console.error("停止できかた、、、", videoStreamInUse);
  } else {
    console.log("停止できたよ！", videoStreamInUse);
  }
}

function snapshot() {
  var videoElement = document.querySelector("video");
  var canvasElement = document.querySelector("canvas");
  var context = canvasElement.getContext("2d");

  context.drawImage(
    videoElement,
    0,
    0,
    videoElement.width,
    videoElement.height
  );
  document.querySelector("img").src = canvasElement.toDataURL("image/png");
  const result = document.getElementById("result");
  result.removeAttribute("style");
  canvasElement.toBlob(submit);
}

async function submit(blob) {
  const imgFile = new File([blob], "snapshot.png", { type: "image/png" });
  const fd = new FormData();
  fd.append("upload_image", imgFile);

  const response = await fetch("/upload_image", {
    method: "POST",
    body: fd,
  });
  const data = await response.json();

  const external_url = data.track.external_urls.spotify;
  window.open(external_url);
}

startVideo();
