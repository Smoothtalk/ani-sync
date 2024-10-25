import React from "react";
import styles from "../css/anime/animetitle.module.css";

export default function AnimeTitle({ title, anime_id }) {
  return (
    <div className={styles.titleDiv}>
      <a
        href={`https://anilist.co/anime/${anime_id}`}
        target="_blank"
        className={styles.title}
      >
        {title}
      </a>
    </div>
  );
}
