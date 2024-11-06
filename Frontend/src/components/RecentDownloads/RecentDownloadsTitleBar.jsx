import React, { useContext, useEffect, useState } from "react";
import style from "../css/recentdownloads/recentdownloadstitlebar.module.css";

export default function RecentDownloadsTitleBar() {
  const [text, setText] = useState("");

  useEffect(() => {
    function handleResizePubDate() {
      if (window.innerWidth < 1300) {
        setText("Date");
      } else {
        setText("Publish Date");
      }
    }

    handleResizePubDate();

    window.addEventListener("resize", handleResizePubDate);
    return () => window.removeEventListener("resize", handleResizePubDate);
  }, []);

  return (
    <div className={style.titlebar}>
      <p className={style.icon}>Icon</p>
      <p className={style.title}>Title</p>
      <p className={style.episodeNum}>#</p>
      <p className={style.pubDate}>{text}</p>
    </div>
  );
}
