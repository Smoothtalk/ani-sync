import React from "react";
import styles from "../css/anime/animeepisodenum.module.css";

export default function AnimeEpisodeNum({ episode }) {
  return <div className={styles.episode}>{episode}</div>;
}
