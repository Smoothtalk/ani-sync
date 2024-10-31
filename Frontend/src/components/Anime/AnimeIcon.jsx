import React, { useEffect, useState } from "react";
import styles from "../css/anime/animeicon.module.css";

export default function AnimeIcon({ icon_url, anime_id }) {
  return (
    <div className={styles.animeIconDiv}>
      <a href={`https://anilist.co/anime/${anime_id}`} target="_blank">
        <img className={styles.animeIcon} src={icon_url} />
      </a>
    </div>
  );
}
