import React, { useContext, useState } from "react";
import style from "../css/recentdownloads/recentdownloadstitlebar.module.css";

export default function RecentDownloadsTitleBar() {
  return (
    <div className={style.titlebar}>
      <p className={style.icon}>Icon</p>
      <p className={style.title}>Title</p>
      <p className={style.episodeNum}>#</p>
      <p className={style.pubDate}>Publish Date</p>
    </div>
  );
}
