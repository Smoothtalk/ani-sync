import React from "react";
import styles from "../css/anime/animetitle.module.css";

export default function AnimeTitle({ title }) {
  return (
    <div className={styles.titleDiv}>
      <p className={styles.title}>{title}</p>
    </div>
  );
}
