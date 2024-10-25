import React from "react";
import styles from "../css/anime/animetitle.module.css";

export default function AnimeTitle({ title }) {
  return <div className={styles.title}>{title}</div>;
}
